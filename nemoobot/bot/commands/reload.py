import os
import requests
from nemoobot.bot.commands import Command


class Reload(Command):
    API_BASE_URL = os.getenv('API_BASE_URL')

    def load_user_settings_by_channel_id(self, channel_id):
        url = self.API_BASE_URL + 'settings/'
        res = requests.get(url)
        
        settings = res.json()
        settings_list = list()
        for user_settings in settings:
            if user_settings['user']['twitch_user_id'] == channel_id:
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

    def run(self, bot, user, msg):
        user_settings = self.load_user_settings_by_channel_id(bot.channel_id)
        bot.reload(*user_settings)
        