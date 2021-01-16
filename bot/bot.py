import os
from dotenv import load_dotenv
from twisted.internet import reactor, protocol

from twitch_bot import TwitchBot
from bot_irc_client import BotIRCClient
from utils import load_user_settings


class BotFactory(protocol.ClientFactory):
    protocol = BotIRCClient

    def startedConnecting(self, connector):
        print("Connection has been started.")

    def clientConnectionLost(self, connector, reason):
        print("Connection lost. Reason: %s" % reason)
        connector.connect()

    def clientConnectionFailed(self, connector, reason):
        print("Connection failed. Reason: %s" % reason)


if __name__ == '__main__':
    project_folder = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    load_dotenv(os.path.join(project_folder, '.env.dev'))

    # create bot instances
    bots = list()
    for settings in load_user_settings():
        bot = TwitchBot(*settings)
        bots.append(bot)

    BotIRCClient.bots = bots

    reactor.connectTCP('irc.chat.twitch.tv', 6667, BotFactory())
    reactor.run()
