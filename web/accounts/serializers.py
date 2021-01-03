from rest_framework import serializers

from .models import User, Token, Setting, CustomCommand


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


class UserField(serializers.RelatedField):
    def to_representation(self, value):
        user_data = {
            'twitch_username': value.twitch_username,
            'twitch_user_id': value.twitch_user_id,
            'token': value.token.access_token
        }
        return user_data


class CustomCommandSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomCommand
        fields = ['name', 'reply']


class SettingSerializer(serializers.ModelSerializer):
    user = UserField(read_only=True)
    custom_commands = CustomCommandSerializer(many=True, read_only=True)

    class Meta:
        model = Setting
        fields = [
            'user', 'default_commands', 'custom_commands', 'antispam'
        ]
