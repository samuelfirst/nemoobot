import requests

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
