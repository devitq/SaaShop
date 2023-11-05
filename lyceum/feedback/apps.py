from django.apps import AppConfig

__all__ = ("FeedbackConfig",)


class FeedbackConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "feedback"
    verbose_name = "Обратная связь"
