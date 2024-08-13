from django.conf import settings
from django.contrib import admin
from django.urls import include, path
from django.conf.urls.static import static

from src.apps.chat import urls as chat_urls
from src.apps.auth.views.profile import profile_view
from src.apps.api import urls as api_urls
from src.apps.auth.urls import view_urlpatterns as auth_views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("accounts/", include("allauth.urls")),
    path("api/v1/", include(api_urls), name="api"),
    path("profile/", include(auth_views), name="auth_views"),
    path("@<username>/", profile_view, name="profile"),
    path("", include(chat_urls), name="profile"),
]

if settings.DEBUG:
    static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
