import json
import time

import pika
import django
from os import environ

environ.setdefault('DJANGO_SETTINGS_MODULE', 'web.settings')
django.setup()
from django.conf import settings
from accounts.tasks import send_command_to_bot

attemps = 0
reconnect = True
while reconnect:
    try:
        connection = pika.BlockingConnection(pika.ConnectionParameters(
            host=settings.RABBITMQ_HOST,
            virtual_host="/",
            credentials=pika.PlainCredentials(settings.RABBITMQ_USER, settings.RABBITMQ_PASS)
        ))
        reconnect = False
    except pika.exceptions.AMQPConnectionError:
        if attemps > 3:
            break
        attemps += 1
        time.sleep(5)

channel = connection.channel()
channel.queue_declare(queue='command_from_bot', durable=True)


def callback(ch, method, properties, body):
    print("Received in messages...")
    print(body)
    data = json.loads(body)
    if data.get('type', '') == 'command' and data.get('data', {}).get('command', '') == 'start_bot':
        send_command_to_bot.apply_async(('INIT',))


channel.basic_consume(queue='command_from_bot', on_message_callback=callback, auto_ack=True)
print("Started Consuming...")
channel.start_consuming()
