import os

import requests
from celery import shared_task

from accounts.models import User
from .models import Subscription
from .utils import twitch_time_to_datetime, get_app_access_token


@shared_task
def save_subscription_model(subscription_data, twitch_user_id):
    user = User.objects.get(twitch_user_id=twitch_user_id)
    subscription_id = subscription_data.get('id')
    _type = subscription_data.get('type')
    created_at = twitch_time_to_datetime(subscription_data.get('created_at'))
    subscription = Subscription(
        user=user,
        subscription_id=subscription_id,
        type=_type,
        created_at=created_at
    )
    subscription.save()


@shared_task
def create_subscription(user_id, subscription_type):
    user = User.objects.get(pk=user_id)
    url = "https://api.twitch.tv/helix/eventsub/subscriptions"
    token = get_app_access_token()
    headers = {
        "Client-ID": os.getenv('CLIENT_ID'),
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    data = {
        "type": subscription_type,
        "version": "1",
        "condition": {
            "broadcaster_user_id": user.twitch_user_id
        },
        "transport": {
            "method": "webhook",
            "callback": f"{os.getenv('DJANGO_HOST')}webhook/follows/{user.twitch_user_id}/",
            "secret": os.getenv('WEBHOOK_SECRET')
        }
    }
    requests.post(url, headers=headers, json=data)


@shared_task
def delete_subscription(subscription_id):
    url = "https://api.twitch.tv/helix/eventsub/subscriptions"
    token = get_app_access_token()
    headers = {
        "Client-ID": os.getenv('CLIENT_ID'),
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

    requests.post(url, headers=headers, params={"id": subscription_id})
