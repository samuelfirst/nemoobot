import time
import asyncio
import requests
import websockets
from django.conf import settings


def get_token_by_code(code):
    params = {
        'client_id': settings.TWITCH_CLIENT_ID,
        'client_secret': settings.TWITCH_CLIENT_SECRET,
        'code': code,
        'grant_type': 'authorization_code',
        'redirect_uri': settings.TWITCH_REDIRECT_URL,

    }
    url = "https://id.twitch.tv/oauth2/token"
    res = requests.post(url, params=params)
    token_data = res.json()
    access_token = token_data['access_token']
    refresh_token = token_data['refresh_token']
    expires_in = token_data['expires_in']
    expires_time = expires_in + int(time.time())
    return access_token, refresh_token, expires_in, expires_time


def get_user_settings_by_id(settings_id):
    url = f'http://localhost:8000/api/v1/settings/{settings_id}'
    res = requests.get(url)
    return res.json()


def send_message_to_ws(message):
    asyncio.get_event_loop().run_until_complete(send_message(message))


async def send_message(message):
    uri = 'ws://localhost:8000'
    async with websockets.connect(uri) as sock:
        await sock.send(message)
