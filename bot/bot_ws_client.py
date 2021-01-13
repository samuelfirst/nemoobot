import json
from autobahn.twisted.websocket import (
    WebSocketClientProtocol, WebSocketClientFactory
)
from twitch_bot import TwitchBot


class BotWebSocketClient(WebSocketClientProtocol):

    irc = None

    def onConnect(self, response):
        print("[websocket] Server connected: {0}".format(response.peer))

    def onConnecting(self, transport_details):
        # print("Connecting; transport details: {}".format(transport_details))
        return None  # ask for defaults

    def onOpen(self):
        pass

    def onMessage(self, payload, isBinary):
        if isBinary:
            pass
        else:
            message = payload.decode('utf-8')
            print(f'\n[websocket] {message}\n')
            command = message.split(' ', 1)[0]
            args = json.loads(f'{message.split(" ", 1)[-1]}')
            self._process_command(command, args)

    def onClose(self, wasClean, code, reason):
        pass

    def _process_command(self, command, args):
        settings = args
        if command == 'RELOAD':
            self.irc.reload_bot(settings)
        elif command == 'ADD':
            bot = TwitchBot(**settings)
            self.irc.add_bot(bot)
        elif command == 'DELETE':
            bot = TwitchBot(**settings)
            self.irc.delete_bot(bot)


class BotWebSocketClientFactory(WebSocketClientFactory):

    protocol = BotWebSocketClient
