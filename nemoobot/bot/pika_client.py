import json

import pika
from loguru import logger
from pika import spec
from pika.adapters import twisted_connection
from pika.exchange_type import ExchangeType
from twisted.internet import defer, protocol
from twisted.internet.defer import inlineCallbacks

from bot.config import (
    RABBITMQ_HOST, RABBITMQ_USER, RABBITMQ_PASS, RABBITMQ_BASE_EXCHANGE, RABBITMQ_BOT_QUEUE, RABBITMQ_BACKEND_QUEUE
)
from bot.twitch_bot import TwitchBot


PREFETCH_COUNT = 10


class PikaProtocol(twisted_connection.TwistedProtocolConnection):
    connected = False
    name = 'AMQP:Protocol'
    irc = None

    def __init__(self, factory, parameters):
        super().__init__(parameters)
        self.factory = factory

    @inlineCallbacks
    def connectionReady(self):
        self._channel = yield self.channel()
        yield self._channel.basic_qos(prefetch_count=PREFETCH_COUNT)
        self.connected = True
        yield self._channel.confirm_delivery()
        for (
                exchange,
                routing_key,
                callback,
        ) in self.factory.read_list:
            yield self.setup_read(exchange, routing_key, callback)

        if not self.irc.is_started and not self.irc.bots:
            payload = {
                'type': 'command',
                'data': {
                    'command': 'start_bot',
                    'args': {},
                }
            }

            self.send_message(RABBITMQ_BASE_EXCHANGE, RABBITMQ_BACKEND_QUEUE, json.dumps(payload).encode('utf8'))
            logger.info('Send start_bot command to backend')
            self.irc.is_started = True
            self.setup_read(RABBITMQ_BASE_EXCHANGE, RABBITMQ_BOT_QUEUE, self._process_command)

        self.send()

    @inlineCallbacks
    def read(self, exchange, routing_key, callback):
        """Add an exchange to the list of exchanges to read from."""
        if self.connected:
            yield self.setup_read(exchange, routing_key, callback)

    @inlineCallbacks
    def setup_read(self, exchange, routing_key, callback):
        """This function does the work to read from an exchange."""
        if exchange:
            yield self._channel.exchange_declare(
                exchange=exchange,
                exchange_type=ExchangeType.topic,
                durable=True,
                auto_delete=False)

        yield self._channel.queue_declare(queue=routing_key, durable=True)
        if exchange:
            yield self._channel.queue_bind(queue=routing_key, exchange=exchange)
            yield self._channel.queue_bind(
                queue=routing_key, exchange=exchange, routing_key=routing_key)

        (
            queue,
            _consumer_tag,
        ) = yield self._channel.basic_consume(
            queue=routing_key, auto_ack=False)
        d = queue.get()
        d.addCallback(self._read_item, queue, callback)
        d.addErrback(self._read_item_err)

    def _read_item(self, item, queue, callback):
        """Callback function which is called when an item is read."""
        d = queue.get()
        d.addCallback(self._read_item, queue, callback)
        d.addErrback(self._read_item_err)
        (
            channel,
            deliver,
            _props,
            msg,
        ) = item

        logger.info('%s (%s): %s' % (deliver.exchange, deliver.routing_key, repr(msg)))
        d = defer.maybeDeferred(callback, item)
        d.addCallbacks(lambda _: channel.basic_ack(deliver.delivery_tag))

    @staticmethod
    def _read_item_err(error):
        print(error)

    def send(self):
        """If connected, send all waiting messages."""
        if self.connected:
            while self.factory.queued_messages:
                (
                    exchange,
                    r_key,
                    message,
                ) = self.factory.queued_messages.pop(0)
                self.send_message(exchange, r_key, message)

    @inlineCallbacks
    def send_message(self, exchange, routing_key, msg):
        """Send a single message."""
        logger.info('%s (%s): %s' % (exchange, routing_key, repr(msg)))
        yield self._channel.exchange_declare(
            exchange=exchange,
            exchange_type=ExchangeType.topic,
            durable=True,
            auto_delete=False)
        yield self._channel.queue_declare(queue=routing_key, durable=True)
        if exchange:
            yield self._channel.queue_bind(queue=routing_key, exchange=exchange)
            yield self._channel.queue_bind(queue=routing_key, exchange=exchange, routing_key=routing_key)
        prop = spec.BasicProperties()
        try:
            yield self._channel.basic_publish(
                exchange=exchange,
                routing_key=routing_key,
                body=msg,
                properties=prop)
        except Exception as error:  # pylint: disable=W0703
            logger.info('Error while sending message: %s' % error, system=self.name)

    def _process_command(self, msg):
        message = json.loads(msg[3].decode())
        if message['type'] == 'command':
            data = message['data']
            command = data['command']
            args = data['args']
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


class PikaFactory(protocol.ReconnectingClientFactory):
    protocol = PikaProtocol
    name = 'AMQP:Factory'

    def __init__(self, parameters=None):
        if parameters is not None:
            self.parameters = parameters
        else:
            self.parameters = pika.ConnectionParameters(
                host=RABBITMQ_HOST,
                virtual_host="/",
                credentials=pika.PlainCredentials(RABBITMQ_USER, RABBITMQ_PASS)
            )
        self.client = None
        self.queued_messages = []
        self.read_list = []

    def startedConnecting(self, connector):
        logger.info('Started to connect.', system=self.name)

    def buildProtocol(self, addr):
        self.resetDelay()
        logger.info('Connected', system=self.name)
        self.client = PikaProtocol(self, self.parameters)
        return self.client

    def clientConnectionLost(self, connector, reason): # pylint: disable=W0221
        logger.info('Lost connection.  Reason: %s' % reason.value, system=self.name)
        protocol.ReconnectingClientFactory.clientConnectionLost(
            self, connector, reason)

    def clientConnectionFailed(self, connector, reason):
        logger.info(
            'Connection failed. Reason: %s' % reason.value, system=self.name)
        protocol.ReconnectingClientFactory.clientConnectionFailed(
            self, connector, reason)

    def send_message(self, exchange=None, routing_key=None, message=None):
        self.queued_messages.append((exchange, routing_key, message))
        if self.client is not None:
            self.client.send()

    def read_messages(self, exchange, routing_key, callback):
        """Configure an exchange to be read from."""
        self.read_list.append((exchange, routing_key, callback))
        if self.client is not None:
            self.client.read(exchange, routing_key, callback)
