from django.apps import AppConfig


class ChatAppConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "src.apps.chat"
    label = "chat"
