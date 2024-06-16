import os, json
import mutagen
from mutagen.easyid3 import EasyID3
from mutagen.mp3 import MP3, EasyMP3
from mutagen.flac import FLAC
from mutagen.wave import WAVE
from mutagen.mp4 import MP4
import wave
from mutagen import File
from dataclasses import dataclass
from src.utils.db_manager import DBManager
from src.spotify.class_spotify import Spotify
from pathlib import Path
import logging as lg
import warnings


class Music:
    def __init__(self, file_path, extension=None):
        lg.basicConfig(filename="music_class.log",
                       format='%(asctime)s %(message)s',
                       filemode='a')
        self.logger = lg.Logger("music_logger")
        with open("config.json", "r") as fi:
            self.config = json.load(fi)

        if not os.path.exists(file_path):
            self.logger.error("File Not Found! Info: \n File: {}".format(file_path))
            raise FileNotFoundError("No such file found: {}".format(file_path))

        self.dbobj = DBManager()
        self.audio_file = None
        self.music_info = {}
        self.audio = None
        self.audio_info = None
        self.extension = extension if extension else file_path.lower()[-4:].replace(".", "")
        if self.extension not in ['mp3', 'flac', 'm4a', 'wav']:
            self.logger.error("Unsupported file! Info: \n File: {} \n Extension: {}".format(file_path, extension))
            raise ValueError("Invalid File")
        self.audio_quality_data = {}
        self.read_file(file_path)

    def read_file(self, file_path):
        try:
            if self.extension == 'mp3':
                self.audio = EasyMP3(file_path)
                self.audio_info = MP3(file_path)
            elif self.extension == 'flac':
                self.audio = FLAC(file_path)
                self.audio_info = self.audio
            elif self.extension == 'm4a':
                self.audio = MP4(file_path)
                self.audio_info = self.audio
            elif self.extension == "wav":
                self.audio = WAVE(file_path)
                self.audio_info = self.audio
            else:
                raise ValueError("Unknown file type: {}".format(file_path))
        except Exception as e:
            print("Error reading music file: {}".format(file_path))

    @staticmethod
    def windows_path_to_posix_relative(windows_path, start_directory='Music'):
        """
        Convert a Windows path to a relative POSIX path starting from a specified directory.

        Parameters:
        - windows_path (str): The Windows path.
        - start_directory (str): The directory from which the relative path should start. Default is 'Documents'.

        Returns:
        - str: The relative POSIX path.
        """
        # Convert Windows path to a Path object
        path_object = Path(windows_path)

        # Find the index of the start directory
        start_index = path_object.parts.index(start_directory)

        # Get the relative path from the start directory
        relative_path = Path(*path_object.parts[start_index:]).as_posix()

        return relative_path

    def extract_m4a_data(self):
        for key, value in self.config["m4a_tag_map"].items():
            self.music_info[key] = self.audio.get(value)

    def extract_music_metadata(self):
        if not self.audio:
            return None
        if "m4a" in self.extension:
            self.extract_m4a_data()
        elif "flac" in self.extension:
            self.music_info = dict([(x[0].lower, x[1]) for x in self.audio.tags])
        elif "mp3" in self.extension:
            mp3_data = self.audio.tags  # dict([(x[0].lower, x[1]) for x in self.audio_info.tags])
            if isinstance(mp3_data, mutagen.easyid3.EasyID3):
                mp3_data = dict(mp3_data)
                for key in mp3_data.keys():
                    if isinstance(mp3_data[key], list) and len(mp3_data[key]) == 1:
                        mp3_data[key] = mp3_data[key][0]
            self.music_info = mp3_data

    def extract_file_info(self):
        if not self.audio:
            return None
        if "m4a" in self.extension:
            self.audio_quality_data = dict(self.audio.info)
        elif "flac" in self.extension:
            self.audio_quality_data = dict(self.audio.info)
        elif "mp3" in self.extension:
            mp3_data = self.audio_info.info  # dict([(x[0].lower, x[1]) for x in self.audio_info.tags])
            if isinstance(mp3_data, mutagen.easyid3.EasyID3):
                mp3_data = dict(mp3_data)
                for key in mp3_data.keys():
                    if isinstance(mp3_data[key], list) and len(mp3_data[key]) == 1:
                        mp3_data[key] = mp3_data[key][0]
            self.audio_quality_data = mp3_data
        if "wav" in self.extension:
            self.audio_quality_data = dict(self.audio.info)

    def embed_tag(self, values_to_update: dict) -> object:
        if self.extension == "wav":
            warnings.warn("Cannot perform action on file type: WAV")
            return True
        for tag, value in values_to_update.items():
            if not all([tag, value]):
                continue
            self.audio[tag] = value
        self.audio.save()

    def display_music_info(self):
        print(self.music_info)
        print(self.audio_quality_data)

    def clean_up_bad_tags_values(self):
        if self.extension == "wav":
            warnings.warn("Cannot perform action on file type: WAV")
            return True
        for tag in self.config["blacklisted_tags"]:
            if tag in self.music_info:
                self.audio.pop(tag)
        self.audio.save()

    def refresh_tags(self, update_from_spotify=False):
        if self.extension == "wav":
            warnings.warn("Cannot perform action on file type: WAV")
            return True
        self.clean_up_bad_tags_values()
        if update_from_spotify:
            new_tags = self.find_tags_from_spotify()
            if any([x in self.config["expected_tags"] for x in new_tags]):
                self.embed_tag(new_tags)

    def find_tags_from_spotify(self):
        spobj = Spotify()
        return spobj.search_track(self.music_info["title"])
