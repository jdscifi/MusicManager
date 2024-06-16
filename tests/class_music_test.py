import os
from src.music_file.class_music import Music
import pytest

file_exts = []

"""def process_music_files_in_directory(directory):
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
"""


def test_flac_tag_collection():
    mobj = Music(r"J:\Downloads\Telegram Desktop\01 Satyanaas (From _Chandu Champion_).flac")
    wl = mobj.extract_music_metadata()
    mobj.display_music_info()
    assert len(mobj.music_info.keys()) != 0


def test_mp3_tag_collection():
    mobj = Music(r"J:\Downloads\38833FF26BA1D.UnigramPreview_g9c9v27vpyspw!App\Ahankaar (1995) Movie Mp3 Songs ["
                 r"SongsMp3\Rama-Rama-Poornima.mp3")
    wl = mobj.extract_music_metadata()
    mobj.display_music_info()
    assert len(mobj.music_info.keys()) != 0


def test_mp3_info_collection():
    mobj = Music(r"J:\Downloads\38833FF26BA1D.UnigramPreview_g9c9v27vpyspw!App\Ahankaar (1995) Movie Mp3 Songs ["
                 r"SongsMp3\Rama-Rama-Poornima.mp3")
    mobj.display_music_info()
    assert len(mobj.audio_quality_data.keys()) != 0
