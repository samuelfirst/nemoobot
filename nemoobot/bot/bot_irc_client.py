from typing import List

from apscheduler.schedulers.twisted import TwistedScheduler
from twisted.words.protocols import irc
from twisted.internet import reactor
from loguru import logger

from bot.config import BOT_NICKNAME, CLIENT_ID, BOT_AUTH_TOKEN, WS_HOST, WS_PORT, RABBITMQ_HOST, RABBITMQ_PORT
from bot.twitch_bot import TwitchBot


class BotIRCClient(irc.IRCClient):

    bots: List[TwitchBot] = []
    ws_factory = None
    is_started: bool = False
    scheduler: TwistedScheduler = TwistedScheduler()

    def __init__(self):
        self.username = BOT_NICKNAME
        self.client_id = CLIENT_ID
        self.password = BOT_AUTH_TOKEN
        # set irc attribute for websocket factory's protocol
        self.amqp.protocol.irc = self

    def signedOn(self):
        self.factory.wait_time = 1

        # self.sendLine("CAP REQ :twitch.tv/membership")
        self.sendLine("CAP REQ :twitch.tv/commands")
        # self.sendLine("CAP REQ :twitch.tv/tags")

        self.scheduler.start()

        for bot in self.bots:
            self.join_bot_channel(bot)

        # connect to websocket
        if self.amqp is not None:
            reactor.connectTCP(RABBITMQ_HOST, RABBITMQ_PORT, self.amqp)

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
        if bot.jobs:
            for job in bot.jobs.items():
                job_id = f'{bot.channel}_{job[0]}'
                self.scheduler.add_job(
                    bot.write,
                    'interval',
                    minutes=job[1]['interval'],
                    id=job_id,
                    kwargs={
                        'message': job[1]['text']
                    }
                )

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
        # TODO fix bug if twitch_user_id is None or ''
        for bot in self.bots:
            if bot.channel_id == args['user']['twitch_user_id']:
                bot.reload(**args)
                logger.info(f'Bot in {bot.channel} was reloaded!')

    def add_bot_job(self, args):
        for bot in self.bots:
            if bot.channel_id == args['user']['twitch_user_id']:
                channel = args['user']['twitch_username']
                job_text = args["job"]["text"]
                job_interval = args["job"]["interval"]
                job_id = f'#{channel}_{args["job"]["id"]}'
                self.scheduler.add_job(
                    bot.write,
                    'interval',
                    minutes=job_interval,
                    id=job_id,
                    kwargs={
                        'message': job_text
                    }
                )
                bot.jobs[args["job"]["id"]] = {
                    'text': job_text,
                    'interval': job_interval
                }

    def remove_bot_job(self, args):
        for bot in self.bots:
            if bot.channel_id == args['user']['twitch_user_id']:
                channel = args['user']['twitch_username']
                job_id = f'#{channel}_{args["job"]["id"]}'
                self.scheduler.remove_job(job_id=job_id)
                bot.jobs.pop(args["job"]["id"])
