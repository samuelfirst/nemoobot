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

    def clean(self):
        cleaned_data = super().clean()

        default_commands = cleaned_data.get('default_commands')
        antispam_settings = cleaned_data.get('antispam_settings')

        if default_commands is None:
            default_commands = list()
        if antispam_settings is None:
            antispam_settings = list()

        self.cleaned_data = {
            'default_commands': default_commands,
            'antispam_settings': antispam_settings,
        }
