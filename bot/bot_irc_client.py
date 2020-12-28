import os
from typing import List
from twisted.words.protocols import irc

from twitch_bot import TwitchBot


class BotIRCClient(irc.IRCClient):

    bots: List[TwitchBot] = []

    def __init__(self):
        self.username = os.getenv('BOT_NICKNAME')
        self.client_id = os.getenv('CLIENT_ID')
        self.password = os.getenv('BOT_AUTH_TOKEN')

    def signedOn(self):
        self.factory.wait_time = 1

        # self.sendLine("CAP REQ :twitch.tv/membership")
        # self.sendLine("CAP REQ :twitch.tv/commands")
        # self.sendLine("CAP REQ :twitch.tv/tags")

        for bot in self.bots:
            bot.irc = self
            self.join(bot.channel)
            self.joined(bot)

    def lineReceived(self, line):
        self.parse_line(line.decode('utf-8'))
        super().lineReceived(line)

    def parse_line(self, line):
        pass

    def privmsg(self, user, channel, message):
        user = user.rsplit('!', 1)[0]
        print(f"[{channel}] {user}: {message}")
        for bot in self.bots:
            if bot.channel == channel:
                bot.process_command(user, message)

    def joined(self, bot: TwitchBot):
        print(f"{self.username} connected to {bot.channel}")
        bot.write("Hello, there! I'm your TwitchBot")

    def userJoined(self, user, channel):
        for bot in self.bots:
            if f'#{bot.channel}' == channel:
                pass
