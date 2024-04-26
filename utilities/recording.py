import os
import librosa
import soundfile as sf


def load_audio(audio_path:str):
    """
    ...

    Args:
        ...

    Returns:
        ...
    """
    # Load the audio
    try:
        audio, sr = librosa.load(audio_path, sr=16000)
        return audio, sr
    except Exception as e:
        print(f"Error loading {audio_path}: {str(e)}")
        return '', ''

def save_audio(audio_path:str, audio, sr):
    """
    ...

    Args:
        ...

    Returns:
        ...
    """
    format_to = '.wav'

    # Save the audio as .wav
    new_audio_path = os.path.splitext(audio_path)[0] + '_16k' + format_to
    # librosa.output.write_wav(new_audio_path, audio, sr)
    sf.write(new_audio_path, audio, sr)
    print(f"Audio file is saved in {new_audio_path}")

    return new_audio_path

def check_and_convert_audio(audio_path):
    """
    ...

    Args:
        ...

    Returns:
        ...
    """
    # Check if the file exists
    if not os.path.exists(audio_path):
        print(f"File {audio_path} does not exist.")
        return
    
    audio_file = audio_path.split('/')[-1]
    name, ext = os.path.splitext(audio_file)

    # Check if the file is in .wav format
    if ext.lower() == ".wav":
        print(f"{audio_file} is already in .wav format.")
        if name.split('_')[-1] == '16k':
            print(f"{audio_file} has already 16k sample rate.")
            return audio_path
        
    # Convert the file into .wav with 16k sample rate.
    audio, sr = load_audio(audio_path)
    new_audio_path = save_audio(audio_path, audio, sr)
    
    print(f"Checked and converted audio file!")
    return new_audio_path

def get_audio_files_in_folder(folder_path):
    """
    Get a list of audio files (in .wav, .mp3, .flac, or .ogg format) in the specified folder.

    Args:
        folder_path (str): Path to the folder containing audio files.

    Returns:
        list: List of audio file paths.
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

        speaker_tag = s['speaker']
        contents = s['contents'][:50]
        start_s = s['start_time']
        end_s = start_s + 10

        start_idx, end_idx = librosa.time_to_samples([start_s, end_s], sr=sr)
        sample = audio[start_idx : end_idx]
        
        audio_samples.append(sample)
    
    return audio_samples, sr

def get_audio_sample_monologue(audio, sr):

    start_idx, end_idx = librosa.time_to_samples([0, 10], sr=sr)

    return [audio[start_idx : end_idx]], sr