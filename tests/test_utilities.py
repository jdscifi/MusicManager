import pytest
from src.utils.utilties import *
import json


def test_delete_unwanted_key_from_json():
    with open(r"C:\Users\jaydu\AppData\Local\Temp\spotify\searches\spotify_search_24_06_18_19_58_47.log", "r") as fo:
        data = json.load(fo)
    data = delete_key_recursive(data, "available_markets")
    with open(r"C:\Users\jaydu\AppData\Local\Temp\spotify\searches\spotify_search_24_06_18_19_58_47.log", "w") as fo:
        fo.write(json.dumps(data, indent="\t"))
    assert ("available_markets" in data["tracks"]["items"][0]) is False
