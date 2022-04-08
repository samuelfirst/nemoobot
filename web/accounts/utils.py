import json
import os
import time
from typing import List

import pika
import requests
from django.conf import settings


def get_token_by_code(code):
    params = {
        'client_id': settings.TWITCH_CLIENT_ID,
        'client_secret': settings.TWITCH_CLIENT_SECRET,
        'code': code,
        'grant_type': 'authorization_code',
        'redirect_uri': settings.TWITCH_REDIRECT_URL,

    }
    url = "https://id.twitch.tv/oauth2/token"
    res = requests.post(url, params=params)
    token_data = res.json()
    access_token = token_data['access_token']
    refresh_token = token_data['refresh_token']
    expires_in = token_data['expires_in']
    expires_time = expires_in + int(time.time())
    return access_token, refresh_token, expires_in, expires_time


def get_user_settings_by_id(settings_id):
    # TODO remove this shit
    url = f'{settings.BASE_API_URL}settings/{settings_id}'
    res = requests.get(url)
    return res.json()


def get_list_user_settings():
    # TODO remove this shit
    url = f'{settings.BASE_API_URL}settings/'
    res = requests.get(url)
    return res.json()


def send_message_to_queue(message):
    print('sending mesasge to queue. Message: {message}')
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(
            host=settings.RABBITMQ_HOST,
            virtual_host="/",
            credentials=pika.PlainCredentials(settings.RABBITMQ_USER, settings.RABBITMQ_PASS)
        )
    )
    channel = connection.channel()
    channel.basic_publish(
        exchange=settings.RABBITMQ_BASE_EXCHANGE,
        routing_key=settings.RABBITMQ_BOT_QUEUE,
        body=json.dumps(message).encode(),
    )
    print("[x] Sent message")
    connection.close()


def get_app_token():
    params = {
        'client_id': settings.TWITCH_CLIENT_ID,
        'client_secret': settings.TWITCH_CLIENT_SECRET,
        'grant_type': 'client_credentials',

    }
    url = "https://id.twitch.tv/oauth2/token"
    res = requests.post(url, params=params)
    token_data = res.json()
    access_token = token_data['access_token']
    expires_in = token_data['expires_in']
    expires_time = expires_in + int(time.time())
    return access_token, expires_in, expires_time


def get_log_files_filenames() -> List[str]:
    """
    Get filenames of log files
    """
    filenames = [filename for filename in os.walk('../../log') if filename.endswith('.log')]
    return filenames
