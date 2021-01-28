from typing import List
from twisted.words.protocols import irc
from twisted.internet import reactor, threads, task
from loguru import logger

from bot.config import (
    BOT_NICKNAME, CLIENT_ID, BOT_AUTH_TOKEN,
    WS_HOST, WS_PORT
)
from bot.twitch_bot import TwitchBot


class BotIRCClient(irc.IRCClient):

    bots: List[TwitchBot] = []
    ws_factory = None
    is_started = False

    def __init__(self):
        self.username = BOT_NICKNAME
        self.client_id = CLIENT_ID
        self.password = BOT_AUTH_TOKEN
        # set irc attribute for websocket factory's protocol
        self.ws_factory.protocol.irc = self

    def signedOn(self):
        self.factory.wait_time = 1

        # self.sendLine("CAP REQ :twitch.tv/membership")
        self.sendLine("CAP REQ :twitch.tv/commands")
        # self.sendLine("CAP REQ :twitch.tv/tags")

        for bot in self.bots:
            self.join_bot_channel(bot)

        # connect to websocket
        if self.ws_factory is not None:
            reactor.connectTCP(WS_HOST, WS_PORT, self.ws_factory)

    def lineReceived(self, line):
        self.parse_line(line.decode('utf-8'))
        super().lineReceived(line)

    def parse_line(self, line):
        pass

    def privmsg(self, user, channel, message):
        user = user.rsplit('!', 1)[0]
        logger.info(f"[{channel}] {user}: {message}")
        for bot in self.bots:
            if bot.channel == channel:
                if bot.antispam.is_active:
                    bot.antispam_check(user, message)
                bot.process_command(user, message)

    def joined(self, bot: TwitchBot):
        logger.info(f"Bot [{self.username}] connected to chat channel [{bot.channel}]")

    def userJoined(self, user, channel):
        for bot in self.bots:
            if f'#{bot.channel}' == channel:
                pass

    def join_bot_channel(self, bot):
        bot.irc = self
        self.join(bot.channel)
        self.joined(bot)

    def add_bot(self, bot):
        self.bots.append(bot)
        self.join_bot_channel(bot)

    def delete_bot(self, delete_bot):
        for bot in self.bots:
            # get bot instance to delete
            if bot.channel_id == delete_bot.channel_id:
                i = self.bots.index(bot)
                # remove bot from bots list
                self.bots.pop(i)
                # leave the channel
                self.leave(bot.channel)
                logger.info(f'Bot leave {bot.channel}!')

    def reload_bot(self, args):
        for bot in self.bots:
            if bot.channel_id == args['user']['twitch_user_id']:
                bot.reload(**args)
                logger.info(f'Bot in {bot.channel} was reloaded!')
