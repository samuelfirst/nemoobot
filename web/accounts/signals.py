from django.db.models.signals import post_save, post_delete, pre_delete
from django.dispatch import receiver

from .models import CustomCommand, Setting, User, Token, Notice
from .tasks import send_command_to_bot, send_job_command_to_bot
from .utils import get_app_token


@receiver(post_save, sender=Token)
def create_default_settings_for_new_user(sender, **kwargs):
    token = kwargs.get('instance')
    if kwargs.get('created') and token.token_type == 'userToken':
        user = token.user
        settings = Setting(
            user=user,
            default_commands=['uptime', 'followage', 'game', 'title'],
            antispam=['caps', 'urls'],
            follow_notification=True
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
    user = kwargs.get('instance')
    update_fields = kwargs.get('update_fields')
    if update_fields and 'twitch_username' in update_fields:
        settings = Setting.objects.get(user_id=user.id)
        send_command_to_bot.apply_async(('ADD', settings.id))
    if kwargs.get('created') and user.is_staff:
        access_token, expires_in, expires_time = get_app_token()
        Token(
            user=user,
            access_token=access_token,
            refresh_token="",
            expires_in=expires_in,
            expires_time=expires_time,
            token_type="appToken"
        ).save()


@receiver(pre_delete, sender=Setting)
def send_delete_command_to_bot(sender, **kwargs):
    settings = kwargs.get('instance')
    # waiting for result of task and then delete settings
    result = send_command_to_bot.apply_async(('DELETE', settings.id))
    # if result.get():
    #     return


@receiver(post_save, sender=Notice)
def send_add_job_command_to_bot(sender, instance, **kwargs):
    send_job_command_to_bot.apply_async(('ADD_JOB', instance.id))


@receiver(post_delete, sender=Notice)
def send_remove_job_command_to_bot(sender, instance, **kwargs):
    res = send_job_command_to_bot.apply_async(('REMOVE_JOB', instance.id))
    res.get()
