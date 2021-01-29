from rest_framework import viewsets, permissions

from .serializers import (
    UserSerializer, TokenSerializer, SettingSerializer,
    CustomCommandSerializer, NoticeSerializer
)
from accounts.models import Token, User, Setting, CustomCommand, Notice


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class TokenViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Token.objects.all()
    serializer_class = TokenSerializer


class SettingViewSet(viewsets.ModelViewSet):
    queryset = Setting.objects.all()
    serializer_class = SettingSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class CustomCommandsViewSet(viewsets.ModelViewSet):
    queryset = CustomCommand.objects.all()
    serializer_class = CustomCommandSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class NoticeViewSet(viewsets.ModelViewSet):
    queryset = Notice.objects.all()
    serializer_class = NoticeSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
