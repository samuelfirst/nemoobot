import os
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
import requests

from .models import Token

CLIENT_ID = os.getenv('CLIENT_ID')
CLIENT_SECRET = os.getenv('CLIENT_SECRET')
TWITCH_REDIRECT_URL = os.getenv('TWITCH_REDIRECT_URL')


def get_token_by_code(code):
    url = (
        "https://id.twitch.tv/oauth2/token"
        f"?client_id={CLIENT_ID}"
        f"&client_secret={CLIENT_SECRET}"
        f"&code={code}"
        "&grant_type=authorization_code"
        f"&redirect_uri={TWITCH_REDIRECT_URL}"
    )
    res = requests.post(url)
    token_data = res.json()
    access_token = token_data['access_token']
    refresh_token = token_data['refresh_token']
    expires_in = token_data['expires_in']
    return access_token, refresh_token, expires_in


def index(request):
    return render(request, 'index.html')


def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('index')
    else:
        form = UserCreationForm()
    return render(request, 'signup.html', {'form': form})


def connect_to_twicth(request):
    code = request.GET.get('code')
    access_token, refresh_token, expires_in = get_token_by_code(code)
    user = request.user
    token = Token(
                access_token=access_token,
                refresh_token=refresh_token,
                expires_in=expires_in,
                user=user
    )
    token.save()
    return redirect('index')


