import os
import librosa
import soundfile as sf

import helper_files as my_hf   # Importing my helper_files.py module

from pytubefix import YouTube
from pytubefix.cli import on_progress
from moviepy.editor import VideoFileClip

AUDIO_SEGMENTS_DURATION = 3 # seconds

# === === === === ===

# Function to download video from YouTube and convert into wav audio 
def download_video_from_youtube_and_convert_to_wav_audio(video_url):
    
    # downloading the youtube video
    video_file_path = _download_mp4_video_from_youtube(video_url)
    
    # extracting the audio from the video
    audio_file_path = _convert_mp4_video_to_wav_audio(video_file_path)
    
    # returning the audio file path
    return audio_file_path

# === === === === ===

# Function to split the audio file into smaller segments
def split_wav_audio_file(audio_file_path, segment_duration=AUDIO_SEGMENTS_DURATION):

    # loading the audio file
    y, sr = librosa.load(audio_file_path, sr=None) 

    # calculating and splitting the audio file
    segment_samples = int(segment_duration * sr)
    segments = [y[i:i + segment_samples] for i in range(0, len(y), segment_samples)]

    # creating a file for each segment
    segments_file_paths = []
    for i, segment in enumerate(segments):
        segment_file_path = f"{my_hf.PATH_AUDIO_SPLITTED}/{os.path.basename(audio_file_path).replace('.wav','')}_Segment{str(i).zfill(3)}.wav"
        sf.write(segment_file_path, segment, sr)
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