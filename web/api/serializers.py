from rest_framework import serializers

from accounts.models import User, Token, Setting, CustomCommand, Notice


class TokenSerializer(serializers.ModelSerializer):
    class Meta:
        model = Token
        fields = [
            'access_token', 'refresh_token', 'token_type', 'expires_in',
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
            'token': value.token.access_token,
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


class NoticeField(serializers.RelatedField):
    def to_representation(self, value):
        notice_data = {
            'id': value.id,
            'text': value.text,
            'interval': value.interval
        }
        return notice_data


class NoticeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notice
        fields = ['settings', 'text', 'interval']


class SettingSerializer(serializers.ModelSerializer):
    user = UserField(read_only=True)
    custom_commands = CustomCommandField(many=True, read_only=True)
    default_commands = serializers.ListField(child=serializers.CharField())
    antispam = serializers.ListField(child=serializers.CharField())
    banned_words = serializers.ListField(child=serializers.CharField())
    notices = NoticeField(many=True, read_only=True)

    class Meta:
        model = Setting
        fields = [
            'user', 'default_commands', 'custom_commands', 'antispam',
            'follow_notification', 'banned_words', 'notices'
        ]
