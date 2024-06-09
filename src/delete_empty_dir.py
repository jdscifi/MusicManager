import os


def delete_directories_without_music_and_subdirs(root_directory):
    """
    Delete directories without music files and subdirectories inside the specified root directory.

    Parameters:
    - root_directory (str): The root directory to start the search.
    """
    for root, dirs, files in os.walk(root_directory, topdown=False):
        # Check if the current directory has no music files and no subdirectories
        if not dirs and not any(file.lower().endswith(('.mp3', '.flac', '.wav', '.m4a')) for file in files):
            try:
                # shutil.rmtree(root)
                print(f"dir /a /b \"{root}\"")
            except Exception as e:
                print(f"Error deleting directory {root}: {e}")


def delete_empty_directories(root_directory):
    """
    Delete empty directories inside the specified root directory.

    Parameters:
    - root_directory (str): The root directory to start the search.
    """
    for root, dirs, files in os.walk(root_directory):
        if not dirs and not files:
            # If there are no subdirectories and no files, delete the directory
            # os.rmdir(root)
            #
            print(f"dir /a /b \"{root}\"")


# Example usage:
root_directory = r'C:\Users\jaydu\Downloads\Telegram Desktop'
root_directory = r'M:\Music\Music'
# root_directory = r'D:\OSWALDEN'
delete_empty_directories(root_directory)
