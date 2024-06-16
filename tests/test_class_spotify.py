from src.spotify.class_spotify import Spotify
import pytest


def test_spotify_search():
    sponj = Spotify()
    obj = sponj.search_by_keyword({"q": "Haule%20Haule", "type": "track"})
    print(obj.content)
    assert obj is not None
