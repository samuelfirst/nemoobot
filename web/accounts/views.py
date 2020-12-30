from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from rest_framework import viewsets

from .models import Token, User, Setting
from .utils import get_token_by_code
from .forms import CustomUserCreationForm, CustomUserChangeForm
from .tasks import set_twitch_username_and_id_to_user
from .serializers import UserSerializer, TokenSerializer, SettingSerializer


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


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class TokenViewSet(viewsets.ModelViewSet):
    queryset = Token.objects.all()
    serializer_class = TokenSerializer


class SettingViewSet(viewsets.ModelViewSet):
    queryset = Setting.objects.all()
    serializer_class = SettingSerializer
