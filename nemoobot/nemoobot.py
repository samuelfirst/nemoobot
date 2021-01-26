from twisted.internet import reactor, protocol
from loguru import logger

from bot.twitch_bot import TwitchBot
from bot.bot_irc_client import BotIRCClient
from bot.bot_ws_client import BotWebSocketClientFactory
from bot.utils import load_user_settings

logger.add('logs/nemoobot_logs.log', enqueue=True, format="{time} {level} | {module:<15} | {message}", level="DEBUG")


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

    # create bot instances
    bots = list()
    for settings in load_user_settings():
        bot = TwitchBot(**settings)
        bots.append(bot)

    BotIRCClient.bots = bots
    BotIRCClient.ws_factory = BotWebSocketClientFactory()

    reactor.connectTCP('irc.chat.twitch.tv', 6667, BotFactory())
    reactor.run()
