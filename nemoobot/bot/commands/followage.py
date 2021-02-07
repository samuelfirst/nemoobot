from .command import Command
from bot.utils import decapi_followage

class FollowAge(Command):
    def match(self, bot, user, msg):
        cmd = msg.split(' ')[0]
        return cmd == '!followage'

    def run(self, bot, user, msg):

        twitch_username = bot.channel.replace('#','')
        follow = decapi_followage(twitch_username,user)
        if 'Follow not found' in follow:
            bot.write(user + ' ты не подписан!')
        elif twitch_username == user:
            bot.write('Сам на себя не подпишешься, никто не подпишется')
        else:
            bot.write(user + ' ты следишь за каналом уже ' + follow)
