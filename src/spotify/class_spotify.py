import json
import time
import warnings
from datetime import datetime
import requests as rq
import os
import logging as lg
import tempfile
from src.utils.utilties import delete_key_recursive

class Spotify:
    def __init__(self):
        self.access_token = ""
        lg.basicConfig(filename="spotify_class.log",
                       format='%(asctime)s %(message)s',
                       filemode='a')
        self.logger = lg.Logger("spotify_logger")
        self.tmp_dir = os.path.join(tempfile.gettempdir(), "spotify")
        self.headers = None
        self.CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID")
        self.CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET")
        self.BASE_URL = 'https://api.spotify.com/v1/{}/{}'
        self.get_access_token()
        self.headers = {
            'Authorization': 'Bearer {token}'.format(token=self.access_token)
        }
        print(self.headers)

    def get_access_token(self):
        token_cache_file = os.path.join(self.tmp_dir, "token_data")

        if os.path.exists(token_cache_file):
            with open(token_cache_file, "r") as tok_fil:
                token_data = json.load(tok_fil)
                if int(token_data["timestamp"]) > (int(datetime.timestamp(datetime.now())) - 3600):
                    print("Using valid token available offline......")
                    self.access_token = token_data["token"]
                    return True

        AUTH_URL = 'https://accounts.spotify.com/api/token'

        auth_response = rq.post(AUTH_URL, {
            'grant_type': 'client_credentials',
            'client_id': self.CLIENT_ID,
            'client_secret': self.CLIENT_SECRET,
        })

        # convert the response to JSON
        auth_response_data = auth_response.json()
        # save the access token
        self.access_token = auth_response_data['access_token']

        if not os.path.exists(self.tmp_dir):
            os.mkdir(self.tmp_dir)
        token_data = {
            "timestamp": datetime.timestamp(datetime.now()),
            "token": self.access_token
        }

        with open(token_cache_file, "w") as tok_fil:
            tok_fil.write(json.dumps(token_data))

        print("Token saved at {}".format(token_cache_file))

    def save_search(self, results):
        try:
            spotify_search_tmp_dir = os.path.join(self.tmp_dir, "searches")
            if not os.path.exists(self.tmp_dir):
                os.mkdir(self.tmp_dir)
            if not os.path.exists(spotify_search_tmp_dir):
                os.mkdir(spotify_search_tmp_dir)

            search_file_name = os.path.join(spotify_search_tmp_dir,
                                            datetime.now().strftime('spotify_search_%y_%m_%d_%H_%M_%S.log'))
            if os.path.exists(search_file_name):
                search_file_name.replace("spotify_search_", "spotify_search_2_")
            if isinstance(results, dict):
                results = json.dumps(results, indent="\t")

            with open(search_file_name, "w") as file_obj:
                file_obj.write(str(results))

            print("Saved search at : {}".format(search_file_name))
        except Exception as e:
            print(e)

    def make_a_request(self, request_uri, param=None):
        try:
            if param:
                search_results = rq.get(
                    request_uri,
                    headers=self.headers,
                    params=param
                )
            else:
                search_results = rq.get(
                    request_uri,
                    headers=self.headers
                )

            if search_results.status_code == 429:
                warnings.warn("Spotify API limit reached! Waiting for 60 seconds....")
                time.sleep(60)

            if search_results.status_code != 200:
                return False
            search_json = json.loads(search_results.text)

            delete_key_recursive(search_json, "available_markets")

            self.save_search(search_json)
            return search_json

        except Exception:
            self.logger.error("Error when searching for {}".format(str(param)), exc_info=True)
            return False

        pass

    def search_by_keyword(self, param):
        request_uri = self.BASE_URL.format("search", "")
        result = self.make_a_request(request_uri, param)
        return result

    def get_album_info(self, album_id):
        if isinstance(album_id, list):
            album_id = ",".join([x.strip() for x in album_id])
        request_uri = self.BASE_URL.format("albums", album_id)
        results = self.make_a_request(request_uri)
        return results

    def get_track_info(self, track_id):
        if isinstance(track_id, list):
            track_id = ",".join([x.strip() for x in track_id])
        request_uri = self.BASE_URL.format("tracks", track_id)
        results = self.make_a_request(request_uri)
        return results

    def get_playlist_info(self, playlist_id):
        request_uri = self.BASE_URL.format("playlists", playlist_id)
        results = self.make_a_request(request_uri)
        return results
