from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User, Token, Setting, CustomCommand, Notice


class TokenInline(admin.TabularInline):
    model = Token
    readonly_fields = (
        'access_token', 'refresh_token', 'token_type', 'expires_in', 'expires_time',
    )


class CustomCommandInline(admin.TabularInline):
    model = CustomCommand
    readonly_fields = (
        'name', 'reply',
    )


class NoticeInline(admin.TabularInline):
    model = Notice
    readonly_fields = (
        'id', 'text', 'interval',
    )


@admin.register(Token)
class TokenAdmin(admin.ModelAdmin):
    list_display = ('access_token', 'user',)
    readonly_fields = (
        'access_token', 'refresh_token', 'token_type', 'expires_in', 'expires_time', 'user'
    )

    fieldsets = (
        ('Token', {'fields': (
            'access_token', 'refresh_token', 'token_type', 'expires_in', 'expires_time',
        )}),
        ('User', {'fields': (
            'user',
        )}),
    )


class CustomUserAdmin(UserAdmin):
    list_display = UserAdmin.list_display + (
        'is_connected_to_twitch',
    )
    inlines = (TokenInline, )
    fieldsets = UserAdmin.fieldsets + (
        ('Twitch', {'fields': ('is_connected_to_twitch', 'twitch_username', 'twitch_user_id')}),
    )


@admin.register(Setting)
class SettingAdmin(admin.ModelAdmin):
    inlines = (CustomCommandInline, NoticeInline)
    fieldsets = (
        ('User', {'fields': ('user',)}),
        ('Settings', {'fields': (
            'default_commands', 'antispam', 'follow_notification',
            'follow_notification_text', 'banned_words'
        )}),
    )


admin.site.register(User, CustomUserAdmin)
admin.site.register(CustomCommand)
admin.site.register(Notice)
