from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    # path('signup/', views.signup, name='signup'),
    path(
        'connect_to_twitch/',
        views.connect_to_twicth,
        name='connect_to_twitch'
    ),
    path('profile/', views.profile, name='profile'),
    path('settings/', views.settings, name='settings'),
]
