import os
import shutil

from datetime import datetime

# === === === === ===

PATH_AUDIO_DOWNLOADED = "./01_audio_downloaded"
PATH_AUDIO_PRELOADED  = "./01_audio_preloaded"
PATH_AUDIO_SPLITTED   = "./02_audio_splitted"

# === === === === ===

# Function to remove the contents of a folder
def remove_folder_contents(folder_path):
    # if folder exists, remove its contents
    if os.path.exists(folder_path):
        for filename in os.listdir(folder_path):
            file_path = os.path.join(folder_path, filename)
            try:
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.remove(file_path)
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
            except Exception as e:
                print(f'Failed to delete {file_path}. Reason: {e}')
    # creating one empty folder
    os.makedirs(folder_path, exist_ok=True)

# === === === === ===

# Function to split the file path
def split_file_path(file_path):
    # spliting the directory and filename
    directory, filename = os.path.split(file_path)
    # spliting the filename and extension
    filename, extension = os.path.splitext(filename)
    # retuning the directory, filename, and extension
    return directory, filename, extension

# === === === === ===

# Function to generate a provisional name using one prefix and the current datetime
def generate_provisional_file_name(prefix):
    current_datetime = datetime.now().strftime("%Y%m%d_%H%M%S")
    provisional_name = f"{prefix}_{current_datetime}"
    return provisional_name

# === === === === ===