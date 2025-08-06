import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Folder for music downloads
MUSIC_DIR = os.path.join(BASE_DIR, 'music')
os.makedirs(MUSIC_DIR, exist_ok=True)

# Function to get the download path
def get_download_path(subfolder='downloads'):
    path = os.path.join(MUSIC_DIR, subfolder)
    os.makedirs(path, exist_ok=True)
    return path

# Default screen to load
load_screen = 'downloader'