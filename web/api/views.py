from rest_framework import viewsets, permissions, generics

from .serializers import (
    UserSerializer, TokenSerializer, SettingSerializer,
    CustomCommandSerializer, NoticeSerializer, CreateUserSerializer
)
from accounts.models import Token, User, Setting, CustomCommand, Notice


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (permissions.IsAuthenticated,)


class TokenViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Token.objects.all()
    serializer_class = TokenSerializer
    permission_classes = (permissions.IsAuthenticated,)


class SettingViewSet(viewsets.ModelViewSet):
    queryset = Setting.objects.all()
    serializer_class = SettingSerializer
    permission_classes = (permissions.IsAuthenticated,)


class CustomCommandsViewSet(viewsets.ModelViewSet):
    queryset = CustomCommand.objects.all()
    serializer_class = CustomCommandSerializer
    permission_classes = (permissions.IsAuthenticated,)


class NoticeViewSet(viewsets.ModelViewSet):
    queryset = Notice.objects.all()
    serializer_class = NoticeSerializer
    permission_classes = (permissions.IsAuthenticated,)


class UserCreateView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = CreateUserSerializer
    permission_classes = [permissions.AllowAny]
