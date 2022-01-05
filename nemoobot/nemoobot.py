from twisted.internet import reactor, protocol
from loguru import logger

from bot.bot_irc_client import BotIRCClient
from bot.pika_client import PikaFactory

logger.add('logs/nemoobot_logs.log', enqueue=True, format="{time} {level} | {module:<15} | {message}", level="DEBUG")


class BotFactory(protocol.ClientFactory):
    protocol = BotIRCClient

    def startedConnecting(self, connector):
        logger.info("Connection has been started.")

    def clientConnectionLost(self, connector, reason):
        logger.info("Connection lost. Reason: %s" % reason)
        self.protocol.scheduler.shutdown(wait=False)
        connector.connect()

    def clientConnectionFailed(self, connector, reason):
        logger.debug("Connection failed. Reason: %s" % reason)
        self.protocol.scheduler.shutdown(wait=False)


if __name__ == '__main__':
    BotIRCClient.amqp = PikaFactory()

    reactor.connectTCP('irc.chat.twitch.tv', 6667, BotFactory())
    reactor.run()
