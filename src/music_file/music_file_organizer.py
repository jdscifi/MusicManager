import os
from class_music import Music
import shutil

file_exts = []

albums = []


def process_music_files_in_directory(directory):
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.lower().endswith(('.mp3', '.flac', '.m4a', '.wav')):  # Add more formats if needed
                file_path = os.path.join(root, file)
                try:
                    mobj = Music(file_path)
                    # mobj.extract_file_info()
                    mobj.extract_music_metadata()
                    if mobj.music_info.album != "":
                        print(mobj.music_info.album.replace("(Original Motion Picture Soundtrack)", "").strip())
                        for i in ["[Original Soundtrack]", "(Original Motion Picture Soundtrack)", ":"]:
                            mobj.music_info.album = mobj.music_info.album.replace(i, "").strip()
                        albums.append(mobj.music_info.album)
                        # if mobj.music_info.album in file_path:
                        #    continue
                        directory = os.path.dirname(file_path)
                        if mobj.music_info.album in directory:
                            new_path = os.path.join(directory, '..')
                            new_path = os.path.normpath(new_path)
                            shutil.move(file_path, new_path)
                        else:
                            if not os.path.exists(os.path.join(root, mobj.music_info.album)):
                                os.mkdir(os.path.join(root, mobj.music_info.album))
                            shutil.move(file_path, os.path.join(root, mobj.music_info.album))
                    else:
                        print("################", file_path)
                    # mobj.display_music_info()
                    # mobj.add_to_db()
                except Exception as e:
                    print(e)
            else:
                file_exts.append(file.lower()[-4:])


process_music_files_in_directory(r"J:\Downloads\Telegram Desktop")
# process_music_files_in_directory(r"M:\Music\Music\Top 50 Bollywood Songs 2017 FLACs")

print(set(albums), len(set(albums)))
