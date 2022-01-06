import os
from datetime import datetime

import requests
from Cryptodome.Hash import HMAC, SHA256
from accounts.utils import send_message_to_queue


def is_request_verified(request):
    twitch_signature = request.headers.get('Twitch-Eventsub-Message-Signature', '')
    message_id = request.headers.get('Twitch-Eventsub-Message-Id', '')
    timestamp = request.headers.get('Twitch-Eventsub-Message-Timestamp', '')
    payload = message_id.encode('utf-8') + timestamp.encode('utf-8') + request.body
    secret = os.getenv('WEBHOOK_SECRET').encode('utf-8')
    _hash = HMAC.new(secret, payload, SHA256)
    signature = f"sha256={_hash.hexdigest()}"
    return twitch_signature == signature


def process_event(event, event_type):
    if event_type == 'new_follow':
        twitch_user_id = int(event.get('broadcaster_user_id'))
        follower_name = event.get('user_name')
        message = {
            "type": "command",
            "data": {
                "command": 'NEW_FOLLOW',
                "args": {
                    "twitch_user_id": twitch_user_id,
                    "follower_name": follower_name
                }
            }
        }
        send_message_to_queue(message)


def twitch_time_to_datetime(twitch_time: str):
    twitch_time = twitch_time.replace('T', ' ').replace('Z', '').split('.')[0]
    frmt = '%Y-%m-%d %H:%M:%S'
    return datetime.strptime(twitch_time, frmt)


def get_app_access_token():
    tokens_url = f"{os.getenv('BASE_API_URL')}tokens/"
    res = requests.get(tokens_url)
    tokens = res.json()
    app_access_token = tokens[0].get('access_token')
    return app_access_token
