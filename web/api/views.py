from rest_framework import viewsets, permissions

from serializers import SettingSerializer, CustomCommandSerializer, NoticeSerializer
from models import Setting, CustomCommand, Notice


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
