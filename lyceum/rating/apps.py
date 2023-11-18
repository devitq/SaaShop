from django.apps import AppConfig

__all__ = ("RatingConfig",)


class RatingConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "rating"
