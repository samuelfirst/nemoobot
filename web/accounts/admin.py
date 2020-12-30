from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User, Token, Setting


class TokenInline(admin.TabularInline):
    model = Token
    readonly_fields = (
        'access_token', 'refresh_token', 'expires_in', 'expires_time',
    )


@admin.register(Token)
class TokenAdmin(admin.ModelAdmin):
    list_display = ('access_token', 'user',)
    readonly_fields = (
        'access_token', 'refresh_token', 'expires_in', 'expires_time', 'user'
    )

    fieldsets = (
        ('Token', {'fields': (
            'access_token', 'refresh_token', 'expires_in', 'expires_time',
        )}),
        ('User', {'fields': (
            'user',
        )}),
    )


class CustomUserAdmin(UserAdmin):
    inlines = (TokenInline, )
    fieldsets = UserAdmin.fieldsets + (
            ('Twitch', {'fields': ('twitch_username', 'twitch_user_id')}),
    )


@admin.register(Setting)
class SettingAdmin(admin.ModelAdmin):
    fieldsets = (
        ('User', {'fields': ('user',)}),
        ('Settings', {'fields': (
            'default_commands', 'custom_commands', 'antispam'
        )}),
    )


admin.site.register(User, CustomUserAdmin)
