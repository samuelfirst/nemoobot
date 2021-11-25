from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    path(
        'login/',
        auth_views.LoginView.as_view(template_name='login.html'),
        name='login'
    ),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('', include('accounts.urls')),
    path('webhooks/', include('twitch_webhook.urls')),
    path('api/v1/', include('api.urls'))
    path('api/v1/accounts', include())
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
