from django.contrib import admin

from .models import Subscription


@admin.register(Subscription)
class TokenAdmin(admin.ModelAdmin):
    list_display = ('type', 'user',)
    readonly_fields = (
        'user', 'type', 'created_at',
    )
