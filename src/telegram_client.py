import os, json
from telethon import TelegramClient, sync
from telethon.tl.types import InputMessagesFilterPhotos, InputMessagesFilterMusic, InputPeerEmpty
from time import time
from telethon.tl.functions.contacts import SearchRequest
from telethon.tl.functions.messages import SearchGlobalRequest
import datetime
from telethon.errors.rpcerrorlist import FolderIdInvalidError

class Telegram():
    TELEGRAM_APP_ID = None
    TELEGRAM_API_HASH = None
    TELEGRAM_CHANNEL_USERNAME = None

    def __init__(self):
        with open(r"J:\dev\telegram.config","r") as file:
            creds = json.load(file)
            self.TELEGRAM_APP_ID = creds["TELEGRAM_APP_ID"]
            self.TELEGRAM_API_HASH = creds["TELEGRAM_API_HASH"]
            self.TELEGRAM_CHANNEL_USERNAME = creds["TELEGRAM_CHANNEL_USERNAME"]
        # Create the client and connect
        self.client = TelegramClient(
            'Default_Session_{}'.format(time()),
            self.TELEGRAM_APP_ID,
            self.TELEGRAM_API_HASH
        )
        self.client.start()

    # Function to download media
    def download_media(self, channel, limit=10, media_filter=InputMessagesFilterPhotos):
        messages = self.client.get_messages(channel, limit=limit, filter=media_filter)
        for msg in messages:
            if msg.media:
                filename = msg.download_media()
                print(f'Downloaded {filename}')

    def search_messages(self, keyword):
        try:
            results = self.client(
                SearchGlobalRequest(
                    q=keyword,
                    filter=InputMessagesFilterMusic(),
                    min_date=datetime.datetime(2022, 6, 25),
                    max_date=datetime.datetime(2024, 6, 25),
                    offset_rate=42,
                    offset_peer=InputPeerEmpty(),
                    offset_id=42,
                    limit=100,
                    broadcasts_only=None,
                    folder_id=None
                )
            )
            print(results)
        except FolderIdInvalidError as e:
            pass
        except Exception as err:
            print(err)
            self.client.disconnect()

    def __del__(self):
        # Disconnect the client
        self.client.disconnect()


obj = Telegram()
obj.search_messages("fukrey")
