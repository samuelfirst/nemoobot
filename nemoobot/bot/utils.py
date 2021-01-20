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


def stream_info(channel_username):

    url = 'https://api.twitch.tv/helix/streams'
    token = get_app_access_token()
    headers = {
        'Authorization': f'Bearer {token}',
        'Client-ID': CLIENT_ID
    }
    params = {
        'user_login': channel_username
    }
    res = requests.get(url, headers=headers, params=params)
    json_response = res.json()['data'] 
    return json_response


def time_manage(stream_start):
    now = datetime.utcnow()
    for ch in ["-", "T", "Z", ":"]:
        stream_start = stream_start.replace(ch, "")

    stream_start = datetime.strptime(stream_start, "%Y%m%d%H%M%S")
    elapsed_time = now - stream_start
    seconds = int(elapsed_time.total_seconds())

    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    seconds = seconds % 60
    
    var = str(hours) + ':' + str(minutes) + ':' + str(seconds)
    return var


def user_info(user_username):
    url = 'https://api.twitch.tv/helix/users'
    token = get_app_access_token()
    headers = {
        'Authorization': f'Bearer {token}',
        'Client-ID': CLIENT_ID
    }
    params = {
        'login': user_username
    }

    res = requests.get(url, headers=headers, params=params)
    json_response = res.json()['data'] 
    return json_response


def follow_age(streamer, follower):
    url = 'https://api.twitch.tv/helix/users/follows?'
    token = get_app_access_token()
    headers = {
        'Authorization': f'Bearer {token}',
        'Client-ID': 'cj6u5ko0kn9bpdgajxrbz5ircahgff'
    }

    params = {
        'from_id': follower,
        'to_id': streamer
    }

    res = requests.get(url, headers=headers, params=params)
    json_follow = res.json()['data']
    
    return json_follow


def follow_time(startfollow):
    now = datetime.now()

    for ch in ["-", "T", "Z", ":"]:
        startfollow = startfollow.replace(ch, "")

    startfollow = datetime.strptime(startfollow, "%Y%m%d%H%M%S")
    diff = now - startfollow
    diff = str(diff)

    x = diff.split()

    days = x[0]
    return days
