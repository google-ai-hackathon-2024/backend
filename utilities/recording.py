import os
import librosa
import soundfile as sf
import ffmpeg

SAMPLE_RATE = 48000

def audio_PCM_encoding(audio_path:str):

    input_audio = ffmpeg.input(audio_path)

    output_options = {
        "vn": True,  # Disable video stream
        "acodec": "pcm_s16le",  # Set audio codec to 16-bit PCM
        "ac": 1,  # Set number of audio channels to 1 (mono)
        "ar": SAMPLE_RATE,  # Set audio sample rate to 16 kHz
        "f": "wav",  # Set output format to WAV
    }
    enc_audio_path = audio_path.split('.')[0] + '_enc.wav'
    output_audio = input_audio.output(enc_audio_path, **output_options)
    output_audio.run(quiet=True, overwrite_output=True)
    print(f"new encoding Audio file: {enc_audio_path}")
    return enc_audio_path

def load_audio(audio_path:str):

    # Load the audio
    try:
        print(f"Read audio file with sr:{SAMPLE_RATE} Hz!")
        audio, sr = librosa.load(audio_path, sr=SAMPLE_RATE)
        return audio, sr
    except Exception as e:
        print(f"Error audio reading: {str(e)}")
        return None, None

def save_audio(audio_path:str, audio, sr):


    # Save the audio as .wav
    new_audio_path = audio_path.replace("_enc",f'_enc_{SAMPLE_RATE}')

    # librosa.output.write_wav(new_audio_path, audio, sr)
    sf.write(new_audio_path, audio, sr)
    print(f"Audio file is saved in {new_audio_path}")

    return new_audio_path

def check_and_convert_audio(audio_path):

    # Check if the file exists
    if not os.path.exists(audio_path):
        print(f"File {audio_path} does not exist.")
        return

    print(f"Try to encode audio file into wav with {SAMPLE_RATE} samplerate using PCM codec!")
    new_audio_path = audio_PCM_encoding(audio_path)
    audio, sr = load_audio(new_audio_path)
    new_audio_path = save_audio(new_audio_path, audio, sr)
    print(f"DONE: Checked and converted audio file!")
    return new_audio_path

def get_audio_files_in_folder(folder_path):
    """
    Get a list of audio files (in .wav, .mp3, .flac, or .ogg format) in the specified folder.
    """
    audio_files = []
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            _, ext = os.path.splitext(file)
            if ext.lower() in [".wav", ".mp3", ".flac", ".ogg"]:
                audio_files.append(os.path.join(root, file))
    
    print(f"Audio file detected! {len(audio_files)}")
    return audio_files

def get_audio_samples(audio, sr, speaker_samples):

    audio_samples = []
    for s in speaker_samples:

        start_s = s['start_time']
        end_s = start_s + 10

        start_idx, end_idx = librosa.time_to_samples([start_s, end_s], sr=sr)
        sample = audio[start_idx : end_idx]
        
        audio_samples.append(sample)
    
    return audio_samples, sr

def get_audio_sample_monologue(audio, sr):

    start_idx, end_idx = librosa.time_to_samples([0, 10], sr=sr)

    return [audio[start_idx : end_idx]], sr