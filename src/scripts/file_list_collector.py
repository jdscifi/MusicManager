import os
from src.music_file.class_music import Music
import pandas as pd

unexpected_file_extension = []


def collect_file_data(file_path):
    mobj = Music(file_path)
    mobj.extract_music_metadata()
    mobj.music_info["file_path"] = file_path
    mobj.music_info["audio_quality_data"] = mobj.audio_quality_data
    # print(mobj.music_info)

    return mobj.music_info


def process_music_files_in_directory(directory):
    all_data = []
    rbc = ""
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.lower().endswith(('.mp3', '.flac', '.m4a', '.wav')):
                if rbc != root:
                    rbc = root
                    print(f"Now reading {root}")
                all_data.append(collect_file_data(os.path.join(root, file)))
            else:
                unexpected_file_extension.append(os.path.join(root, file))
    try:
        music_df = pd.DataFrame(all_data)
        music_df.to_csv(r"D:\Documents\MM\all_music_data.tsv", sep="\t")

    except Exception as e:
        print(e)
    print("{} music files found!".format(len(all_data)))


process_music_files_in_directory(r"M:\Music\Music")
