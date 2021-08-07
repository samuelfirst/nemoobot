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
        if not self.irc.is_started and not self.irc.bots:
            payload = {
                'type': 'command',
                'data': {
                    'command': 'start_bot',
                    'args': ''
                }
            }
            self.sendMessage(json.dumps(payload).encode('utf8'))
            self.irc.is_started = True
            logger.info('Sending start_bot command to get bot settings')

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
            if command == 'INIT':
                for settings in args:
                    bot = TwitchBot(**settings)
                    self.irc.add_bot(bot)
            elif command == 'RELOAD':
                self.irc.reload_bot(args)
            elif command == 'ADD':
                bot = TwitchBot(**args)
                self.irc.add_bot(bot)
            elif command == 'DELETE':
                bot = TwitchBot(**args)
                self.irc.delete_bot(bot)
            elif command == 'NEW_FOLLOW':
                for bot in self.irc.bots:
                    if bot.channel_id == args.get('twitch_user_id'):
                        user = args.get("follower_name")
                        if bot.is_follow_notice_active:
                            bot.follow_notice(user)
            elif command == 'ADD_JOB':
                self.irc.add_bot_job(args)
            elif command == 'REMOVE_JOB':
                self.irc.remove_bot_job(args)
        except KeyError as err:
            logger.error(err)


class BotWebSocketClientFactory(WebSocketClientFactory, ReconnectingClientFactory):
    protocol = BotWebSocketClient

    maxDelay = 10
    maxRetries = 10

    def startedConnecting(self, connector):
        logger.info('Started to connect.')

    def clientConnectionLost(self, connector, reason):
        logger.info(f'Lost connection. Reason: {format(reason)}.')
        self.retry(connector)

    def clientConnectionFailed(self, connector, reason):
        logger.info(f'Connection failed. Reason: {format(reason)}.')
        self.retry(connector)
