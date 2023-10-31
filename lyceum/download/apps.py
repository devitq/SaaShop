from django.apps import AppConfig

__all__ = ("DownloadConfig",)


class DownloadConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "download"
