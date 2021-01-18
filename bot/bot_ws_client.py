import json
from autobahn.twisted.websocket import (
    WebSocketClientProtocol, WebSocketClientFactory
)
from loguru import logger

from twitch_bot import TwitchBot

logger.add('logs/nemoobot.log', format="{time} {level} {message}", filter="bot_ws_client")


class BotWebSocketClient(WebSocketClientProtocol):

    irc = None

    def onConnect(self, response):
        logger.info("Server connected: {0}".format(response.peer))

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
        pass

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


class BotWebSocketClientFactory(WebSocketClientFactory):

    protocol = BotWebSocketClient
