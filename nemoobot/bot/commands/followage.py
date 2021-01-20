from .command import Command
from bot.utils import user_info, follow_time, follow_age


class FollowAge(Command):
    def match(self, bot, user, msg):
        cmd = msg.split(' ')[0]
        return cmd == '!followage'

    def run(self, bot, user, msg):

        if user == bot.channel.replace('#', ''):
            bot.write('Стример не следит за какналом.')
        else:
            user_id = user_info(user)[0]['id']
            streamer_id = bot.channel_id

            if not follow_age(streamer_id, user_id):
                bot.write(user + ' ты не следишь за каналом')
            else:
                followtime = follow_age(streamer_id, user_id)[0]['followed_at']
                bot.write(user + ' ты следишь за каналом уже  ' + follow_time(followtime) + ' дней!')
