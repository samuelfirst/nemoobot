import time
import requests
from django.conf import settings
from celery import shared_task

from .models import User, Token
from .utils import get_user_settings_by_id, send_message_to_ws


@shared_task
def set_twitch_username_and_id_to_user(user_id):
    user = User.objects.get(pk=user_id)
    url = 'https://id.twitch.tv/oauth2/validate'
    token = user.token.access_token
    headers = {
        "Authorization": f"OAuth {token}"
    }

    res = requests.get(url, headers=headers)
    res = res.json()

    twitch_username = res['login']
    twitch_user_id = res['user_id']

    user.twitch_username = twitch_username
    user.twitch_user_id = twitch_user_id
    user.is_connected_to_twitch = True

    user.save(update_fields=['twitch_username', 'twitch_user_id'])


@shared_task
def refresh_access_token(token_id):
    token = Token.objects.get(pk=token_id)
    url = 'https://id.twitch.tv/oauth2/token'
    params = {
        'grant_type': 'refresh_token',
        'refresh_token': token.refresh_token,
        'client_id': settings.TWITCH_CLIENT_ID,
        'client_secret': settings.TWITCH_CLIENT_SECRET,
    }
    res = requests.post(url, params=params)
    res = res.json()

    access_token = res['access_token']
    expires_in = res['expires_in']
    expires_time = expires_in + int(time.time())

    token.access_token = access_token
    token.expires_in = expires_in
    token.expires_time = expires_time
    token.save()


@shared_task
def check_twitch_access_token_freshness():
    tokens = Token.objects.all()
    for token in tokens:
        freshness_time = token.expires_time - int(time.time())
        if freshness_time < 60:
            refresh_access_token.apply_async((token.id,))


@shared_task
def send_command_to_bot(command, settings_id):
    settings = get_user_settings_by_id(settings_id)
    message = f'{command} {settings}'
    send_message_to_ws(message)
