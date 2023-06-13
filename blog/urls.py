from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("posts.urls")),
    path("", include("users.urls")),
    path("", include('allauth.urls')),
    path("accounts/", include("django.contrib.auth.urls")),
    path("api/", include("api.urls")),
    path('api-auth/', include('rest_framework.urls')),
    path('auth/', include('djoser.urls'))
]
urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root = settings.STATIC_ROOT)
