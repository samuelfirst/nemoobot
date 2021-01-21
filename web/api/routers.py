from rest_framework import routers
from api import views as api_views

router = routers.DefaultRouter()
router.register(r'users', api_views.UserViewSet)
router.register(r'tokens', api_views.TokenViewSet)
router.register(r'settings', api_views.SettingViewSet)
router.register(r'custom_commands', api_views.CustomCommandsViewSet)
