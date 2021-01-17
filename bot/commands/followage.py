import requests
import pprint

from .command import Command
from ..utils import stream_info, time_manage, user_info, follow_time, follow_age 

class Followage(Command):

    def match(self, bot, user, msg):
        cmd = msg.split(' ')[0]
        return cmd == '!followage'

    def run(self, bot, user, msg):
        twitch_username = f'{bot.channel}'
        twitch_username = twitch_username.replace('#', '')
        
        user_info(user)
        
        user_id = user_info(user)[0]['id']
        streamer_id = user_info(twitch_username)[0]['id']
        
        follow_age(streamer_id, user_id)
        
        
        if follow_age(streamer_id, user_id) == [] :
            bot.write(user + ' ты не следишь за каналом')
        else: 
            followtime = follow_age(streamer_id, user_id)[0]['followed_at']
            bot.write(user + ' ты следишь за каналом уже  ' + follow_time(followtime) + ' дней!')    