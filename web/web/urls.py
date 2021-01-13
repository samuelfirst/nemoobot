from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from rest_framework import routers

from accounts import views as accounts_views

router = routers.DefaultRouter()
router.register(r'users', accounts_views.UserViewSet)
router.register(r'tokens', accounts_views.TokenViewSet)
router.register(r'settings', accounts_views.SettingViewSet)
router.register(r'custom_commands', accounts_views.CustomCommandsViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', accounts_views.index, name='index'),
    path(
        'login/',
        auth_views.LoginView.as_view(template_name='login.html'),
        name='login'
    ),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('signup/', accounts_views.signup, name='signup'),
    path(
        'connect_to_twitch/',
        accounts_views.connect_to_twicth,
        name='connect_to_twitch'),
    path('profile/', accounts_views.profile, name='profile'),
    path('settings/', accounts_views.settings, name='settings'),
    path('api/v1/', include(router.urls)),
    path('api/v1/', include('rest_framework.urls', namespace='rest_framework')),
]
