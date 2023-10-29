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

__all__ = ("Category", "Item", "ItemImages", "MainImage", "Tag")

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


class ItemManager(models.Manager):
    def homepage(self):
        return (
            self.get_queryset()
            .select_related("category")
            .filter(
                is_on_main=True,
                is_published=True,
                category__is_published=True,
            )
            .prefetch_related(
                models.Prefetch(
                    "tags",
                    queryset=Tag.objects.filter(is_published=True).only(
                        "name",
                    ),
                ),
            )
            .only("id", "name", "text", "category__name")
        )

    def item_list(self):
        return (
            self.get_queryset()
            .select_related("category")
            .prefetch_related(
                models.Prefetch(
                    "tags",
                    queryset=Tag.objects.filter(is_published=True).only(
                        "name",
                    ),
                ),
            )
            .filter(is_published=True, category__is_published=True)
            .only("id", "name", "text", "category__name")
            .order_by("category__name")
        )

    def item_detail(self):
        return (
            self.get_queryset()
            .select_related("category")
            .select_related("main_image")
            .prefetch_related(
                models.Prefetch(
                    "tags",
                    queryset=Tag.objects.filter(is_published=True).only(
                        "name",
                    ),
                ),
            )
            .prefetch_related(
                models.Prefetch(
                    "images",
                    queryset=ItemImages.objects.only(
                        "image",
                        "item_id",
                    ),
                ),
            )
            .filter(is_published=True, category__is_published=True)
            .only(
                "id",
                "name",
                "text",
                "category__name",
                "main_image__main_image",
            )
        )


class Item(CoreModel):
    objects = ItemManager()

    is_on_main = models.BooleanField("отображать на главной", default=False)
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
        related_query_name="tag",
        help_text="Выберите теги(необязательно)",
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        null=True,
        verbose_name="категория",
        blank=True,
        related_query_name="category",
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
        ordering = ("name", "id")
        verbose_name = "товар"
        verbose_name_plural = "товары"


class ItemImages(models.Model):
    item = models.ForeignKey(
        Item,
        on_delete=models.SET_NULL,
        null=True,
        related_query_name="images",
        verbose_name="товар",
        related_name="images",
    )
    image = models.ImageField(
        "изображение",
        upload_to=get_file_path_for_images,
        null=True,
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

    class Meta:
        verbose_name = "фотография для товаров"
        verbose_name_plural = "фотографии для товаров"


def sorl_delete(**kwargs):
    sorl.thumbnail.delete(kwargs["file"])


django_cleanup.signals.cleanup_pre_delete.connect(sorl_delete)
