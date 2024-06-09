import json
import pandas as pd

data = json.load(open("package.json", "r"))

tracks = []

for i in data["items"]:
    tracks.append(i['track'])

cols = ['album', 'artists', 'disc_number', 'track_number', 'duration_ms', 'external_ids', 'id', 'name', 'uri']

ko = pd.DataFrame(tracks)[cols]

print(ko)
# ko.to_csv("Best of Coke Studio Pakistan.tsv", sep="\t")
