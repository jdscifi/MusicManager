import os
from class_music import Music

file_exts = []


def process_music_files_in_directory(directory):
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.lower().endswith(('.mp3', '.flac', '.m4a', '.wav')):  # Add more formats if needed
                file_path = os.path.join(root, file)
                try:
                    mobj = Music(file_path)
                    mobj.extract_file_info()
                    mobj.extract_music_metadata()
                    # mobj.display_music_info()
                    mobj.add_to_db()
                except Exception as e:
                    print(e)
            else:
                file_exts.append(file.lower()[-4:])


# Replace 'your_music_directory' with the path to your music directory
process_music_files_in_directory(r"M:\Music\Music")
# process_music_files_in_directory(r"C:\Users\jaydu\Downloads\Music")
# process_music_files_in_directory(r"M:\Music\Music\Bareily ki Barfi")
# process_music_files_in_directory(r'U:\\')


print(set(file_exts))
