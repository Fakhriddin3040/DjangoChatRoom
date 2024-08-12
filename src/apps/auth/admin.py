from django.contrib import admin

from src.apps.auth.models import User, Profile

admin.site.register((User, Profile))
