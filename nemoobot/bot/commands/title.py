from .command import Command
from bot.utils import stream_info, set_new_stream_title, channel_info


class Title(Command):
    def match(self, bot, user, msg):
        cmd = msg.split(' ')[0]
        return cmd == '!title'

    def run(self, bot, user, msg):

        token = bot.token
        twitch_username = bot.channel.replace('#', '')
        info = channel_info(str(bot.channel_id), token)

        if msg == '!title':
            title_info = info[0]['title']
            bot.write(f'{user} {title_info}')
        elif twitch_username == user:
            cmd, name = msg.split(' ', 1)
            set_new_stream_title(bot.channel_id, name, token)
            bot.write(f'{user} название стрима {name}')
        else:
            bot.write(f'{user} недостаточно прав')
