from .command import Command
from bot.utils import stream_info, time_manage


class Uptime(Command):

    def match(self, bot, user, msg):
        cmd = msg.split(' ')[0]
        return cmd == '!uptime'

    def run(self, bot, user, msg):

        twitch_username = f'{bot.channel}'
        twitch_username = twitch_username.replace('#', '')
        
        if stream_info(twitch_username) == [] :
            bot.write(user + ' Stream offline')
        else:
            streamstart = stream_info(twitch_username)[0]['started_at']    
            bot.write('Стрем идет - ' + time_manage(streamstart))
