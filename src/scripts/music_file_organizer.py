import os
from class_music import Music
import shutil
import re


def make_valid_directory_name(name):
    # Define the characters forbidden in Windows directory names
    forbidden_chars = r'[\\/:*?"<>|]'

    # Replace forbidden characters with an underscore
    valid_name = re.sub(forbidden_chars, ' ', name)

    return valid_name


def move_files(all_music_files):
    for path in all_music_files:
        try:
            file_path = os.path.join(path[0], path[1])
            mobj = Music(file_path)
            mobj.extract_music_metadata()
            if "album" not in mobj.music_info:
                print("Unable to extract album name for {}".format(file_path))
                continue

            music_album = make_valid_directory_name(mobj.music_info["album"])

            if music_album == "":
                print("Unable to extract album name for {}".format(file_path))
                continue
            if music_album in path[0]:
                print("File already at the expected path: {}".format(file_path))
                continue

            new_location = os.path.join(path[0], music_album)
            os.makedirs(new_location, exist_ok=True)
            shutil.move(file_path, new_location)
        except Exception as e:
            print(e)


def process_music_files_in_directory(directory):
    all_music_files = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.lower().endswith(('.mp3', '.flac', '.m4a', '.wav')):  # Add more formats if needed
                all_music_files.append((root, file))
            else:
                print("Unexpected file extension of file: {}".format(os.path.join(root, file)))

    move_files(all_music_files)


process_music_files_in_directory(r"J:\Downloads\Telegram Desktop")
