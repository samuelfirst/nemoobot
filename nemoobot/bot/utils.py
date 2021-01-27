import requests
from datetime import datetime
from bot.config import CLIENT_ID, CLIENT_SECRET, BASE_DRF_API_URL

API_SETTINGS_URL = BASE_DRF_API_URL + 'settings/'

APP_ACCESS_TOKEN_URL = f'https://id.twitch.tv/oauth2/token?client_id={CLIENT_ID}&client_secret={CLIENT_SECRET}&grant_type=client_credentials'


def load_user_settings():
    res = requests.get(API_SETTINGS_URL)
    settings = res.json()

    settings_list = list()

    try:
        for user_settings in settings:
            # add user settings to settings list
            settings_list.append(user_settings)
    except:
        pass

    return settings_list


def load_user_settings_by_channel_id(channel_id):

    res = requests.get(API_SETTINGS_URL)
    settings = res.json()

    for user_settings in settings:
        if settings['user']['twitch_user_id'] == channel_id:
            return user_settings


def get_app_access_token():
    res = requests.post(APP_ACCESS_TOKEN_URL)
    data = res.json()
    app_access_token = data.get('access_token')
    return app_access_token


def decapi_followage(channel_username, user_username):

    url = 'https://decapi.me/twitch/followage'
    
    params = {
        'channel': channel_username,
        'user': user_username,
        'lang': 'ru'
    }

    res = requests.get(url, params=params)
    return res.text


def decapi_uptime(channel_username):
    
    url = 'https://decapi.me/twitch/uptime'
    
    params = {
        'channel': channel_username,
        'lang': 'ru'
    }

    res = requests.get(url, params=params)
    return res.text
