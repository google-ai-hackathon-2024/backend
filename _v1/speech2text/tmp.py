import json
import os
import gcp_speech2text as sp2txt
import transcript as trs
import constants

CREDENTIALS_FILE = "../gcp-credential/key.json"

if __name__ == "__main__":

    # biz-meeting, debating, interview, monologue
    style = 'monologue'
    gcs_uri_wav_lst = constants.gcs_uri_wav[style]
    speaker_info_lst = constants.speaker[style]

    for idx, gcs_uri_wav in enumerate(gcs_uri_wav_lst):
        # ------------------------------------------------------------------

        print(gcs_uri_wav)

        # -------------------------------------------------------------------
        subfolder1, subfolder2 = gcs_uri_wav.split('/')[-2:]
        subfolder2 = subfolder2.split('.')[0]
        save_root = os.path.join('results',subfolder1,subfolder2)
        if not os.path.exists(save_root): os.makedirs(save_root)

        transcript_json_path = os.path.join(save_root, 'transcript.json')
        with open(transcript_json_path, 'r') as file:
            transcript = json.load(file)
        
        speaker = speaker_info_lst[idx]['speakers']
        transcript_txt = trs.convert_transcript_json2txt(transcript, speaker)

        transcript_txt_path = transcript_json_path.replace('.json', '.txt')
        trs.save_result(transcript_txt_path, transcript_txt)

        print()
        print()