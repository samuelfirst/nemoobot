from django.urls import path, include
from .routers import router

urlpatterns = [
    path('', include(router.urls)),
    path('', include('rest_framework.urls', namespace='api'))
]
