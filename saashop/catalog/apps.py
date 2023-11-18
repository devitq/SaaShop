from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _

__all__ = ("CatalogConfig",)


class CatalogConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "catalog"
    verbose_name = _("catalog_app")
