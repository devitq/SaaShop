from datetime import datetime
from pathlib import Path
import uuid

from django.core.validators import (
    MaxValueValidator,
    MinValueValidator,
)
from django.db import models
from django.utils.html import mark_safe
import django_cleanup
import sorl.thumbnail
from tinymce.models import HTMLField

from catalog.validators import ValidateMustContain
from core.models import AddUniqueName, CoreModel

__all__ = ()

BASE_DIR = Path(__file__).resolve().parent.parent


def get_file_path_for_main_image(instance, filename):
    filename = str(uuid.uuid4()) + "." + filename.split(".")[-1]
    return "main_image/{0}/{1}".format(
        datetime.now().strftime("%Y.%m.%d"),
        filename,
    )


def get_file_path_for_images(instance, filename):
    filename = str(uuid.uuid4()) + "." + filename.split(".")[-1]
    return "images/{0}/{1}".format(
        datetime.now().strftime("%Y.%m.%d"),
        filename,
    )


class Tag(CoreModel, AddUniqueName):
    slug = models.SlugField(
        "слаг",
        max_length=200,
        unique=True,
        help_text="a-z, 0-9, _, -",
    )

    class Meta:
        verbose_name = "тег"
        verbose_name_plural = "теги"


class Category(CoreModel, AddUniqueName):
    slug = models.SlugField(
        "слаг",
        max_length=200,
        unique=True,
        help_text="a-z, 0-9, _, -",
    )
    weight = models.PositiveSmallIntegerField(
        "вес",
        default=100,
        validators=[MinValueValidator(1), MaxValueValidator(32767)],
    )

    class Meta:
        verbose_name = "категория"
        verbose_name_plural = "категории"


class MainImage(models.Model):
    main_image = models.ImageField(
        "основное изображение",
        upload_to=get_file_path_for_main_image,
    )

    def get_thumbnail(
        self,
        thumb_height=300,
        thumb_width=300,
        thumb_quality=51,
    ):
        return sorl.thumbnail.get_thumbnail(
            self.main_image,
            f"{thumb_width}x{thumb_height}",
            quality=thumb_quality,
        )

    def image_tmb(self):
        if self.main_image:
            return mark_safe(
                f"<img src='{self.get_thumbnail().url}' width='300'",
            )
        return "Изображение отсутствует"

    image_tmb.short_description = "превью"
    image_tmb.allow_tags = True

    class Meta:
        verbose_name = "основное изображение"
        verbose_name_plural = "основные изображения"


class Item(CoreModel):
    text = HTMLField(
        "текст",
        validators=[ValidateMustContain("превосходно", "роскошно")],
        help_text=(
            'Описание должно содержать слово "превосходно" или "роскошно"'
        ),
    )
    tags = models.ManyToManyField(
        Tag,
        verbose_name="теги",
        blank=True,
        help_text="Выберите теги(необязательно)",
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name="категория",
        blank=True,
        help_text="Выберите категорию(необязательно)",
    )
    main_image = models.OneToOneField(
        MainImage,
        verbose_name="основное изображение",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )

    class Meta:
        verbose_name = "товар"
        verbose_name_plural = "товары"


class ItemImages(models.Model):
    item = models.ForeignKey(
        Item,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name="товар",
        related_name="images",
    )
    image = models.ImageField(
        "изображение",
        upload_to=get_file_path_for_images,
        null=True,
    )

    class Meta:
        verbose_name = "фотография для товаров"
        verbose_name_plural = "фотографии для товаров"


def sorl_delete(**kwargs):
    sorl.thumbnail.delete(kwargs["file"])


django_cleanup.signals.cleanup_pre_delete.connect(sorl_delete)
