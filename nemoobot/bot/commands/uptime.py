from .command import Command
from bot.utils import decapi_uptime


class Uptime(Command):

    def match(self, bot, user, msg):
        cmd = msg.split(' ')[0]
        return cmd == '!uptime'

    def run(self, bot, user, msg):

        twitch_username = bot.channel.replace('#','')        
        time = decapi_uptime(twitch_username)            
        if twitch_username in time:
            bot.write(user + ' stream currently offline')
        else:
            bot.write(user + ' стрим онлайн уже ' + time)

