from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from rest_framework import viewsets

from .models import Token, User
from .utils import get_token_by_code
from .forms import CustomUserCreationForm
from .tasks import (
    set_twitch_username_and_id_to_user, refresh_access_token
)
from .serializers import UserSerializer


def index(request):
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
    access_token, refresh_token, expires_in = get_token_by_code(code)
    user = request.user
    token = Token(
                access_token=access_token,
                refresh_token=refresh_token,
                expires_in=expires_in,
                user=user
    )
    token.save()

    set_twitch_username_and_id_to_user(user.id)
    countdown = token.expires_in - 10
    refresh_access_token.apply_async((token.id,), countdown=countdown)
    return redirect('index')


def profile(request):
    return render(request, 'profile.html')


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
