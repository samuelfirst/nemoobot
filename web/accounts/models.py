from django.conf import settings
from django.db import models
from django.contrib.postgres.fields import ArrayField, HStoreField
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):

    email = models.EmailField(max_length=254, verbose_name='email address')
    is_connected_to_twitch = models.BooleanField(default=False)
    twitch_username = models.CharField(max_length=100, blank=True)
    twitch_user_id = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return f"User {self.username}"


class Token(models.Model):

    access_token = models.CharField(max_length=40)
    refresh_token = models.CharField(max_length=80, blank=True)
    token_type = models.CharField(max_length=50, default='userToken')
    expires_in = models.IntegerField()
    expires_time = models.IntegerField()
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return f"Token {self.access_token}"
