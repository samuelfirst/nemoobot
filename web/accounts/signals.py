from django.db.models.signals import post_save, post_delete, pre_delete
from django.dispatch import receiver

from .models import CustomCommand, Setting, User, Token
from .tasks import send_command_to_bot


@receiver(post_save, sender=Token)
def create_default_settings_for_new_user(sender, **kwargs):
    if kwargs.get('created'):
        token = kwargs.get('instance')
        user_id = token.user
        settings = Setting(
            user=user_id,
            default_commands=['uptime', 'followage', 'game', 'title'],
            antispam=['caps', 'urls']
        )
        settings.save()


@receiver([post_save, post_delete], sender=CustomCommand)
@receiver(post_save, sender=Setting)
def send_reload_command_to_bot(sender, **kwargs):
    if sender is Setting:
        settings = kwargs.get('instance')
        if kwargs.get('created'):
            return
    else:
        custom_command = kwargs.get('instance')
        settings = custom_command.settings
    send_command_to_bot.apply_async(('RELOAD', settings.id))


@receiver(post_save, sender=User)
def send_add_command_to_bot(sender, **kwargs):
    update_fields = kwargs.get('update_fields')
    if update_fields and 'twitch_username' in update_fields:
        user = kwargs.get('instance')
        settings = Setting.objects.get(user_id=user.id)
        send_command_to_bot.apply_async(('ADD', settings.id))


@receiver(pre_delete, sender=Setting)
def send_delete_command_to_bot(sender, **kwargs):
    settings = kwargs.get('instance')
    # waiting for result of task and then delete settings
    result = send_command_to_bot.apply_async(('DELETE', settings.id))
    if result.get():
        return
