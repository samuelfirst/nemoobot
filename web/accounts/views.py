from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate

from .models import Token, User, Setting, CustomCommand
from .utils import get_token_by_code
from .forms import (
    CustomUserCreationForm, CustomUserChangeForm
)
from .tasks import set_twitch_username_and_id_to_user


def index(request):
    user = request.user
    if user.is_active and getattr(user, 'is_connected_to_twitch'):
        return redirect('settings')
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

    return redirect('settings')


@login_required
def profile(request):
    if request.method == 'POST':
        form = CustomUserChangeForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
    return render(request, 'profile.html')


@login_required
def settings(request):
    user = request.user
    user_settings = Setting.objects.filter(user_id=user.id)
    if user_settings.exists():
        user_settings = user_settings.first()
        custom_commands = CustomCommand.objects.filter(settings_id=user_settings.id)
        context = {
            'settings': user_settings, 'custom_commands': custom_commands,
            'default_commands': ["uptime", "followage", "game", "title"],
            'antispam_settings': ['urls', 'caps'],
        }
        return render(request, 'settings.html', context)
    else:
        return redirect('index')
