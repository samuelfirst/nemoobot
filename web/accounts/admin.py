from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User, Token


class TokenInline(admin.TabularInline):
    model = Token
    readonly_fields = ('access_token', 'refresh_token', 'expires_in')


@admin.register(Token)
class TokenAdmin(admin.ModelAdmin):
    list_display = ('access_token', 'user',)
    readonly_fields = ('access_token', 'refresh_token', 'expires_in', 'user')

    fieldsets = (
        ('Token', {'fields': ('access_token', 'refresh_token', 'expires_in',)}),
        ('User', {'fields': ('user',)}),
    )


class CustomUserAdmin(UserAdmin):
    inlines = (TokenInline, )
    fieldsets = UserAdmin.fieldsets + (
            ('Twitch', {'fields': ('twitch_username', 'twitch_user_id')}),
    )


admin.site.register(User, CustomUserAdmin)
