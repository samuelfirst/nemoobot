from rest_framework import serializers

from .models import User, Token


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'twitch_username', 'twitch_user_id']


class TokenSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Token
        fields = ['access_token', 'refresh_token', 'expires_in', 'user']
