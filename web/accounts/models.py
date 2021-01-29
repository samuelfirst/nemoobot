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


class Setting(models.Model):

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    default_commands = ArrayField(
        models.CharField(max_length=50, blank=True),
        default=list,
    )
    antispam = ArrayField(
        models.CharField(max_length=50, blank=True),
        default=list,
    )
    follow_notification = models.BooleanField(default=False)
    banned_words = ArrayField(
        models.CharField(max_length=50, blank=True),
        default=list,
    )

    def __str__(self):
        return f"Settings {self.user.username}"


class CustomCommand(models.Model):
    settings = models.ForeignKey(
        Setting, on_delete=models.CASCADE,
        related_name='custom_commands',
        related_query_name='custom_command',
    )
    name = models.CharField(max_length=50)
    reply = models.TextField()

    def __str__(self):
        return f"CustomCommand {self.name} user {self.settings.user.pk}"


class Notice(models.Model):
    settings = models.ForeignKey(
        Setting, on_delete=models.CASCADE,
        related_name='notices',
        related_query_name='notice',
    )
    text = models.TextField()
    interval = models.IntegerField()

    def __str__(self):
        return f'Notice {self.id} user {self.settings.user.pk}'
