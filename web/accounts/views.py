from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from rest_framework import viewsets, permissions

from forms import CustomUserCreationForm, CustomUserChangeForm
from models import Token, User
from serializers import TokenSerializer, UserSerializer
from tasks import set_twitch_username_and_id_to_user
from utils import get_token_by_code, get_log_files_filenames


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


@login_required()
def logs(request):
    if request.user.is_staff:
        query = request.GET
        filename = query.get('filename', '')
        filenames = get_log_files_filenames()
        if filename and filename in filenames:
            return {'downloading'}
        context = {
            'filenames': filenames,
        }
        return render(request, 'logs.html', context)
    else:
        return redirect('index')


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class TokenViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Token.objects.all()
    serializer_class = TokenSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
