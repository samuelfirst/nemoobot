import requests

from .command import Command
from ..utils import stream_token, time_manage

class Uptime(Command):

    

    def match(self, bot, user, msg):
        cmd = msg.split(' ')[0]
        return cmd == '!uptime'

    def run(self, bot, user, msg):
        twitch_username = 'qrushcsgo'
        if stream_token(twitch_username) == [] :
            bot.write(user + ' Stream offline')
        else:
            streamstart = stream_token(twitch_username)[0]['started_at']    
            bot.write('Стрем идет - ' + time_manage(streamstart))
           
