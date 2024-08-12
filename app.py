import re
import streamlit as st
import pandas as pd
import altair as alt
import joblib

from PIL import Image

import helper_files as my_hf   # Importing my helper_files.py module
import helper_audio as my_ha   # Importing my helper_audio.py module
import helper_model as my_hm   # Importing my helper_model.py module

# === === === === ===

ABOUT_THIS_PROJECT = [
    "This is a demo for the Big Data Capstone Project for Lambton College, Mississauga.",
    "Instructor: Meysam Effati.",
    "Students:",
    "- C0898944, Adriana Penaranda",
    "- C0896129, Aruna Gurung",
    "- C0901167, Pujan Shretha",
    "- C0868575, Carlos Rey Pinto",
    "- C0904838, Haldo Somoza"
]

BASE_YOUTUBE_URL = "https://www.youtube.com/watch?v="

YOUTUBE_SAMPLES = [
    "https://www.youtube.com/watch?v=F8dImol79ew",
    "https://www.youtube.com/watch?v=Nao3M3UpPpI",
    "https://www.youtube.com/watch?v=DwOVXz74N9c",
    "https://www.youtube.com/watch?v=aYuEyUXj2xo",
    "https://www.youtube.com/watch?v=F2kJeD_cl5w",
    #"https://www.youtube.com/watch?v=hpZFJctBUHQ"
]

PRELOADED_SAMPLES = [
    "", # empty first option
    #"01-DEMO-TEST-AUDIO-VIDEO.mp4",
    #"02-DEMO-TEST-AUDIO-VIDEO.mp4",
    #"03-DEMO-TEST-AUDIO-VIDEO.mp4",
    "04-DEMO-TEST-AUDIO-VIDEO.mp4",
    "05-DEMO-TEST-AUDIO-VIDEO.mp4",
    "06-DEMO-TEST-AUDIO-VIDEO.mp4",
]

PATH_STYLE_CSS_FILE = "./static_content/style.css"
PATH_EMOTION_IMAGES = "./icon_images/face_prediction.png"

# removing the contents of the processing folders
my_hf.remove_folder_contents(my_hf.PATH_AUDIO_DOWNLOADED)
my_hf.remove_folder_contents(my_hf.PATH_AUDIO_SPLITTED)

# # reading the style css file
# with open(PATH_STYLE_CSS_FILE) as css_file:
#     st.markdown(f'<style>{css_file.read()}</style>', unsafe_allow_html=True)

# === === === === ===

st.title('Speech Emotion Recognition Demo')

# Button to trigger the modal popup
with st.expander("About this project ..."):
    for about_line in ABOUT_THIS_PROJECT:
        st.write(about_line)

# === === === === ===

st.markdown ("<br/>", unsafe_allow_html=True)
st.subheader('Step 1: Obtaining one audio file')

# youtube samples were deprecated because some problems with the download
# audio_source_selected = st.text_input('Enter a YouTube Video URL:', placeholder=BASE_YOUTUBE_URL)
# audio_source_selected = video_youtube_url.strip()
#
# with st.expander("Have no idea! Clic here to show you some examples you can try ..."):
#     for youtube_sample in YOUTUBE_SAMPLES:
#         st.markdown(f"- [{youtube_sample}]({youtube_sample})")

# preloaded samples were added to avoid the youtube download
audio_source_selected = st.selectbox('Select one Sample Audio:', PRELOADED_SAMPLES)

audio_obtained = False
if audio_source_selected:
    try:
        # youtube samples were deprecated because some problems with the download
        # if (not video_youtube_url.startswith(BASE_YOUTUBE_URL) or \
        #     not re.match(r'^[a-zA-Z0-9_-]{11}$', video_youtube_url.replace(BASE_YOUTUBE_URL, ''))):
        #     raise Exception("Invalid YouTube URL")

        with st.spinner('Loading and converting resource into wav audio file ...'):
            try:
                # youtube samples were deprecated because some problems with the download
                # audio_wav_file_path = my_ha.download_video_from_youtube_and_convert_to_wav_audio(audio_source_selected)
                # --- --- ---
                # preloaded samples were added to avoid the youtube download
                audio_wav_file_path = my_ha.load_preloaded_audio_and_convert_to_wav_audio(audio_source_selected)
            except Exception as ex: raise Exception("Resource Not Found")
            st.success('Resource loaded and converted into wav audio file !')

            # showing one audio sampling control 
            audio_file = open(audio_wav_file_path, 'rb')
            audio_file_bytes = audio_file.read()
            st.audio(audio_file_bytes, format='audio/wav')

        audio_obtained = True
    except Exception as ex:
        st.error(f"An error occurred: {ex}")

# === === === === ===

audio_preprocessed = False
if audio_obtained:
    st.markdown ("<br/>", unsafe_allow_html=True)
    st.subheader('Step 2: Preprocessing the audio file')
    try:
        with st.spinner('Splitting the audio file and removing silence segments ...'):
            #segments_audio_file_paths = my_ha.split_wav_audio_file_by_duration(audio_wav_file_path) # replaced for next line
            segments_audio_file_paths = my_ha.split_wav_audio_file_by_silence(audio_wav_file_path)
            segments_audio_file_feats = []
            for i, segment_audio_file_path in enumerate(segments_audio_file_paths):
                print("Featuring Audio Segment:", segment_audio_file_path)
                audio_features = my_hm.extract_features_from_audio_file(segment_audio_file_path, mfcc=True, chroma=True, mel=True)
                segments_audio_file_feats.append(audio_features)
            st.success(f'Audio splitted and preprocessed into {len(segments_audio_file_paths)} smaller pieces !')

        audio_preprocessed = True
    except Exception as ex:
        st.error(f"An error occurred: {ex}")

# === === === === ===

emotions_predicted = False
if audio_preprocessed:
    st.markdown ("<br/>", unsafe_allow_html=True)
    st.subheader('Step 3: Predicting the emotions')
    try:
        with st.spinner('Loading the model and predicting ...'):
            # loading the model
            model = joblib.load(my_hm.PATH_SAVED_MODEL)
            # predicting the emotions
            predictions = model.predict(segments_audio_file_feats)
            print("Predictions: ", predictions)
            st.success('Predicted the emotions in the audio !')

        emotions_predicted = True
    except Exception as ex:
        st.error(f"An error occurred: {ex}")

# === === === === ===

if emotions_predicted:
    st.markdown ("<br/>", unsafe_allow_html=True)
    st.subheader('Step 4: Showing the emotions detected')

    # creating and populating columns with predictions
    num_columns = 10
    column_images = st.columns(num_columns)
    for i, prediction in enumerate(predictions):
        col_index = i % num_columns
        #columns[col_index].write(prediction)
        column = column_images[col_index]
        with column:
            image = Image.open(PATH_EMOTION_IMAGES.replace('prediction', prediction))
            st.image(image, caption=prediction, use_column_width=True)

    # calculating the emotion summary and saving it as a dataframe
    prediction_list = list(predictions)
    label_counts = {label: prediction_list.count(label) for label in set(prediction_list)}
    total_count  = len(prediction_list)
    label_percentages = {label: (round(count/total_count,4)) for label, count in label_counts.items()}
    df = pd.DataFrame(list(label_percentages.items()), columns=['Labels', 'Percentages'])
    df = df.sort_values(by='Percentages', ascending=False).reset_index(drop=True)

    # creating the emotion summary as a text with percentages
    st.write("Emotion Summary")
    html_spaces = "&nbsp;" * 10
    #st.dataframe(df) # displaying the emotion summary as dataframe
    column_texts = st.columns(df.shape[0])
    for i in df.index:
        column = column_texts[i]
        with column:
            st.write(f"{html_spaces} {df.iloc[i,0]}: {df.iloc[i,1]*100:.2f}%")

    # creating the emotion summary as a horizontal bar chart
    chart = alt.Chart(df).mark_bar().encode(
        x=alt.X('Percentages', axis=alt.Axis(format='%')),
        y=alt.Y('Labels', sort='-x'),
        #color='Labels'
    )#.properties(title='Emotion Summary')
    st.altair_chart(chart, use_container_width=True)

# === === === === ===

print("Finished successfully !")