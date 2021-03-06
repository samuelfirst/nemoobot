from django.urls import path, include
from .routers import router
from .views import UserCreateView

urlpatterns = [
    path('', include(router.urls)),
    path('', include('rest_framework.urls', namespace='api')),
    path('signup/', UserCreateView.as_view(), name='signup')
]
