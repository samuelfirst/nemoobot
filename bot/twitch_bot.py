import commands


class TwitchBot:
    def __init__(self, channel):
        self.channel = f"#{channel}"
        self.irc = None
        self.commands = []
        self.load_commands()

    def load_commands(self):
        for cmd in commands.commands:
            self.commands.append(cmd(self))

    def process_command(self, user, message):
        for cmd in self.commands:
            if cmd.match(self, user, message):
                cmd.run(self, user, message)
            else:
                pass

    def write(self, message):
        if self.irc is not None:
            self.irc.msg(self.channel, message)

    def timeout(self, user, duration):
        timeout_message = f"/timeout {user} {duration}"
        self.write(timeout_message)

    def ban(self, user):
        ban_message = f"/ban {user}"
        self.write(ban_message)

    def unban(self, user):
        unban_message = f"/unban {user}"
        self.write(unban_message)
