import os
import shutil
import sys
import logging
from mutagen import File
from mutagen.easyid3 import EasyID3
from mutagen.id3 import ID3NoHeaderError
from mutagen.mp4 import MP4, MP4Cover
from concurrent.futures import ThreadPoolExecutor, as_completed

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s')

def create_directory(path):
    if not os.path.exists(path):
        os.makedirs(path)

translation_table = str.maketrans(' :,/\\', '-----')
def process_str(val):
    return val.translate(translation_table)

def get_metadata(file_path):
    artist = 'Unknown Artist'
    album = 'Unknown Album'
    title = os.path.splitext(os.path.basename(file_path))[0]
    year = ''
    
    try:
        if file_path.endswith('.m4a'):
            audio = MP4(file_path)
            artist = audio.tags.get('\xa9ART', ['Unknown Artist'])[0]
            album = audio.tags.get('\xa9alb', ['Unknown Album'])[0]
            title = audio.tags.get('\xa9nam', [title])[0]
            year = audio.tags.get('\xa9day', [''])[0]
        else:
            audio = EasyID3(file_path)
            artist = audio.get('artist', ['Unknown Artist'])[0]
            album = audio.get('album', ['Unknown Album'])[0]
            title = audio.get('title', [title])[0]
            year = audio.get('date', [''])[0]
    except (ID3NoHeaderError, KeyError):
        try:
            audio = File(file_path)
            artist = audio.tags.get('artist', ['Unknown Artist'])[0]
            album = audio.tags.get('album', ['Unknown Album'])[0]
            title = audio.tags.get('title', [title])[0]
            year = audio.tags.get('date', [''])[0]
        except Exception as e:
            logging.error(f"Error reading metadata for {file_path} using File: {e}")
    except Exception as e:
        logging.error(f"Error reading metadata for {file_path}: {e}")
    
    return artist, album, title, year

def copy_file(file_path, dest_dir):
    try:
        artist, album, title, year = get_metadata(file_path)
        
        title = process_str(title)
        artist = process_str(artist)
        album = process_str(album)
        
        year_and_album = album
        if year:
            year_and_album = f'{year}-{album}'

        dest_path = os.path.join(dest_dir, artist, year_and_album)
        create_directory(dest_path)
        
        dest_file_path = os.path.join(dest_path, f"{title}{os.path.splitext(file_path)[1]}")
        
        if os.path.exists(dest_file_path):
            logging.info(f"File already exists and was not copied: {dest_file_path}")
        else:
            shutil.copy2(file_path, dest_file_path)
            logging.info(f"Copied {file_path} to {dest_file_path}")
    except Exception as e:
        logging.error(f"Error processing {file_path}: {e}")

def copy_music_files(source_dir, dest_dir, max_workers=4):
    if not os.path.isdir(source_dir):
        logging.error(f"Source directory '{source_dir}' does not exist or is not a directory.")
        sys.exit(1)

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = []
        for root, dirs, files in os.walk(source_dir):
            for file in files:
                if file.endswith(('.mp3', '.m4a', '.aac', '.wav', '.flac', '.ogg')):
                    file_path = os.path.join(root, file)
                    futures.append(executor.submit(copy_file, file_path, dest_dir))
        
        for future in as_completed(futures):
            future.result()

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python copy_music.py <source_directory> <destination_directory>")
        sys.exit(1)

    source_dir = os.path.join(sys.argv[1], "iPod_Control", "Music")
    dest_dir = sys.argv[2]

    logging.info(f"Source directory: {source_dir}")
    logging.info(f"Destination directory: {dest_dir}")
    
    copy_music_files(source_dir, dest_dir)