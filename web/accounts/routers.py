from rest_framework import routers

from views import TokenViewSet, UserViewSet

router = routers.DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'tokens', TokenViewSet)
