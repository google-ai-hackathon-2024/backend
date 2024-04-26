import string
import random
import os

import recording.recording as rec
import recording.gcp_bucket as bucket
import speech2text.transcript as trs
import speech2text.gcp_speech2text as sp2txt
import summarization.vertexai_summary as summ
import summarization.prompt_template as ptemp

BUCKET_NAME = "talking-dataset"
CREDENTIALS_FILE = "gcp-credential/key.json"

def id_generator(size=6):
    chars=string.ascii_uppercase + string.digits
    return ''.join(random.choice(chars) for _ in range(size))

def delete_cache(cache_path):
    try:
        for filename in os.listdir(cache_path):
            file_path = os.path.join(cache_path, filename)
            if os.path.isfile(file_path):
                os.remove(file_path)
                print(f"Deleted {filename}")
        print("All files deleted successfully!")
    except Exception as e:
        print(f"An error occurred: {e}")

def generate_audio_sample_url(conv_id, audio_lst, sr):
    audio_url_lst = []
    for i, aud in enumerate(audio_lst):
        filename = f"{i+1}_sample_audio"
        audio_file_path = rec.save_audio(os.path.join('cache',filename), aud, sr)
        blob_name = f"{conv_id}/{filename}.wav"
        pub_audio_url = bucket.upload_to_gcs(source_file_path=audio_file_path,
                                            bucket_name=BUCKET_NAME, 
                                            blob_name=blob_name, 
                                            credentials=CREDENTIALS_FILE)
        audio_url_lst.append(pub_audio_url)
    return audio_url_lst

def upload_audio_to_gcpbucket(jdata:dict):
    """
    Upload a conversation audio file into the GCP bucket for the future use.

    input : 
        dict
        - filepath <string> : The file path of conversation audio 

    output :
        dict
        - convID <string> : Unique ID for the conversation
        - audioURL <string> : Audio file public URL in GCP bucket
    """

    filepath = jdata['filepath']

    filepath = rec.check_and_convert_audio(filepath)

    conv_id = id_generator()
    blob_name = f"{conv_id}/audio.wav"
    pub_audio_url = bucket.upload_to_gcs(source_file_path=filepath,
                                        bucket_name=BUCKET_NAME, 
                                        blob_name=blob_name, 
                                        credentials=CREDENTIALS_FILE)

    return {"convID":conv_id, "audioURL":pub_audio_url}

def set_config_for_transcript(jdata:dict):
    """
    Get basic configuration and generate transcript.

    input :
        dict 
        - convID <string> : Unique ID for the conversation
        - speakerCnt <int> : The number of speakers in conversation
    
    output :
        dict
        - convid <string> : Unique ID for the conversation
        - audioURLs <list:string> : Public GCP bucket link for sample audio chunks by each speaker
    """

    conv_id = jdata['convID']

    if jdata['speakerCnt'] == 1:
        speaker_cnt = (1,1) 
    else:
        speaker_cnt = (2, jdata['speakerCnt'])

    gcs_uri_wav = f"gs://{BUCKET_NAME}/{conv_id}/audio.wav"

    _, word_infos = sp2txt.speech_to_text(gcs_uri_wav, 
                                          CREDENTIALS_FILE, 
                                          speaker_cnt)
    transcript = sp2txt.generate_transcript_with_tag(word_infos)

    transcript_json_path = os.path.join('cache', 'raw_transcript.json')
    trs.save_result(transcript_json_path, transcript)
    
    blob_name = f"{conv_id}/raw_transcript.json"
    pub_transcript_url = bucket.upload_to_gcs(source_file_path=transcript_json_path,
                                            bucket_name=BUCKET_NAME, 
                                            blob_name=blob_name, 
                                            credentials=CREDENTIALS_FILE)
    
    # Depends on the number of speaker, create audio sample and get gcp bucket public links
    blob_name = f"{conv_id}/audio.wav"
    audio, sr = bucket.get_audio_from_gcs(bucket_name=BUCKET_NAME, 
                                          blob_name=blob_name, 
                                          credentials=CREDENTIALS_FILE)

    if jdata['speakerCnt'] == 1:
        print("It is monologue!")
        audio_lst, sr = rec.get_audio_sample_monologue(audio, sr)
    else:
        speaker_samples = trs.extract_speaker_sample(transcript)
        audio_lst, sr = rec.get_audio_samples(audio, sr, speaker_samples)
    
    audio_url_lst = generate_audio_sample_url(conv_id, audio_lst, sr)

    return {"convID":conv_id, "audioURLs":audio_url_lst}

def generate_result(jdata:dict):
    """
    Get information of speaker name, conversation type, and title to generate the final transcript.
    Finally, return the summary link and chatbot link

    input : 
        dict
        - convID <string> : Unique ID for the conversation
        - convType <int> : Conversation type
                            0. biz-meeting 1. debating 2. interview 3. monologue
        - convTitle <string> : Conversation title set by user
        - speakerName <list:string> : The name of speaker
    
    output :
        dict
        - convid <string> : Unique ID for the conversation
        - transcriptURL <string> : Public GCP bucket link for the summary
        - summaryURL <string> : Public GCP bucket link for the transcript
        - chatbotURL <string> : Chatbot activation link
    """

    # Get parameters
    conv_id = jdata['convID']
    conv_type = jdata['convType']
    conv_title = jdata['convTitle']
    speaker_name = jdata['speakerName']

    # Get transcript and change it to string type
    blob_name = f"{conv_id}/raw_transcript.json"
    transcript = bucket.get_json_from_gcs(bucket_name=BUCKET_NAME, 
                                          blob_name=blob_name, 
                                          credentials=CREDENTIALS_FILE)
    transcript = trs.convert_transcript_json2txt(transcript, speaker_name)
    
    # Generate the summary
    template = ptemp.get_template(conv_type)
    summary = summ.generate_summary(credentials=CREDENTIALS_FILE, 
                                    template=template, 
                                    transcript=transcript, 
                                    conv_title=conv_title)

    # Save the result into the GCP bucket
    transcript_txt_path = os.path.join('cache', 'transcript.txt')
    trs.save_result(transcript_txt_path, transcript)
    blob_name = f"{conv_id}/transcript.txt"
    pub_transcript_url = bucket.upload_to_gcs(source_file_path=transcript_txt_path,
                                            bucket_name=BUCKET_NAME, 
                                            blob_name=blob_name, 
                                            credentials=CREDENTIALS_FILE)

    summary_txt_path = os.path.join('cache', 'summary.txt')
    trs.save_result(summary_txt_path, summary)
    blob_name = f"{conv_id}/summary.txt"
    pub_summary_url = bucket.upload_to_gcs(source_file_path=summary_txt_path,
                                            bucket_name=BUCKET_NAME, 
                                            blob_name=blob_name, 
                                            credentials=CREDENTIALS_FILE)

    # Delete Cache files...
    delete_cache('./cache')

    return {"convID":conv_id, "summaryURL":pub_summary_url, "transcriptURL":pub_transcript_url, "chatbotURL": ''}

def get_result(conv_id:string):

    pub_transcript_url = f"https://storage.googleapis.com/{BUCKET_NAME}/{conv_id}/transcript.txt"
    pub_summary_url = f"https://storage.googleapis.com/{BUCKET_NAME}/{conv_id}/summary.txt"
    
    return {"convID":conv_id, "summaryURL":pub_summary_url, "transcriptURL":pub_transcript_url, "chatbotURL": ''}
