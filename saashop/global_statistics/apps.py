from django.apps import AppConfig


__all__ = ("GlobalStatisticsConfig",)


class GlobalStatisticsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "global_statistics"
    verbose_name = "статистика"
