from django.conf import settings
from django.db import models
from django.contrib.postgres.fields import ArrayField, JSONField


class Setting(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    default_commands = JSONField(
        models.CharField(max_length=50, blank=True),
        default=dict,
    )
    antispam_settings = JSONField(
        models.CharField(max_length=50, blank=True),
        default=list,
    )
    follow_notification = models.BooleanField(default=False)
    follow_notification_text = models.TextField(
        default='Welcome <username>! Thank you for follow!'
    )
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
        return f"CustomCommand !{self.name}; User: {self.settings.user.username}"


class Notice(models.Model):
    settings = models.ForeignKey(
        Setting, on_delete=models.CASCADE,
        related_name='notices',
        related_query_name='notice',
    )
    text = models.TextField()
    interval = models.IntegerField()

    def __str__(self):
        return f'Notice {self.id}; User: {self.settings.user.username}'

