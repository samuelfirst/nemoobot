from django.conf import settings
from celery import shared_task
import requests

from .models import User, Token


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

    user.save()


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

    token.access_token = access_token
    token.expires_in = expires_in
    token.save()

    countdown = token.expires_in - 10
    refresh_access_token.apply_async((token.id,), countdown=countdown)
