from nemoobot.bot.commands import Command
from nemoobot.bot.utils import decapi_uptime


class Uptime(Command):
    def run(self, bot, user, msg):
        twitch_username = bot.channel.replace('#','')        
        time = decapi_uptime(twitch_username)            
        if twitch_username in time:
            bot.write(user + ' stream currently offline')
        else:
            bot.write(user + ' стрим онлайн уже ' + time)

