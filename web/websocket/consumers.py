import json

from channels.generic.websocket import AsyncWebsocketConsumer


class BotCommandsConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_group_name = 'bot_commands'

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
        await self.send(json.dumps(event))
