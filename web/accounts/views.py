from django.db.models.signals import post_save, post_delete
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from rest_framework import viewsets

from .models import Token, User, Setting, CustomCommand
from .utils import get_token_by_code
from .forms import (
    CustomUserCreationForm, CustomUserChangeForm, SettingsChangeForm
)
from .tasks import set_twitch_username_and_id_to_user
from .serializers import UserSerializer, TokenSerializer, SettingSerializer


def index(request):
    # user = request.user
    # if user.is_active and getattr(user, 'token'):
    #     return redirect('settings')
    return render(request, 'index.html')


def signup(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('index')
    else:
        form = CustomUserCreationForm()
    return render(request, 'signup.html', {'form': form})


def connect_to_twicth(request):
    code = request.GET.get('code')
    access_token, refresh_token, expires_in, expires_time = get_token_by_code(code)
    user = request.user
    token = Token(
                access_token=access_token,
                refresh_token=refresh_token,
                expires_in=expires_in,
                expires_time=expires_time,
                user=user
    )
    token.save()

    set_twitch_username_and_id_to_user.delay(user.id)

    return redirect('index')


def profile(request):
    if request.method == 'POST':
        form = CustomUserChangeForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
    return render(request, 'profile.html')


def settings(request):
    # TODO refactor this view and rename variables!!!
    user = request.user
    user_settings = Setting.objects.get(user_id=user.id)
    custom_commands = CustomCommand.objects.filter(settings_id=user_settings.id)
    if request.method == 'POST':
        data = {
            'default_commands': request.POST.getlist('default_commands'),
            'antispam_settings': request.POST.getlist('antispam_settings'),
            'cmd_name': request.POST.getlist('cmd_name'),
            'cmd_reply': request.POST.getlist('cmd_reply'),
            'new_cmd_name': request.POST.get('new_cmd_name'),
            'new_cmd_reply': request.POST.get('new_cmd_reply')
         }
        form = SettingsChangeForm(data)
        print(form)
        if form.is_valid():
            # TODO move to utils
            default_commands = form.cleaned_data.get('default_commands')
            antispam_settings = form.cleaned_data.get('antispam_settings')
            custom_commands_list = form.cleaned_data.get('custom_commands')
            new_custom_command = form.cleaned_data.get('new_custom_command')
            # save changed settings
            user_settings.default_commands = default_commands
            user_settings.antispam = antispam_settings
            user_settings.save()
            # delete custom commands from db those was deleted on site
            custom_commands_dict = {cstm_cmd['name']: cstm_cmd['reply'] for cstm_cmd in custom_commands_list}
            for cmd in custom_commands:
                if cmd.name not in custom_commands_dict.keys():
                    if cmd.reply in custom_commands_dict.values():
                        cmd.name = [name for name, reply in custom_commands_dict.items() if cmd.reply == reply][0]
                        cmd.save()
                    else:
                        cmd.delete()
                else:
                    if cmd.reply != custom_commands_dict[cmd.name]:
                        cmd.reply = custom_commands_dict[cmd.name]
                        cmd.save()
            # add new custom commands to db if was added on site
            if new_custom_command['name']:
                CustomCommand.objects.create(settings_id=user_settings.id, **new_custom_command)
            post_save, post_delete
            custom_commands = CustomCommand.objects.filter(settings_id=user_settings.id)
    else:
        form = SettingsChangeForm()
    return render(
        request, 'settings.html', {
            'settings': user_settings, 'custom_commands': custom_commands,
            'default_commands': ["uptime", "followage", "game", "title"],
            'antispam_settings': ['urls', 'caps'],
            'form': form
        }
    )


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class TokenViewSet(viewsets.ModelViewSet):
    queryset = Token.objects.all()
    serializer_class = TokenSerializer


class SettingViewSet(viewsets.ModelViewSet):
    queryset = Setting.objects.all()
    serializer_class = SettingSerializer
