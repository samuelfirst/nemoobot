import requests
from nemoobot.bot.config import CLIENT_ID, CLIENT_SECRET, BASE_DRF_API_URL

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


def channel_info(twitch_username_id, token):
    url = ' https://api.twitch.tv/helix/channels'
    headers = {
        'Authorization': f'Bearer {token}',
        'Client-Id': CLIENT_ID

    }
    params = {
        'broadcaster_id': twitch_username_id
    }
    res = requests.get(url, headers=headers, params=params)
    return res.json()['data']


def stream_info(twich_username_id):
    url = 'https://api.twitch.tv/helix/streams'
    token = get_app_access_token()
    headers = {
        'Authorization': f'Bearer {token}',
        'Client-Id': CLIENT_ID

    }
    params = {
        'user_id': twich_username_id
    }
    res = requests.get(url, headers=headers, params=params)
    return res.json()


def set_new_stream_game(channel_username, name_of_game, token):
    url = 'https://api.twitch.tv/helix/channels'
    headers = {
        'Authorization': f'Bearer {token}',
        'Client-Id': CLIENT_ID

    }
    params = {
        'broadcaster_id': channel_username,
        'game_id': name_of_game
    }
    res = requests.patch(url, headers=headers, params=params)
    return res


def get_game_id_by_game_name(game_name):
    url = 'https://api.twitch.tv/helix/games'
    token = get_app_access_token()
    headers = {
        'Authorization': f'Bearer {token}',
        'Client-Id': CLIENT_ID

    }
    params = {
        'name': game_name
    }
    res = requests.get(url, headers=headers, params=params)

    return res.json()['data']


def set_new_stream_title(channel_username, name_of_title, token):
    url = 'https://api.twitch.tv/helix/channels'
    headers = {
        'Authorization': f'Bearer {token}',
        'Client-Id': CLIENT_ID

    }
    params = {
        'broadcaster_id': channel_username,
        'title': name_of_title
    }

    res = requests.patch(url, headers=headers, params=params)
    return res