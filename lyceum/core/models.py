import re

from django.core.exceptions import ValidationError
from django.db import models
from transliterate import translit
from transliterate.discover import autodiscover

__all__ = ("AddUniqueName", "CoreModel")


autodiscover()


class CoreModel(models.Model):
    is_published = models.BooleanField("опубликовано", default=True)
    name = models.CharField(
        "название",
        max_length=150,
        unique=True,
        help_text="Не больше 150 символов",
    )

    class Meta:
        abstract = True

    def __str__(self) -> str:
        return self.name


class AddUniqueName(models.Model):
    unique_name = models.CharField(
        "уникальное название",
        max_length=150,
        unique=True,
        editable=False,
        help_text="Сгенерированное название для унификации",
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
                "Элемент с таким же похожим именем уже существует",
            )

    class Meta:
        abstract = True
