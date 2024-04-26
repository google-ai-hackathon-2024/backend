import json
import os
import gcp_speech2text as sp2txt
import transcript as trs
import constants

CREDENTIALS_FILE = "../gcp-credential/key_new.json"

if __name__ == "__main__":

    # biz-meeting, debating, interview, monologue
    style = 'biz-meeting'
    gcs_uri_wav_lst = constants.gcs_uri_wav[style]
    speaker_info_lst = constants.speaker[style]

    # For Test Run
    gcs_uri_wav_lst = [constants.gcs_uri_wav[style][0]]
    speaker_info_lst = [constants.speaker[style][0]]

    for idx, gcs_uri_wav in enumerate(gcs_uri_wav_lst):
        # -------------------------------------------------------------------
        script_conf_pairs, word_infos = sp2txt.speech_to_text(gcs_uri_wav, 
                                                                  CREDENTIALS_FILE, 
                                                                  speaker_info_lst[idx]['min_max'])
        
        transcript = sp2txt.generate_transcript_with_tag(word_infos)



        # NOTE: 'speaker' is going to be set by User Input through Front-end
        # speaker_sample is used for getting this User Input
        if speaker_info_lst[idx]['min_max'] != (1,1):
            speaker_sample = trs.extract_speaker_sample(transcript)
            print(speaker_sample)
        speaker = speaker_info_lst[idx]['speakers'] 
        

        transcript_txt = trs.convert_transcript_json2txt(transcript, speaker)

        print()

        # # -------------------------------------------------------------------
        subfolder1, subfolder2 = gcs_uri_wav.split('/')[-2:]
        subfolder2 = subfolder2.split('.')[0]
        save_root = os.path.join('results',subfolder1,subfolder2)
        if not os.path.exists(save_root): os.makedirs(save_root)

        script_conf_pairs_path = os.path.join(save_root, 'script_conf_pairs.json')
        trs.save_result(script_conf_pairs_path, script_conf_pairs)

        word_infos_path = os.path.join(save_root, 'word_infos.json')
        trs.save_result(word_infos_path, word_infos)

        transcript_json_path = os.path.join(save_root, 'transcript.json')
        trs.save_result(transcript_json_path, transcript)

        transcript_txt_path = transcript_json_path.replace('.json', '.txt')
        trs.save_result(transcript_txt_path, transcript_txt)

        print()
        print()