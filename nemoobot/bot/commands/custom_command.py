from .command import Command


class CustomCommand(Command):
    
    def __init__(self, bot, name, reply):
        self.name = f'!{name}'
        self.reply = reply

    def match(self, bot, user, msg):
        cmd = msg.split(' ')[0]
        return cmd == self.name

    def run(self, bot, user, msg):
        bot.write(self.reply)

