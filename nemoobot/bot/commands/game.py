from .command import Command
from bot.utils import (
    stream_info, set_new_stream_game,
    get_game_id_by_game_name, channel_info
)


class Game(Command):
    def match(self, bot, user, msg):
        cmd = msg.split(' ')[0]
        return cmd == '!game'

    def run(self, bot, user, msg):

        twitch_username = bot.channel.replace('#', '')
        info = channel_info(str(bot.channel_id), bot.token)

        if msg == '!game':
            game_info = info[0]['game_name']
            bot.write(f'{user} текущая игра {game_info}')
        elif twitch_username == user:
            cmd, name = msg.split(' ', 1)
            game_id = get_game_id_by_game_name(name)[0]['id']
            set_new_stream_game(
                bot.channel_id,
                game_id,
                bot.token
            )
            bot.write(f'{user} поменял игру на {name}')
        else:
            bot.write(f'{user} недостаточно прав')