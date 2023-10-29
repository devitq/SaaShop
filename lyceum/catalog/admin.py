from django.contrib import admin
from django.db import models
from tinymce.widgets import AdminTinyMCE

from catalog.models import Category, Item, ItemImages, MainImage, Tag

__all__ = ()


class ImagesInline(admin.TabularInline):
    model = ItemImages
    extra = 1


class MainImageAdmin(admin.ModelAdmin):
    list_display = (MainImage.image_tmb,)


class CatalogItemAdmin(admin.ModelAdmin):
    list_display = [
        Item.name.field.name,
        Item.is_published.field.name,
        Item.is_on_main.field.name,
        "preview",
    ]
    list_editable = [
        Item.is_published.field.name,
        Item.is_on_main.field.name,
    ]
    list_display_links = [Item.name.field.name]
    filter_horizontal = [Item.tags.field.name]
    inlines = [
        ImagesInline,
    ]
    readonly_fields = ["preview"]
    formfield_overrides = {
        models.TextField: {"widget": AdminTinyMCE},
    }

    def preview(self, obj):
        if obj.main_image:
            return obj.main_image.image_tmb()
        return "Изображение отсутсвует"

    preview.short_description = "превью"
    preview.allow_tags = True


class AutoGenSlug(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}


admin.site.register(Item, CatalogItemAdmin)
admin.site.register(Tag, AutoGenSlug)
admin.site.register(Category, AutoGenSlug)
admin.site.register(MainImage, MainImageAdmin)
admin.site.register(ItemImages)
