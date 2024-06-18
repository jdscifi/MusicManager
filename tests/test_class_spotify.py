from src.spotify.class_spotify import Spotify
import pytest


def test_spotify_get_album():
    spobj = Spotify()
    obj = spobj.get_album_info("6NPpE0RmGDMnaxvB8xvXo6")
    print(obj)
    assert isinstance(obj, dict) is True


def test_spotify_get_track():
    spobj = Spotify()
    obj = spobj.get_track_info("5xU3g1Vtv1FXaKFn83NbDK")
    print(obj)
    assert isinstance(obj, dict) is True


def test_spotify_get_playlist():
    spobj = Spotify()
    obj = spobj.get_playlist_info("37i9dQZF1DXbVhgADFy3im")
    print(obj)
    assert isinstance(obj, dict) is True
