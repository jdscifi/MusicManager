import json
import re
import pandas as pd
import requests as rq
from bs4 import BeautifulSoup


def make_windows_filename(input_string, replacement='_'):
    # Remove invalid characters
    cleaned_string = re.sub(r'[\\/:*?"<>|]', replacement, input_string)

    # Remove leading and trailing whitespaces
    cleaned_string = cleaned_string.strip()

    # Ensure the filename is not empty after cleaning
    if not cleaned_string:
        cleaned_string = 'untitled'

    return cleaned_string


photo_anchors = {}

all_data = pd.DataFrame()

for x in range(1990, 2024):
    i = f"https://en.wikipedia.org/wiki/Billboard_Year-End_Hot_100_singles_of_{x}"
    try:
        data1 = pd.read_html(i)[0]
        if len(data1.columns) < 3:
            data1 = pd.read_html(i)[1]
        data1.columns = ["Rank", "Track", "Artist(s)"]
        data1["Year"] = [x] * len(data1)
        all_data = pd.concat([all_data, data1], ignore_index=True, sort=False)
        # all_data.append(data1, ignore_index=True)
        """resp = rq.get(i)
        if resp.status_code != 200:
            print(i, resp)
            continue
        print(i)
        soup = BeautifulSoup(resp.text, 'html.parser')
        div = soup.find('table')
        try:

            if anchor:
                img = div.find("img")
                if img:
                    img_down = rq.get(img["src0_4x"])
                    local_file_path = "allherluv_thumbnails/" + make_windows_filename(img['alt']) + ".jpg"
                    with open(local_file_path, 'wb') as file:
                         file.write(img_down.content)
                    photo_anchors[anchor['href']] = local_file_path
        except Exception as e:
            print(e)"""
    except Exception as e:
        print(data1)
        print(e, i)

# print(photo_anchors)

# Save the list of anchor links to a file
all_data.to_csv("billboard.tsv", sep="\t", index=False)
