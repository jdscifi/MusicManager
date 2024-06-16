import time
import warnings

import requests as rq
import os
import logging as lg


class Spotify:
    def __init__(self):

        self.access_token = "BQDlkcj33OkjuVtfZbTC6LnJIZQmwDNaQZ2CmtUBrLiqOKI8_I0gg_o_OFQhTv3HkxgbVQoTcQUpkEeMe1gt8vuY_KwoHeZdoJW5okoPRJ8MiwuH8gE"
        lg.basicConfig(filename="spotify_class.log",
                       format='%(asctime)s %(message)s',
                       filemode='a')
        self.logger = lg.Logger("spotify_logger")
        self.headers = None
        self.CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID")
        self.CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET")
        self.BASE_URL = 'https://api.spotify.com/v1/'
        self.get_access_token()
        self.headers = {
            'Authorization': 'Bearer {token}'.format(token=self.access_token)
        }
        print(self.headers)

    def get_access_token(self):
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

    def search_by_keyword(self, param):
        try:
            print(param)
            track_info = rq.get(
                    'https://api.spotify.com/v1/search',
                    headers=self.headers,
                    params=param
                )
            if track_info.status_code == 429:
                warnings.warn("Spotify API limit reached! Waiting for 60 seconds....")
                time.sleep(60)

            print(track_info)

            if track_info.status_code != 200:
                return False

            return track_info
        except Exception:
            self.logger.error("Error when searching for {}".format(str(param)), exc_info=True)

    def get_album_info(self):
        pass

    def get_track_info(self):
        pass
