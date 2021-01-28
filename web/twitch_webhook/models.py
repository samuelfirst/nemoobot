from django.conf import settings
from django.db import models


class Subscription(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    subscription_id = models.CharField(max_length=256)
    type = models.CharField(max_length=256)
    created_at = models.DateTimeField()
