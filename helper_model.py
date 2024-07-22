import librosa
import soundfile
import numpy as np  

PATH_SAVED_MODEL = ".\\saved_models\\model_2024-07.pkl"

OBSERVED_EMOTIONS = ['neutral', 'calm', 'happy', 'sad', 'angry', 'fearful']    # 'disgust', 'surprised' 

# === === === === ===

# Function to extract features (mfcc, chroma, mel) from an audio file
def extract_features_from_audio_file(wav_file_path, mfcc, chroma, mel):

    with soundfile.SoundFile(wav_file_path) as sound_file:
        sound_array = sound_file.read(dtype="float32")
        sample_rate = sound_file.samplerate
        result = np.array([])
        if chroma:
            stft   = np.abs(librosa.stft(sound_array))
        if mfcc:
            mfccs  = np.mean(librosa.feature.mfcc(y=sound_array, sr=sample_rate, n_mfcc=40).T, axis=0)
            result = np.hstack((result, mfccs))
        if chroma:
            chroma = np.mean(librosa.feature.chroma_stft(S=stft, sr=sample_rate).T,axis=0)
            result = np.hstack((result, chroma))
        if mel:
            #mel=np.mean(librosa.feature.melspectrogram(X, sr=sample_rate).T,axis=0)
            mel    = np.mean(librosa.feature.melspectrogram(y=sound_array, sr=sample_rate).T,axis=0)
            result = np.hstack((result, mel))
    
    return result

# === === === === ===