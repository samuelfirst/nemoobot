import json
from channels.generic.websocket import AsyncWebsocketConsumer

from accounts.tasks import send_command_to_bot


ROOM_GROOP_NAME = 'bot_commands'


class Commands:
    START = 'start_bot'
    INIT_BOT = 'INIT'


class BotCommandsConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_group_name = ROOM_GROOP_NAME

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()

    async def receive(self, text_data):
        message = json.loads(text_data)
        if message['type'] == 'command':
            await self.channel_layer.group_send(
                self.room_group_name,
                message
            )

    async def command(self, event):
        command = event['data']['command']
        if command == Commands.START:
            send_command_to_bot.apply_async((Commands.INIT_BOT,))
        else:
            await self.send(json.dumps(event))
