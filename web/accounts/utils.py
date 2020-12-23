from django.conf import settings
import requests


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
    return access_token, refresh_token, expires_in
