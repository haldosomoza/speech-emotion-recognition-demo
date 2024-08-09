import os
import librosa
import soundfile as sf

import helper_files as my_hf   # Importing my helper_files.py module

#from pytube import YouTube
#from pytube.cli import on_progress
from moviepy.editor import VideoFileClip

from pydub import AudioSegment
from pydub.silence import split_on_silence

AUDIO_HOMOGENIZED_BITRATE = 16000 # "256k"

AUDIO_SEGMENTS_DURATION = 3 # seconds

AUDIO_MIN_SILENCE_LENGH = 500 # miliseconds
AUDIO_SILENCE_THRESH = -40 # dBFS
AUDIO_KEEP_SILENCE = 500 # miliseconds
AUDIO_REMAIN_MIN_LEN = 2000 # miliseconds

# === === === === ===

# Deprecated: Function get problems eventually with the youtube download
# Function to download video from YouTube and convert into wav audio 
def download_video_from_youtube_and_convert_to_wav_audio(video_url):
    print("Starting download_video_from_youtube_and_convert_to_wav_audio ...")
    
    # downloading the youtube video
    video_file_path = _download_mp4_video_from_youtube(video_url)
    print("Downloaded Video File Path:", video_file_path)
    
    # extracting the audio from the video
    audio_file_path = _convert_mp4_video_to_wav_audio(video_file_path)
    print("Converted Audio File Path:", audio_file_path)

    # returning the audio file path
    print("Finishing download_video_from_youtube_and_convert_to_wav_audio ...")
    return audio_file_path

# Function to load precharged audio and convert into wav audio 
def load_preloaded_audio_and_convert_to_wav_audio(audio_name):
    print("Starting load_preloaded_audio_and_convert_to_wav_audio ...")

    # setting the path of preloaded audio files
    audio_file_path = f"{my_hf.PATH_AUDIO_PRELOADED}/{audio_name}"
    print("Audio File Path:", audio_file_path)
    
    # extracting the audio from the video
    audio_file_path = _convert_mp4_video_to_wav_audio(audio_file_path)
    print("Converted Audio File Path:", audio_file_path)

    # returning the audio file path
    print("Finishing load_preloaded_audio_and_convert_to_wav_audio ...")
    return audio_file_path

# === === === === ===

# Function to split the audio file into smaller segments by duration
def split_wav_audio_file_by_duration(audio_file_path, segment_duration=AUDIO_SEGMENTS_DURATION):

    # loading the audio file
    y, sr = librosa.load(audio_file_path, sr=None) 
    print("Loaded Audio Size:", len(y))

    # calculating and splitting the audio file
    segment_samples = int(segment_duration * sr)
    segments = [y[i:i + segment_samples] for i in range(0, len(y), segment_samples)]
    print("Quantity Segments:", len(segments))

    # creating a file for each segment
    segments_file_paths = []
    for i, segment in enumerate(segments):
        print("Saving Audio Segment #:", i)
        segment_file_path = f"{my_hf.PATH_AUDIO_SPLITTED}/{os.path.basename(audio_file_path).replace('.wav','')}_Segment{str(i).zfill(3)}.wav"
        sf.write(segment_file_path, segment, sr) 
        #ffmpeg.input(segment_file_path).output(segment_file_path, audio_bitrate=AUDIO_HOMOGENIZED_BITRATE).run()
        segments_file_paths.append(segment_file_path)

    # returning the paths of the segment files
    return segments_file_paths    

# === === === === ===

def split_wav_audio_file_by_silence(audio_file_path, 
                                    min_silence_len=AUDIO_MIN_SILENCE_LENGH, 
                                    silence_thresh=AUDIO_SILENCE_THRESH, 
                                    keep_silence=AUDIO_KEEP_SILENCE,
                                    remain_min_len=AUDIO_REMAIN_MIN_LEN):
    """
    Splits an audio file based on silent periods.

    Parameters:
    - audio_file_path: The path to the input WAV file.
    - min_silence_len: Minimum length of silence in milliseconds to be considered a split point.
    - silence_thresh: Silence threshold in dBFS. Quieter than this value will be considered silence.
    - keep_silence: Amount of silence to keep at the beginning and end of each chunk in milliseconds.
    - remain_min_len: Minimum length of the audio fragment to be saved in milliseconds.

    Returns:
    - List of audio fragment file paths.
    """
    # loading the audio file
    audio = AudioSegment.from_wav(audio_file_path)
    print("Loaded Audio Size:", len(audio))

    # spliting audio based on silence
    segments = split_on_silence(
        audio,
        min_silence_len=min_silence_len,
        silence_thresh=silence_thresh,
        keep_silence=keep_silence
    )
    print("Quantity Segments:", len(segments))

    # creating a file for each segment
    segments_file_paths = []
    for i, chunk in enumerate(segments):
        if len(chunk) <= remain_min_len:
            print("Skipping Audio Segment #:", i)
            continue

        # converting to mono and setting bitrate
        chunk_mono = chunk.set_channels(1)  
        chunk_mono_bitrated = chunk_mono.set_frame_rate(AUDIO_HOMOGENIZED_BITRATE)

        print("Saving Audio Segment #:", i)
        segment_file_path = f"{my_hf.PATH_AUDIO_SPLITTED}/{os.path.basename(audio_file_path).replace('.wav','')}_Segment{str(i).zfill(3)}.wav"
        chunk_mono_bitrated.export(segment_file_path, format="wav") #, bitrate=AUDIO_HOMOGENIZED_BITRATE)
        segments_file_paths.append(segment_file_path)

    # returning the paths of the segment files
    return segments_file_paths    

# === === === === ===

# Function to download mp4 video from YouTube
def _download_mp4_video_from_youtube(video_url):

    yt = YouTube(video_url, on_progress_callback = on_progress)
    print("Youtube Title:", yt.title)
    
    youtube_video = yt.streams.get_lowest_resolution() #.get_audio_only()
    out_file_path = youtube_video.download(output_path=my_hf.PATH_AUDIO_DOWNLOADED) #, mp3=True) 
    print("Out Youtube Filename:", out_file_path)

    out_file_folder, out_file_name, out_file_extension = my_hf.split_file_path(out_file_path)
    mp4_file_path = out_file_folder + "/" + my_hf.generate_provisional_file_name("AUDIO") + out_file_extension 
    os.rename(out_file_path, mp4_file_path)
    print("New Youtube Filename:", out_file_path)

    # returning the path of the mp4 file
    return mp4_file_path

# === === === === ===

# Function to convert mp4 video to wav audio
def _convert_mp4_video_to_wav_audio(mp4_file_path):

    # loading the video file
    video = VideoFileClip(mp4_file_path)

    # saving the audio into a wav file
    wav_file_path = mp4_file_path.replace('.mp4', '.wav')
    video.audio.write_audiofile(wav_file_path)

    # returning the path of the wav file
    return wav_file_path

# === === === === ===