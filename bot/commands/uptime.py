import requests

from .command import Command


class Uptime(Command):

    def match(self, bot, user, msg):
        cmd = msg.split(' ')[0]
        return cmd == '!uptime'

    def run(self, bot, user, msg):
        # command logic here
        bot.write('uptime command')
