from datetime import datetime
from pathlib import Path
import uuid

from django.core.validators import (
    MaxValueValidator,
    MinValueValidator,
)
from django.db import models
from django.utils.html import mark_safe
from django.utils.translation import gettext_lazy as _
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
        _("slug_models"),
        max_length=200,
        unique=True,
        help_text="a-z, 0-9, _, -",
    )

    class Meta:
        verbose_name = _("tag_models")
        verbose_name_plural = _("tags_models")


class Category(CoreModel, AddUniqueName):
    slug = models.SlugField(
        _("slug_models"),
        max_length=200,
        unique=True,
        help_text="a-z, 0-9, _, -",
    )
    weight = models.PositiveSmallIntegerField(
        _("weight_models"),
        default=100,
        validators=[MinValueValidator(1), MaxValueValidator(32767)],
    )

    class Meta:
        verbose_name = _("category_models")
        verbose_name_plural = _("categories_models")


class MainImage(models.Model):
    main_image = models.ImageField(
        _("image_models"),
        upload_to=get_file_path_for_main_image,
    )

    def get_image_300x300(self):
        return sorl.thumbnail.get_thumbnail(
            self.main_image,
            "300x300",
            quolity=51,
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
                f"<img src='{self.get_image_300x300().url}' width='300'",
            )
        return _("no_image")

    image_tmb.short_description = _("preview")
    image_tmb.allow_tags = True

    def __str__(self) -> str:
        verbose = _("main_image_models").capitalize()
        return f"{verbose}, ID:{self.id}"

    class Meta:
        verbose_name = _("main_image_models")
        verbose_name_plural = _("main_images_models")


class ItemManager(models.Manager):
    def on_main(self):
        return (
            self.get_queryset()
            .select_related(Item.category.field.name)
            .filter(
                is_on_main=True,
                is_published=True,
                category__is_published=True,
            )
            .prefetch_related(
                models.Prefetch(
                    Item.tags.field.name,
                    queryset=Tag.objects.filter(is_published=True)
                    .order_by(Tag.name.field.name)
                    .only(
                        Tag.name.field.name,
                    ),
                ),
            )
            .only(
                Item.id.field.name,
                Item.name.field.name,
                Item.text.field.name,
                f"{Item.category.field.name}__{Category.name.field.name}",
            )
        )

    def published(self):
        return (
            self.get_queryset()
            .select_related(Item.category.field.name)
            .prefetch_related(
                models.Prefetch(
                    Item.tags.field.name,
                    queryset=Tag.objects.filter(is_published=True)
                    .order_by(Tag.name.field.name)
                    .only(
                        Tag.name.field.name,
                    ),
                ),
            )
            .filter(is_published=True, category__is_published=True)
            .only(
                Item.id.field.name,
                Item.name.field.name,
                Item.text.field.name,
                f"{Item.category.field.name}__{Category.name.field.name}",
            )
            .order_by(
                f"{Item.category.field.name}__{Category.name.field.name}",
            )
        )

    def item_detail(self, item_id):
        return (
            self.get_queryset()
            .filter(id=item_id)
            .select_related(Item.category.field.name)
            .select_related(Item.main_image.field.name)
            .prefetch_related(
                models.Prefetch(
                    Item.tags.field.name,
                    queryset=Tag.objects.filter(is_published=True)
                    .order_by(Tag.name.field.name)
                    .only(
                        Tag.name.field.name,
                    ),
                ),
            )
            .prefetch_related(
                models.Prefetch(
                    "images",
                    queryset=ItemImages.objects.only(
                        ItemImages.image.field.name,
                        "item_id",
                    ),
                ),
            )
            .filter(is_published=True, category__is_published=True)
            .only(
                Item.id.field.name,
                Item.name.field.name,
                Item.text.field.name,
                f"{Item.category.field.name}__{Category.name.field.name}",
                (
                    f"{Item.main_image.field.name}__"
                    f"{MainImage.main_image.field.name}"
                ),
            )
        )


class Item(CoreModel):
    objects = ItemManager()

    is_on_main = models.BooleanField(_("show_on_main_models"), default=False)
    text = HTMLField(
        _("text_models"),
        validators=[
            ValidateMustContain(
                "превосходно",
                "роскошно",
                "perfect",
                "luxurious",
            ),
        ],
        help_text=(_("text_should_contain")),
    )
    created_at = models.DateTimeField(
        _("created_at_utc_models"),
        null=True,
        auto_now_add=True,
    )
    updated_at = models.DateTimeField(
        _("updated_at_utc_models"),
        null=True,
        auto_now=True,
    )
    tags = models.ManyToManyField(
        Tag,
        verbose_name=_("tags_models"),
        blank=True,
        related_query_name="tag",
        help_text=_("choose_tags_non_required"),
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        null=True,
        verbose_name=_("category_models"),
        blank=True,
        related_name="item",
        related_query_name="category",
        help_text=_("choose_category_non_required"),
    )
    main_image = models.OneToOneField(
        MainImage,
        verbose_name=_("main_image_models"),
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )

    class Meta:
        ordering = ("name", "id")
        verbose_name = _("item_models")
        verbose_name_plural = _("items_models")


class ItemImages(models.Model):
    item = models.ForeignKey(
        Item,
        on_delete=models.SET_NULL,
        null=True,
        related_query_name="images",
        verbose_name=_("item_models"),
        related_name="images",
    )
    image = models.ImageField(
        _("image_models"),
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
            self.image,
            f"{thumb_width}x{thumb_height}",
            quality=thumb_quality,
        )

    def image_tmb(self):
        if self.image:
            return mark_safe(
                f"<img src='{self.get_thumbnail().url}' width='300'",
            )
        return _("no_image")

    image_tmb.short_description = _("preview")
    image_tmb.allow_tags = True

    def __str__(self) -> str:
        verbose = _("item_image_models").capitalize()
        return f"{verbose}, ID:{self.id}"

    class Meta:
        verbose_name = _("item_image_models")
        verbose_name_plural = _("item_images_models")


def sorl_delete(**kwargs):
    sorl.thumbnail.delete(kwargs["file"])


django_cleanup.signals.cleanup_pre_delete.connect(sorl_delete)
