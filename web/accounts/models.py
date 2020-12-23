from django.conf import settings
from django.db import models


class Token(models.Model):

    access_token = models.CharField(max_length=40)
    refresh_token = models.CharField(max_length=80)
    expires_in = models.IntegerField()
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return self.access_token
