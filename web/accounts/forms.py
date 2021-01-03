from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from .models import User


class CustomUserCreationForm(UserCreationForm):

    class Meta(UserCreationForm):
        model = User
        fields = ('username',)


class CustomUserChangeForm(UserChangeForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        del self.fields['password']

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', )


class SettingsChangeForm(forms.Form):

    default_commands = forms.JSONField(required=False)
    antispam_settings = forms.JSONField(required=False)
    cmd_name = forms.JSONField()
    cmd_reply = forms.JSONField()
    new_cmd_name = forms.CharField(max_length=50, required=False)
    new_cmd_reply = forms.CharField(max_length=200, required=False)

    def clean(self):
        # TODO refactor clean method
        cleaned_data = super().clean()

        default_commands = cleaned_data.get('default_commands')
        antispam_settings = cleaned_data.get('antispam_settings')
        cmd_names = cleaned_data.get('cmd_name')
        cmd_replies = cleaned_data.get('cmd_reply')
        if cmd_names is not None and cmd_replies is not None:
            custom_commands = [
                {'name': name, 'reply': reply} for name, reply in zip(cmd_names, cmd_replies)
            ]
        else:
            custom_commands = []
        new_custom_command = {
            'name': cleaned_data.get('new_cmd_name'),
            'reply': cleaned_data.get('new_cmd_reply'),
        }
        if default_commands is None:
            default_commands = list()
        if antispam_settings is None:
            antispam_settings = list()
        self.cleaned_data = {
            'default_commands': default_commands,
            'antispam_settings': antispam_settings,
            'custom_commands': custom_commands,
            'new_custom_command': new_custom_command,
        }
