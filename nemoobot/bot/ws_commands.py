from nemoobot.bot.exceptions import SettingsNotFound


class Command:
    keyword = ''

    def __init__(self, irc):
        """Initialize the command."""
        self.irc_client = irc

    def run(self, bot_class, *args, **kwargs):
        """Run this command."""
        raise NotImplementedError

    def close(self):
        """Clean up."""
        pass


class BotInitCommand(Command):
    keyword = 'init'

    def __init__(self, irc):
        super().__init__(irc)
        self.name = 'INIT'

    def run(self, bot_class, *args, **kwargs) -> None:
        """
        Initialize and add new bot if settings found
        """
        settings = kwargs.get('settings')

        if not settings:
            raise SettingsNotFound('Settings not found in command kwargs')

        bot = bot_class(**settings)
        self.irc_client.add_bot(bot)
        self.irc_client.join_bot_channel(bot)


COMMANDS_MAP = {
    BotInitCommand.keyword: BotInitCommand,
}
