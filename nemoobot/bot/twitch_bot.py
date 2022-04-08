from loguru import logger
from typing import List

import bot.commands as commands
from bot.antispam import AntiSpam


class TwitchBot:
    def __init__(
            self, user, default_commands,
            custom_commands, antispam, follow_notification,
            follow_notification_text, notices, banned_words=None):

        self.channel = f"#{user['twitch_username']}"
        self.channel_id = user['twitch_user_id']
        self.token = user['token']

        self.default_commands = default_commands
        self.custom_commands = custom_commands
        self.is_follow_notice_active = follow_notification
        self.follow_notice_message = follow_notification_text

        self.jobs = dict()
        for notice in notices:
            self.jobs[notice['id']] = {
                'text': notice['text'],
                'interval': notice['interval']
            }

        if banned_words is not None:
            banned_words = set(banned_words)
        caps = 'caps' in antispam
        urls = 'urls' in antispam
        self.antispam = AntiSpam(
            is_active=True,
            caps=caps,
            urls=urls,
            banned_words=banned_words
        )

        self.irc = None

        self.commands = list()
        self.commands_list: List[str] = list()
        self.load_commands()

    def __eq__(self, other):
        if (self.channel == other.channel and
                self.default_commands == other.default_commands and
                self.custom_commands == other.custom_commands and
                self.antispam == other.antispam):
            return True
        else:
            return False

    def reload(
            self, user, default_commands,
            custom_commands, antispam, follow_notification,
            follow_notification_text, notices, banned_words=None):

        self.channel = f"#{user['twitch_username']}"
        self.channel_id = user['twitch_user_id']
        self.token = user['token']

        self.default_commands = default_commands
        self.custom_commands = custom_commands
        self.is_follow_notice_active = follow_notification
        self.follow_notice_message = follow_notification_text

        self.jobs = dict()
        for notice in notices:
            self.jobs[notice['id']] = {
                'text': notice['text'],
                'interval': notice['interval']
            }

        if banned_words is not None:
            banned_words = set(banned_words)
        caps = 'caps' in antispam
        urls = 'urls' in antispam
        self.antispam = AntiSpam(
            is_active=True,
            caps=caps,
            urls=urls,
            banned_words=banned_words
        )

        self.reload_commands()

    def load_commands(self):
        logger.info(f'Load command for TwitchBot in {self.channel} channel')
        for cmd in commands.commands:
            if cmd.__name__.lower() in self.default_commands:
                self.commands.append(cmd(self))
        if self.custom_commands:
            for custom_command in self.custom_commands:
                cmd_name = custom_command['name']
                cmd_reply = custom_command['reply']
                cmd = commands.CustomCommand(self, cmd_name, cmd_reply)
                self.commands.append(cmd)
        commands_list = list()
        for cmd in self.commands:
            try:
                commands_list.append(cmd.name.lower())
            except AttributeError:
                commands_list.append(f'!{cmd.__class__.__name__.lower()}')
        self.commands_list = commands_list

    def reload_commands(self):
        self.commands.clear()
        self.commands_list.clear()
        self.load_commands()

    def antispam_check(self, user, message):
        spam_detected, warn_message = self.antispam.check_message(message)
        if spam_detected:
            self.timeout(user, 10)
            self.write(f'{user} {warn_message}')

    def process_command(self, user, message):
        for cmd in self.commands:
            if cmd.match(self, user, message):
                logger.debug(f'[{self.channel}] {cmd.__class__.__name__} command running')
                cmd.run(self, user, message)
                return
        self.write('Unknown command.')
        self.write(f'Commands list: {", ".join(self.commands_list)}')

    def follow_notice(self, user):
        message = self.follow_notice_message.replace('<username>', user)
        self.write(message)

    def write(self, message):
        if self.irc is not None:
            self.irc.msg(self.channel, message)
            logger.info(f'[{self.channel}] {self.irc.username}: {message}')

    def timeout(self, user, duration):
        timeout_message = f"/timeout {user} {duration}"
        self.write(timeout_message)

    def ban(self, user):
        ban_message = f"/ban {user}"
        self.write(ban_message)

    def unban(self, user):
        unban_message = f"/unban {user}"
        self.write(unban_message)
