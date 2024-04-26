import os
import json
import numpy as np

def extract_speaker_sample(transcript:list) -> list:

    speaker_cnt = np.max([tr['speaker'] for tr in transcript])
    speaker_sample = [{'speaker':tag+1, 'contents':'', 'start_time':0, 'end_time':0} for tag in range(speaker_cnt)]
    # print(speaker_sample)
    # print()
    # print(transcript)
    for tr in transcript:
        tag = tr['speaker'] - 1
        if speaker_sample[tag]['contents'] != '':
            old = speaker_sample[tag]['end_time'] - speaker_sample[tag]['start_time']
            new = tr['end_time'] - tr['start_time']
            if new > old:        
                # Update to longer sample 
                speaker_sample[tag]['contents'] = tr['contents']
                speaker_sample[tag]['start_time'] = tr['start_time']
                speaker_sample[tag]['end_time'] = tr['end_time']
                # print(f"{tag} updated!! {old}s -> {new}s")

        else:
            # Initialization
            speaker_sample[tag]['contents'] = tr['contents']
            speaker_sample[tag]['start_time'] = tr['start_time']
            speaker_sample[tag]['end_time'] = tr['end_time']
            # print(f"{tag} initialized! {tr['start_time']}, {tr['end_time']}")

    print(f"Extracted audio samples by each speaker tag!")
    for sample in speaker_sample:
        print(f"{sample['speaker']} : {sample['contents'][:50]}... ({sample['end_time']-sample['start_time']:.2f}s)")
    print()
    return speaker_sample

def map_speaker_tag(transcript:list, speaker:list) -> dict:

    speaker_cnt = np.max([tr['speaker'] for tr in transcript])
    speaker_tags = [tag+1 for tag in range(speaker_cnt)]

    # assert len(speaker_tags) == len(speaker), "item counts are different!"
    if len(speaker_tags) != len(speaker):
        print(f"item counts are different!\trecognized: {len(speaker_tags)} people\tuser input: {len(speaker)} people")
        print("Reduce the size of user input!")
        speaker = speaker[:len(speaker_tags)]
    speaker_tag = dict(zip(speaker_tags, speaker))

    print(f"Mapped speaker's name into the tag!")
    print()
    return speaker_tag

def convert_transcript_json2txt(transcript_json:list, speaker:list) -> str:
    transcript_txt = ''
    is_monologue = (len(speaker) == 1)
    speaker_tag = map_speaker_tag(transcript_json, speaker)
    print(speaker_tag)
    for tr in transcript_json:
        tag = tr['speaker']
        if is_monologue: tag = 1
        speaker = speaker_tag[tag]
        content = tr['contents']
        transcript_txt += f"{speaker}:\n{content}\n\n"

    print(f"Converted transcript json into txt! {len(transcript_txt)}")
    print()
    return transcript_txt

def save_result(filename:str, contents) -> str:

    _, ext = os.path.splitext(filename)

    if ext.lower() == ".json":
        with open(filename, 'w') as f:
            json.dump(contents, f, indent=4)

    elif ext.lower() == ".txt":
        with open(filename, "w") as f:
            f.write(contents)
    
    print(f"Saved contents into the file! \n{filename}")
    print()
    return 