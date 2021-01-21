import json
from autobahn.twisted.websocket import (
    WebSocketClientProtocol, WebSocketClientFactory
)
from twisted.internet.protocol import ReconnectingClientFactory
from loguru import logger

from bot.twitch_bot import TwitchBot


class BotWebSocketClient(WebSocketClientProtocol):

    irc = None

    def onConnect(self, response):
        logger.info("Client connected: {0}".format(response.peer))

    def onConnecting(self, transport_details):
        # print("Connecting; transport details: {}".format(transport_details))
        return None  # ask for defaults

    def onOpen(self):
        pass

    def onMessage(self, payload, isBinary):
        if isBinary:
            pass
        else:
            message = json.loads(payload.decode('utf-8'))
            if message['type'] == 'command':
                data = message['data']
                command = data['command']
                args = data['args']
                logger.debug(f'Received command: {command}. With args: {args}')
                self._process_command(command, args)

    def onClose(self, wasClean, code, reason):
        logger.info("WebSocket connection closed: {0}".format(reason))

    def _process_command(self, command, args):
        try:
            if command == 'RELOAD':
                self.irc.reload_bot(args)
            elif command == 'ADD':
                bot = TwitchBot(**args)
                self.irc.add_bot(bot)
            elif command == 'DELETE':
                bot = TwitchBot(**args)
                self.irc.delete_bot(bot)
        except KeyError as err:
            logger.error(err)


class BotWebSocketClientFactory(WebSocketClientFactory, ReconnectingClientFactory):
    protocol = BotWebSocketClient

    maxDelay = 10
    maxRetries = 5

    def startedConnecting(self, connector):
        logger.info('Started to connect.')

    def clientConnectionLost(self, connector, reason):
        logger.info(f'Lost connection. Reason: {format(reason)}.')
        ReconnectingClientFactory.clientConnectionLost(self, connector, reason)

    def clientConnectionFailed(self, connector, reason):
        logger.info(f'Connection failed. Reason: {format(reason)}.')
        ReconnectingClientFactory.clientConnectionFailed(self, connector, reason)
