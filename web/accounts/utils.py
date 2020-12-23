import os

import requests

CLIENT_ID = os.getenv('CLIENT_ID')
CLIENT_SECRET = os.getenv('CLIENT_SECRET')
TWITCH_REDIRECT_URL = os.getenv('TWITCH_REDIRECT_URL')


def get_token_by_code(code):
    params = {
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET,
        'code': code,
        'grant_type': 'authorization_code',
        'redirect_uri': TWITCH_REDIRECT_URL,

    }
    url = "https://id.twitch.tv/oauth2/token"
    res = requests.post(url, params=params)
    token_data = res.json()
    access_token = token_data['access_token']
    refresh_token = token_data['refresh_token']
    expires_in = token_data['expires_in']
    return access_token, refresh_token, expires_in
