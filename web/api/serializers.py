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
        return {
            'twitch_username': value.twitch_username,
            'twitch_user_id': value.twitch_user_id,
            'token': value.token.access_token,
        }


class CustomCommandSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomCommand
        fields = ['settings', 'name', 'reply']


class CustomCommandField(serializers.RelatedField):
    def to_representation(self, value):
        return {
            'name': value.name,
            'reply': value.reply
        }


class NoticeField(serializers.RelatedField):
    def to_representation(self, value):
        return {
            'id': value.id,
            'text': value.text,
            'interval': value.interval
        }


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
            'follow_notification', 'follow_notification_text',
            'banned_words', 'notices'
        ]
