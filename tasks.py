import string
import random
import os
from pathlib import Path

from utilities import recording as rec
from utilities import transcript as trs

from google_api import gcp_storage as storage
from google_api import gcp_speech as speech
from google_api import vertexai_chatbot as chatbot
from google_api import vertexai_summary as summary
from google_api import template

BUCKET_NAME = "talking-dataset"

def init_gcp_client(credential_path:str, project_id:str, location:str):

    print("Check GCP credential!")
    credentials = chatbot.create_credential(credential_path)
    print("Init GCP Vertex AI!")
    chatbot.init_vertex_ai(project_id, location, credentials)
    print("Init GCP Storage API!")
    storage_client = storage.init_storage_client(credential_path)
    print("Init GCP Speech API!")
    speech_client = speech.init_speech_client(credential_path)

    print("Done!\n\n")
    return storage_client, speech_client

def id_generator(size=6):
    chars=string.ascii_uppercase + string.digits
    return ''.join(random.choice(chars) for _ in range(size))

def delete_cache(cache_path):

    try:
        for filename in os.listdir(cache_path):
            file_path = os.path.join(cache_path, filename)
            if os.path.isfile(file_path):
                os.remove(file_path)
        os.rmdir(cache_path)
        print(f"All files in {cache_path} and the folder itself are deleted successfully!")
    except Exception as e:
        print(f"An error occurred: {e}")

def generate_audio_sample_url(client, conv_id, audio_lst, sr):
    audio_url_lst = []
    for i, aud in enumerate(audio_lst):
        filename = f"{i+1}_sample_audio"
        audio_file_path = rec.save_audio(os.path.join('cache',conv_id,filename), aud, sr)
        blob_name = f"{conv_id}/{filename}.wav"
        pub_audio_url = storage.upload_to_gcs(
            client=client,
            bucket_name=BUCKET_NAME,
            source_file_path=audio_file_path, 
            blob_name=blob_name
            )
        audio_url_lst.append(pub_audio_url)
    return audio_url_lst

def upload_audio_to_gcpbucket(client, audio_file):
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

    conv_id = id_generator()
    print(f"Generated conversation ID : {conv_id}")
    cache_path = Path(f"./cache/{conv_id}")
    cache_path.mkdir(parents=True, exist_ok=True)

    print(f"Save the audio file into the cache folder : {cache_path}")
    filepath = f"{cache_path}/audio.wav"
    audio_file.save(filepath)

    filepath = rec.check_and_convert_audio(filepath)

    blob_name = f"{conv_id}/audio.wav"
    pub_audio_url = storage.upload_to_gcs(
        client=client,
        bucket_name=BUCKET_NAME, 
        source_file_path=filepath,
        blob_name=blob_name, 
        )

    return {"convID":conv_id, "audioURL":pub_audio_url}

def set_config_for_transcript(storage_client, speech_client, jdata:dict):
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

    _, word_infos = speech.speech_to_text(
        client = speech_client,
        gcs_uri = gcs_uri_wav, 
        speakers = speaker_cnt
        )
    transcript = speech.generate_transcript_with_tag(word_infos)

    transcript_json_path = os.path.join('cache', conv_id, 'raw_transcript.json')
    trs.save_result(transcript_json_path, transcript)
    
    blob_name = f"{conv_id}/raw_transcript.json"
    pub_transcript_url = storage.upload_to_gcs(
        client = storage_client,
        bucket_name=BUCKET_NAME, 
        source_file_path=transcript_json_path,
        blob_name=blob_name, 
        )
    
    # Depends on the number of speaker, create audio sample and get gcp bucket public links
    blob_name = f"{conv_id}/audio.wav"
    audio, sr = storage.get_audio_from_gcs(
        client = storage_client,
        bucket_name=BUCKET_NAME,
        blob_name=blob_name, 
        )

    if jdata['speakerCnt'] == 1:
        print("It is monologue!")
        audio_lst, sr = rec.get_audio_sample_monologue(audio, sr)
    else:
        speaker_samples = trs.extract_speaker_sample(transcript)
        audio_lst, sr = rec.get_audio_samples(audio, sr, speaker_samples)
    
    audio_url_lst = generate_audio_sample_url(storage_client, conv_id, audio_lst, sr)

    return {"convID":conv_id, "audioURLs":audio_url_lst}

def generate_result(client, jdata:dict):
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
    """

    # Get parameters
    conv_id = jdata['convID']
    conv_type = jdata['convType']
    conv_title = jdata['convTitle']
    speaker_name = jdata['speakerName']

    # Get transcript and change it to string type
    blob_name = f"{conv_id}/raw_transcript.json"
    transcript = storage.get_json_from_gcs(
        client = client,
        bucket_name=BUCKET_NAME, 
        blob_name=blob_name, 
        )
    transcript = trs.convert_transcript_json2txt(transcript, speaker_name)
    
    # Generate the summary
    summary_template = template.get_summary_template(conv_type)
    conv_summary = summary.generate_summary(
        template=summary_template, 
        transcript=transcript, 
        conv_title=conv_title
        )

    # Save the result into the GCP bucket
    transcript_txt_path = os.path.join('cache', conv_id, 'transcript.txt')
    trs.save_result(transcript_txt_path, transcript)
    blob_name = f"{conv_id}/transcript.txt"
    pub_transcript_url = storage.upload_to_gcs(
        client = client,
        bucket_name=BUCKET_NAME, 
        source_file_path=transcript_txt_path,
        blob_name=blob_name
        )

    summary_txt_path = os.path.join('cache', conv_id, 'summary.txt')
    trs.save_result(summary_txt_path, conv_summary)
    blob_name = f"{conv_id}/summary.txt"
    pub_summary_url = storage.upload_to_gcs(
        client = client,
        bucket_name=BUCKET_NAME, 
        source_file_path=summary_txt_path,
        blob_name=blob_name
        )

    # Delete Cache files...
    delete_cache(f'./cache/{conv_id}')

    return {"convID":conv_id, "summaryURL":pub_summary_url, "transcriptURL":pub_transcript_url}

def init_chatbot(conv_id:string):
    """
    Initialize and run AI chatbot. This chatbot can retrieve info. of conversation with convID.

    input : 
        - convID <string> : Unique ID for the conversation
    
    output :
        - retrieval_chain <Runnable>
    """
    chatbot_prompt_template = template.get_chatbot_template()
    return chatbot.initialize_chatbot(conv_id, chatbot_prompt_template)

def answer_from_chatbot(chatbot_runnable, jdata:dict):
    """
    Initialize and run AI chatbot. This chatbot can retrieve info. of conversation with convID.

    Request : 
        - input <string> : User input
    
    Response :
        - answer <string> : Answer from chatbot
    """
    user_input = jdata['input']
    answer = chatbot.get_chatbot_answer(chatbot_runnable, user_input)
    return {'answer':answer}

def get_result(conv_id:string):

    pub_transcript_url = f"https://storage.googleapis.com/{BUCKET_NAME}/{conv_id}/transcript.txt"
    pub_summary_url = f"https://storage.googleapis.com/{BUCKET_NAME}/{conv_id}/summary.txt"
    
    return {"convID":conv_id, "summaryURL":pub_summary_url, "transcriptURL":pub_transcript_url}
