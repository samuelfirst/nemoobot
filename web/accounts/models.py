from django.conf import settings
from django.db import models
from django.contrib.postgres.fields import ArrayField, HStoreField
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):

    twitch_username = models.CharField(max_length=100, blank=True)
    twitch_user_id = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return self.username


class Token(models.Model):

    access_token = models.CharField(max_length=40)
    refresh_token = models.CharField(max_length=80)
    expires_in = models.IntegerField()
    expires_time = models.IntegerField()
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return self.access_token


class Setting(models.Model):

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    default_commands = ArrayField(
        models.CharField(max_length=50, blank=True),
    )
    custom_commands = models.JSONField(default=list)
    antispam = ArrayField(
        models.CharField(max_length=50, blank=True),
    )

    def __str__(self):
        return self.user.username
