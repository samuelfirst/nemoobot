import os
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
import requests

from .models import Token

CLIENT_ID = os.getenv('CLIENT_ID')
CLIENT_SECRET = os.getenv('CLIENT_SECRET')
REDIRECT_URL = os.getenv('REDIRECT_URL')


def get_access_token_by_code(code):
    url = (
        "https://id.twitch.tv/oauth2/token"
        f"?client_id={CLIENT_ID}"
        f"&client_secret={CLIENT_SECRET}"
        f"&code={code}"
        "&grant_type=authorization_code"
        f"&redirect_uri={REDIRECT_URL}"
    )
    res = requests.post(url)
    token = res.json()["access_token"]
    return token


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
    token = get_access_token_by_code(code)
    user = request.user
    Token(access_token=token, user=user).save()
    return redirect('index')


