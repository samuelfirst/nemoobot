import os
from dotenv import load_dotenv
from twisted.internet import reactor, protocol
from loguru import logger

from twitch_bot import TwitchBot
from bot_irc_client import BotIRCClient
from bot_ws_client import BotWebSocketClientFactory
from utils import load_user_settings

logger.add('logs/nemoobot.log', format="{time} {level} {message}", filter="__main__")


class BotFactory(protocol.ClientFactory):
    protocol = BotIRCClient

    def startedConnecting(self, connector):
        logger.info("Connection has been started.")

    def clientConnectionLost(self, connector, reason):
        logger.info("Connection lost. Reason: %s" % reason)
        connector.connect()

    def clientConnectionFailed(self, connector, reason):
        logger.debug("Connection failed. Reason: %s" % reason)


if __name__ == '__main__':
    project_folder = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    load_dotenv(os.path.join(project_folder, '.env.dev'))

    # create bot instances
    bots = list()
    for settings in load_user_settings():
        bot = TwitchBot(**settings)
        bots.append(bot)

    BotIRCClient.bots = bots
    BotIRCClient.ws_factory = BotWebSocketClientFactory()

    reactor.connectTCP('irc.chat.twitch.tv', 6667, BotFactory())
    reactor.run()
