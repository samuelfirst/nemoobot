from typing import List

from nemoobot.bot.commands import Command


class CustomCommand(Command):
    def __init__(self, bot, name: str, reply: str):
        super().__init__(bot)
        self.name = name
        self.reply = reply

    def match(self, bot, user: str, cmd_name: str, cmd_args: List) -> bool:
        return self.name == cmd_name

    def run(self, bot, user, msg):
        bot.write(self.reply)

