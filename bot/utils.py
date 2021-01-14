import requests

from datetime import datetime


API_BASE_URL = 'http://127.0.0.1:8000/api/v1/'


def load_user_settings():
    url = API_BASE_URL + 'settings/'
    res = requests.get(url)
    settings = res.json()

    settings_list = list()

    for user_settings in settings:
        user = user_settings['user']
        default_commands = user_settings['default_commands']
        custom_commands = user_settings['custom_commands']
        antispam_settings = user_settings['antispam']
        # add user settings to settings list
        settings_list.append((
            user, default_commands,
            custom_commands, antispam_settings
        ))

    return settings_list


def load_user_settings_by_channel_id(channel_id):
    url = API_BASE_URL + 'settings/'
    res = requests.get(url)
    settings = res.json()

    settings_list = list()

    for user_settings in settings:
        if settings['user']['twitch_user_id'] == channel_id:
<<<<<<< Updated upstream
            user = user_settings['user']
            default_commands = user_settings['default_commands']
            custom_commands = user_settings['custom_commands']
            antispam_settings = user_settings['antispam']
            # add user settings to settings list
            user_settings = (
                user, default_commands,
                custom_commands, antispam_settings
            )

    return user_settings
=======
            return user_settings
            
def stream_token(chanel_username):

    url = 'https://api.twitch.tv/helix/streams'

    token_url = 'https://id.twitch.tv/oauth2/token?client_id=cj6u5ko0kn9bpdgajxrbz5ircahgff&client_secret=jzf4gtifgl40sispkwhca2tfn4mtqc&grant_type=client_credentials'

    res = requests.post(token_url)
    data = res.json()
    token = data.get('access_token')

    headers = {
    'Authorization': f'Bearer {token}',
    'Client-ID': 'cj6u5ko0kn9bpdgajxrbz5ircahgff'
    }

    params = {
    'user_login': chanel_username
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
>>>>>>> Stashed changes
