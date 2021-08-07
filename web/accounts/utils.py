import time

import requests
from django.conf import settings
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer


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
    url = f'{settings.BASE_API_URL}settings/{settings_id}'
    res = requests.get(url)
    return res.json()


def get_list_user_settings():
    url = f'{settings.BASE_API_URL}settings/'
    res = requests.get(url)
    return res.json()


def send_message_to_ws(message):
    print('sending message to ws')
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)("bot_commands", message)


def get_app_token():
    params = {
        'client_id': settings.TWITCH_CLIENT_ID,
        'client_secret': settings.TWITCH_CLIENT_SECRET,
        'grant_type': 'client_credentials',

    }
    url = "https://id.twitch.tv/oauth2/token"
    res = requests.post(url, params=params)
    token_data = res.json()
    access_token = token_data['access_token']
    expires_in = token_data['expires_in']
    expires_time = expires_in + int(time.time())
    return access_token, expires_in, expires_time
