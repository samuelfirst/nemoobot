from django.apps import AppConfig


class TwitchWebhookConfig(AppConfig):
    name = 'twitch_webhook'

    def ready(self):
        import twitch_webhook.signals
