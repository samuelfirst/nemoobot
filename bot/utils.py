import requests

API_BASE_URL = 'http://127.0.0.1:8000/api/v1/'
API_SETTINGS_URL = API_BASE_URL + 'settings/'


def load_user_settings():
    url = API_SETTINGS_URL
    res = requests.get(url)
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
    url = API_SETTINGS_URL
    res = requests.get(url)
    settings = res.json()
    user_settings = []

    for user_settings in settings:
        if settings['user']['twitch_user_id'] == channel_id:
            return user_settings
