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
        }
        return user_data


class CustomCommandSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomCommand
        fields = ['settings', 'name', 'reply']


class CustomCommandField(serializers.RelatedField):
    def to_representation(self, value):
        command_data = {
            'name': value.name,
            'reply': value.reply
        }
        return command_data


class SettingSerializer(serializers.ModelSerializer):
    user = UserField(read_only=True)
    custom_commands = CustomCommandField(many=True, read_only=True)
    default_commands = serializers.ListField(child=serializers.CharField())
    antispam = serializers.ListField(child=serializers.CharField())

    class Meta:
        model = Setting
        fields = [
            'user', 'default_commands', 'custom_commands', 'antispam'
        ]
