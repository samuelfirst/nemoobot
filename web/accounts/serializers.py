from rest_framework import serializers

from .models import User, Token


class TokenSerializer(serializers.ModelSerializer):

    class Meta:
        model = Token
        fields = [
            'access_token', 'refresh_token', 'expires_in',
        ]


class UserSerializer(serializers.ModelSerializer):
    token = TokenSerializer()

    class Meta:
        model = User
        fields = [
            'id', 'username', 'twitch_username', 'twitch_user_id', 'token',
        ]
