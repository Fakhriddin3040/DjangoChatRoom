from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import CustomTokenObtainPairView, CustomTokenRefreshView
from .views import (
    profile_view,
    profile_edit_view,
    profile_settings_view,
    profile_emailchange,
    profile_emailverify,
    profile_delete_view,
)

router = DefaultRouter()

urlpatterns = [
    path("login/", CustomTokenObtainPairView.as_view(), name="login"),
    path("login/refresh/", CustomTokenRefreshView.as_view(), name="refresh-token"),
]

view_urlpatterns = [
    path("", profile_view, name="profile"),
    path("edit/", profile_edit_view, name="profile-edit"),
    path("onboarding/", profile_edit_view, name="profile-onboarding"),
    path("settings/", profile_settings_view, name="profile-settings"),
    path("emailchange/", profile_emailchange, name="profile-emailchange"),
    path("emailverify/", profile_emailverify, name="profile-emailverify"),
    path("delete/", profile_delete_view, name="profile-delete"),
    # path("", home_view, name="home"),
]

