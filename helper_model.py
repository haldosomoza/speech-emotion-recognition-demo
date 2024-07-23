import librosa
import soundfile
import numpy as np  

PATH_SAVED_MODEL = "./saved_models/model_2024-07.pkl"

#OBSERVED_EMOTIONS = ['neutral', 'calm', 'happy', 'sad', 'angry', 'fearful']    # 'disgust', 'surprised' 

# === === === === ===

# Function to extract features (mfcc, chroma, mel) from an audio file
def extract_features_from_audio_file(wav_file_path, mfcc, chroma, mel):

    with soundfile.SoundFile(wav_file_path) as sound_file:
        sound_array = sound_file.read(dtype="float32")
        sample_rate = sound_file.samplerate
        result = np.array([])
        if mfcc:
            #print("Doing mfccs 01 ...")
            mfccs  = np.mean(librosa.feature.mfcc(y=sound_array, sr=sample_rate, n_mfcc=40).T, axis=0)
            #if mfccs.shape[0] > 1: mfccs = mfccs.flatten()  # if it has more thatn 1 dimension, then flatten it
            #print("Doing mfccs 02 ...")
            result = np.hstack((result, mfccs))
        if chroma:
            #print("Doing chroma 01 ...")
            stft   = np.abs(librosa.stft(sound_array))
            #print("Doing chroma 02 ...")
            chroma = np.mean(librosa.feature.chroma_stft(S=stft, sr=sample_rate).T,axis=0)
            #print("Doing chroma 03 ...")
            result = np.hstack((result, chroma))
        if mel:
            #print("Doing mel 01 ...")
            mel    = np.mean(librosa.feature.melspectrogram(y=sound_array, sr=sample_rate).T,axis=0)
            #if mel.shape[0] > 1: mel = mel.flatten()    # if it has more thatn 1 dimension, then flatten it
            #print("Doing mel 02 ...")
            result = np.hstack((result, mel))
    
    return result

# === === === === ===