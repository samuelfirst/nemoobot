from django.db.models.signals import post_delete
from django.dispatch import receiver

from .models import Subscription
from .tasks import delete_subscription


@receiver(post_delete, sender=Subscription)
def delete_subscription_on_twitch_side(sender, instance, **kwargs):
    delete_subscription.apply_async((instance.subscription_id,))
