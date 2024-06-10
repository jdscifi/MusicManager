import os
from telethon import TelegramClient, sync
from telethon.tl.types import InputMessagesFilterPhotos, InputMessagesFilterVideo

# Replace these with your own values
api_id = 'YOUR_API_ID'
api_hash = 'YOUR_API_HASH'
channel_username = 'your_channel_username'

# Create the client and connect
client = TelegramClient('session_name', api_id, api_hash)
client.start()

# Function to download media
def download_media(channel, limit=10, media_filter=InputMessagesFilterPhotos):
    messages = client.get_messages(channel, limit=limit, filter=media_filter)
    for msg in messages:
        if msg.media:
            filename = msg.download_media()
            print(f'Downloaded {filename}')

# Replace 'limit' with the number of media files you want to download
# You can also change InputMessagesFilterPhotos to InputMessagesFilterVideo to download videos
download_media(channel_username, limit=10, media_filter=InputMessagesFilterPhotos)

# You can add more media filters or extend the function to handle different media types
download_media(channel_username, limit=10, media_filter=InputMessagesFilterVideo)

# Disconnect the client
client.disconnect()
