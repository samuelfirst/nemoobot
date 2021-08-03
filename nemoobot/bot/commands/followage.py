from nemoobot.bot.commands import Command
from nemoobot.bot.utils import decapi_followage


class FollowAge(Command):
    def run(self, bot, user: str, msg: str) -> None:
        twitch_username = bot.channel[1:]
        follow = decapi_followage(twitch_username, user)
        if 'Follow not found' in follow:
            bot.write(user + ' ты не подписан!')
        elif twitch_username == user:
            bot.write('Сам на себя не подпишешься, никто не подпишется')
        else:
            bot.write(user + ' ты следишь за каналом уже ' + follow)
