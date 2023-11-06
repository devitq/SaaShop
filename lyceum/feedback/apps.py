from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _

__all__ = ("FeedbackConfig",)


class FeedbackConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "feedback"
    verbose_name = _("feedback")
