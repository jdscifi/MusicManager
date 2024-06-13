import os
import re

class MusicTagEditor:

    def __init__(self, path):
        pass

    def remove_substring_from_nfo(self, file_path, substring):
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()

        # Remove the specified substring from the content
        new_content = re.sub(re.escape(substring), '', content, flags=re.IGNORECASE)
        new_content = new_content.replace("<lockdata>false</lockdata>", "<lockdata>true</lockdata>")

        # Write the modified content back to the file
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(new_content)

    def process_nfo_files(self, directory_path, substring):
        for root, dirs, files in os.walk(directory_path):
            for file_name in files:
                file_path = os.path.join(root, file_name)

                # Check if the file is an NFO file
                if file_name.lower().endswith('.nfo'):
                    self.remove_substring_from_nfo(file_path, substring)
                    print(f"Processed: {file_path}")

                if file_name.lower().endswith(('.flac', '.wav')):
                    # Extract the title without the specified substring
                    new_title = re.sub(re.escape(substring), '', os.path.splitext(file_name)[0], flags=re.IGNORECASE)

                    # Create the new file name
                    new_file_name = f"{new_title}{os.path.splitext(file_name)[1]}"

                    # Create the new file path
                    new_file_path = os.path.join(root, new_file_name)

                    # Rename the file
                    os.rename(file_path, new_file_path)

                    print(f"Renamed: {file_name} -> {new_file_name}")