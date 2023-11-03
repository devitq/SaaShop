import re

from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import gettext_lazy as _
from transliterate import translit
from transliterate.discover import autodiscover

__all__ = ("AddUniqueName", "CoreModel")


autodiscover()


class CoreModel(models.Model):
    name = models.CharField(
        _("title_models"),
        max_length=150,
        unique=True,
        help_text=_("no_more_than_150"),
    )
    is_published = models.BooleanField(_("published_models"), default=True)

    class Meta:
        abstract = True

    def __str__(self) -> str:
        return self.name


class AddUniqueName(models.Model):
    unique_name = models.CharField(
        _("unique_name_models"),
        max_length=150,
        unique=True,
        editable=False,
        help_text=_("generated_name_for_unique"),
        null=True,
    )

    def save(self, *args, **kwargs):
        self.unique_name = re.sub(
            r"[^\w]",
            "",
            translit(self.name, "ru", reversed=True).lower(),
        )
        super().save(*args, **kwargs)

    def clean(self, *args, **kwargs):
        self.generated_unique_name = re.sub(
            r"[^\w]",
            "",
            translit(self.name, "ru", reversed=True).lower(),
        )
        if (
            self._meta.model.objects.filter(
                unique_name=self.generated_unique_name,
            )
            .exclude(id=self.id)
            .count()
            > 0
        ):
            raise ValidationError(
                _("item_with_similar_name_exist"),
            )

    class Meta:
        abstract = True
