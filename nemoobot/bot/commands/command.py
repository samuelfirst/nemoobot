from typing import List


class Command:
    def __init__(self, bot):
        """Initialize the command."""
        pass

    def match(self, bot, user: str, cmd_name: str, cmd_args: List) -> bool:
        """Return whether this command should be run."""
        return cmd_name == self.__class__.__name__.lower()

    def run(self, bot, user: str, msg: str):
        """Run this command."""
        pass

    def close(self, bot):
        """Clean up."""
        pass
