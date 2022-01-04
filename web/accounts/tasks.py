import requests
import time

from django.conf import settings
from celery import shared_task

from twitch_webhook.tasks import create_subscription
from .models import User, Token, Notice
from .utils import (
    get_user_settings_by_id, get_list_user_settings, send_message_to_ws,
    get_app_token
)


@shared_task
def set_twitch_username_and_id_to_user(user_id: int) -> str:
    """Get user info from Twitch and save it for user"""
    user = User.objects.get(pk=user_id)
    url = 'https://id.twitch.tv/oauth2/validate'
    token = user.token.access_token
    headers = {
        "Authorization": f"OAuth {token}"
    }

    res = requests.get(url, headers=headers)
    res = res.json()

    user.twitch_username = res['login']
    user.twitch_user_id = res['user_id']
    user.is_connected_to_twitch = True

    user.save(update_fields=[
        'twitch_username', 'twitch_user_id', 'is_connected_to_twitch'
    ])

    create_subscription.apply_async((user.id, 'channel.follow'))
    return f'Set twitch_username, twitch_user_id, is_connected_to_twitch for User {user}'


@shared_task
def refresh_access_token(token_id: int) -> str:
    """Get token id and refresh token info"""
    token = Token.objects.get(pk=token_id)
    if token.token_type == 'userToken':
        url = 'https://id.twitch.tv/oauth2/token'
        params = {
            'grant_type': 'refresh_token',
            'refresh_token': token.refresh_token,
            'client_id': settings.TWITCH_CLIENT_ID,
            'client_secret': settings.TWITCH_CLIENT_SECRET,
        }
        res = requests.post(url, params=params)
        res = res.json()

        token.access_token = res['access_token']
        token.expires_in = res['expires_in']
        token.expires_time = token.expires_in + int(time.time())
    elif token.token_type == 'appToken':
        access_token, expires_in, expires_time = get_app_token()
        token.access_token = access_token
        token.expires_in = expires_in
        token.expires_time = expires_time
    token.save()
    return f'{token} was refreshed'


@shared_task
def check_twitch_access_token_freshness() -> None:
    """Check access token freshness if expire time less then 60 seconds, create task to refrsesh token"""
    tokens = Token.objects.all()
    for token in tokens:
        freshness_time = token.expires_time - int(time.time())
        if freshness_time < 60:
            refresh_access_token.apply_async((token.id,))


@shared_task
def send_command_to_bot(command: str, settings_id: int = None) -> str:
    if settings_id is not None:
        settings = get_user_settings_by_id(settings_id)
        message = {
            "type": "command",
            "data": {
                "command": command,
                "args": settings
            }
        }
    else:
        list_settings = get_list_user_settings()
        print(list_settings)
        if list_settings:
            message = {
                "type": "command",
                "data": {
                    "command": command,
                    "args": list_settings
                }
            }
        else:
            return
    send_message_to_ws(message)
    return 'Message sent to ws'


@shared_task
def send_job_command_to_bot(command: str, notice_id: int) -> None:
    notice = Notice.objects.get(pk=notice_id)
    user = notice.settings.user
    args = {
        'user': {
            'twitch_username': user.twitch_username,
            'twitch_user_id': user.twitch_user_id
        },
        'job': {
            'id': notice.id,
            'text': notice.text,
            'interval': notice.interval
        }
    }
    message = {}
    if command == "ADD_JOB":
        message = {
            "type": "command",
            "data": {
                "command": command,
                "args": args
            }
        }
    elif command == "REMOVE_JOB":
        message = {
            "type": "command",
            "data": {
                "command": command,
                "args": args
            }
        }
    send_message_to_ws(message)
