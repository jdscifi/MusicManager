import os
from mutagen.easyid3 import EasyID3
from mutagen.mp3 import MP3
from mutagen.flac import FLAC
from mutagen.wavpack import WavPack
from mutagen.mp4 import MP4
import wave
from mutagen import File
from dataclasses import dataclass
from src.utils.db_manager import DBManager
from pathlib import Path
import logging as lg


@dataclass
class MusicInfo:
    year: int = 1970
    genre: str = ""
    artist: str = ""
    album: str = ""
    title: str = ""
    isrc: str = ""
    spotify_id: str = ""
    file_path: str = ""

    def to_dict(self):
        return {key: value for key, value in vars(self).items()}

    def display_info(self):
        print({key: value for key, value in vars(self).items()})


@dataclass
class FileInfo:
    duration: int = 0
    audio_codec: str = ""
    frames: int = ""
    frame_rate: float = 0.0
    channels: str = ""
    sample_width: str = ""
    bitrate: float = 0
    file_path: str = ""
    file_type: str = ""
    isrc: str = ""
    spotify_id: str = ""

    def to_dict(self):
        return {key: value for key, value in vars(self).items()}

    def display_info(self):
        print({key: value for key, value in vars(self).items()})


class Music:
    def __init__(self, file_path, extension=None):
        lg.basicConfig(filename="music_class.log",
                       format='%(asctime)s %(message)s',
                       filemode='a')
        self.logger = lg.Logger()

        if not os.path.exists(file_path):
            self.logger.error("File Not Found! Info: \n File: {}".format(file_path))
            raise FileNotFoundError("No such file found: {}".format(file_path))

        self.dbobj = DBManager()
        self.audio_file = None
        self.music_info = None
        self.audio = None
        self.audio_info = None
        extension = extension if extension else file_path.lower()[-4:].replace(".", "")

        if extension not in ['mp3', 'flac', 'm4a', 'wav']:
            self.logger.error("Unsupported file! Info: \n File: {} \n Extension: {}".format(file_path, extension))
            raise ValueError("Invalid File")

        self.file_info = FileInfo(file_path=file_path, file_type=extension)
        self.read_file(extension, file_path)

    def read_file(self, extension, file_path):
        try:
            if extension == 'mp3':
                self.audio = EasyID3(file_path)
                self.audio_info = MP3(file_path)
            elif extension == 'flac':
                self.audio = FLAC(file_path)
                self.audio_info = self.audio
            elif extension == 'm4a':
                self.audio = MP4(file_path)
                self.audio_info = self.audio
            elif extension == "wav":
                pass
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

    def extract_music_metadata(self):
        self.music_info = MusicInfo(file_path=self.file_info.file_path)
        if self.audio:
            self.music_info.title = self.audio.get('title', [''])[0]
            self.music_info.artist = self.audio.get('artist', [''])[0]
            self.music_info.album = self.audio.get('album', [''])[0]
            self.music_info.genre = self.audio.get('genre', [''])[0]
            self.music_info.year = self.audio.get('date', [''])[0]
            try:
                self.file_info.isrc = self.music_info.isrc = self.audio.get('isrc', [''])[0]
            except Exception as e:
                print(self.file_info.file_path, e)
        else:
            self.music_info.title = os.path.basename(self.file_info.file_path)[:-4].replace(".", " ").strip()
        if isinstance(self.audio, MP4) and self.music_info.album == "":
            self.music_info.album = self.audio.get('\xa9alb', [''])[0]

    def extract_file_info(self):
        if self.audio_info:
            self.file_info.bitrate = self.audio_info.info.bitrate // 1000
            self.file_info.duration = self.audio_info.info.length if self.audio_info else 0
        if self.file_info.file_type in ['mp3', 'flac', 'wav', 'm4a']:
            self.audio_file = File(self.file_info.file_path)
            try:
                self.file_info.audio_codec = self.audio_file.info.codec_name if self.audio_file and self.audio_file.info else ""
            except:
                self.file_info.audio_codec = ""

        if self.file_info.file_type == "wav":
            try:
                with wave.open(self.file_info.file_path, 'rb') as audio_file:
                    self.file_info.channels = audio_file.getnchannels()
                    self.file_info.sample_width = audio_file.getsampwidth()
                    self.file_info.frame_rate = audio_file.getframerate()
                    self.file_info.frames = audio_file.getnframes()
            except Exception as e:
                print("Wav file read error!:", e)

    def embed_tag(self, tag, value):
        try:
            if tag and value:
                self.audio[tag] = value
                self.audio.save()
        except Exception as e:
            print("Unable to set tag {}:{}".format(tag, value))

    def display_music_info(self):
        self.music_info.display_info()
        self.file_info.display_info()

    def add_file_to_db(self):
        self.dbobj.insert_record("file_info", self.file_info.to_dict())

    def add_music_info_to_db(self):
        self.dbobj.insert_record("music_info", self.music_info.to_dict())

    def add_to_db(self):
        try:
            self.file_info.file_path = self.windows_path_to_posix_relative(self.file_info.file_path)
            self.music_info.file_path = self.file_info.file_path
            self.add_music_info_to_db()
        except Exception as e:
            print("Music info table not updated", self.file_info.file_path, e)
        try:
            self.add_file_to_db()
        except Exception as e:
            print("File info table not updated", self.file_info.file_path, e)
