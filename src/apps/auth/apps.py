from django.apps import AppConfig


class AuthConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "src.apps.auth"
    label = "authorization"

    def ready(self) -> None:
        from . import signals  # noqa

        return super().ready()
