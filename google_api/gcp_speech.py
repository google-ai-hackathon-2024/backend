from google.cloud import speech

SAMPLE_RATE = 48000

def init_speech_client(credential_path:str):
    client = speech.SpeechClient.from_service_account_file(credential_path)
    return client

def speech_to_text(client:speech.SpeechClient ,gcs_uri: str, speakers=(2,2)):
    """Asynchronously transcribes the audio file specified by the gcs_uri.
    """
    # ---------------------------------------------------------------------
    audio = speech.RecognitionAudio(uri=gcs_uri)

    print(f"Google Cloud Storage: {gcs_uri}\nWaiting for Speech-to-Text to complete...")
    print(f"Speak diarization - min:{speakers[0]}, max:{speakers[1]}")
    is_monologue = False
    if speakers == (1, 1):
        speakers = (2, 2)
        is_monologue = True
        print("It is Monologue")
    diarization_config = speech.SpeakerDiarizationConfig(
        enable_speaker_diarization=True,
        min_speaker_count=speakers[0],
        max_speaker_count=speakers[1],
    )
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16, # For .wav
        sample_rate_hertz=SAMPLE_RATE, 
        language_code="en-US",
        diarization_config=diarization_config,
        enable_word_time_offsets=True
    )
    operation = client.long_running_recognize(config=config, audio=audio)

    # ---------------------------------------------------------------------
    response = operation.result(timeout=300)

    # ---------------------------------------------------------------------
    # Each result is for a consecutive portion of the audio. Iterate through
    # them to get the transcripts for the entire audio file.
    script_conf_pairs = []
    for result in response.results:
        # The first alternative is the most likely one for this portion.
        script_conf_pairs.append({"Transcript": result.alternatives[0].transcript,
                                   "Confidence": result.alternatives[0].confidence})

    # The transcript within each result is separate and sequential per result.
    # However, the words list within an alternative includes all the words
    # from all the results thus far. Thus, to get all the words with speaker
    # tags, you only have to take the words list from the last result:
    result = response.results[-1]
    infos = result.alternatives[0].words
    # print(result.alternatives[0])
    word_infos = []
    for inf in infos:
        # print(inf)
        item = {"word":inf.word,
                "speaker_tag":inf.speaker_tag,
                "start_time": inf.start_time.total_seconds(),
                "end_time": inf.end_time.total_seconds()}
        if is_monologue: item['speaker_tag'] = 1
        word_infos.append(item)    

    print("Completed!")
    print()
    return script_conf_pairs, word_infos

def generate_transcript_with_tag(word_infos):

    current = 0
    sentence = []
    transcript = []
    for i, info in enumerate(word_infos):
        
        word = info['word']
        tag = info['speaker_tag']


        # Initialize
        if i == 0:
            current, sentence = tag, [word]
            start = info['start_time']
            end = info['end_time']
            continue

        if current == tag:
            sentence.append(word)
            end = info['end_time']
        else:
            transcript.append({"speaker":current, "contents":' '.join(sentence), 
                               "start_time": start, "end_time":end})
            
            # Reset
            current, sentence = tag, [word]
            start = info['start_time']
            end = info['end_time']

    # Append Last script
    transcript.append({"speaker":current, "contents":' '.join(sentence),
                       "start_time": start, "end_time":end})
    
    print(f"Generated Transcript! {len(transcript)}")
    print()
    return transcript