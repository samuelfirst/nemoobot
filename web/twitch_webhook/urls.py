from django.urls import path
from . import views

urlpatterns = [
    path('follows/<int:twitch_user_id>/', views.follows_webhook, name='follows'),
]
