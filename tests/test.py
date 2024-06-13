import os
import shutil


def move_music_files(source_directory, destination_directory):
    """
    Move music files to a higher level along with their corresponding album names.

    Parameters:
    - source_directory (str): The source directory containing the current structure.
    - destination_directory (str): The destination directory for the new structure.
    """
    for root, dirs, files in os.walk(source_directory):
        try:
            for album_name in dirs:
                try:
                    album_path = os.path.join(root, album_name)
                    album_path = os.path.join(album_path, album_name)
                    # album_path = os.path.join(album_path, album_name)

                    destination_path = os.path.join(destination_directory, album_name)

                    # Create the destination directory if it doesn't exist
                    os.makedirs(destination_path, exist_ok=True)

                    # Move music files to the destination directory
                    for file_name in os.listdir(album_path):
                        if True:
                            source_file_path = os.path.join(album_path, file_name)
                            destination_file_path = os.path.join(destination_path, file_name)

                            # Move the music file
                            shutil.copy(source_file_path, destination_file_path)
                except Exception:
                    print(album_name)
        except Exception:
            pass

# Example usage:
# source_directory = r'C:\Users\jaydu\Downloads\Telegram Desktop'
source_directory = r'C:\Users\jaydu\Downloads\Music'
destination_directory = r'C:\Users\jaydu\Downloads\Music2'

move_music_files(source_directory, destination_directory)
