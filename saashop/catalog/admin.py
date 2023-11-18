from django.contrib import admin
from django.db import models
from django.utils.translation import gettext_lazy as _
from modeltranslation.admin import TranslationAdmin
from tinymce.widgets import AdminTinyMCE

from catalog.models import Category, Item, ItemImages, MainImage, Tag

__all__ = ()

admin.site.site_header = _("saashop_admin_panel_header")
admin.site.site_title = _("saashop_admin_panel_title")
admin.site.index_title = _("saashop_admin_panel_index_title")


class ImagesInline(admin.TabularInline):
    model = ItemImages
    extra = 1


class MainImageAdmin(admin.ModelAdmin):
    list_display = (MainImage.image_tmb,)


class ItemImagesAdmin(admin.ModelAdmin):
    list_display = (ItemImages.image_tmb,)


class CatalogItemAdmin(TranslationAdmin):
    list_display = [
        Item.name.field.name,
        Item.is_published.field.name,
        Item.is_on_main.field.name,
        "preview",
        Item.created_at.field.name,
        Item.updated_at.field.name,
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
    readonly_fields = [
        "preview",
        Item.created_at.field.name,
        Item.updated_at.field.name,
    ]
    formfield_overrides = {
        models.TextField: {"widget": AdminTinyMCE},
    }

    def preview(self, obj):
        if obj.main_image:
            return obj.main_image.image_tmb()
        return _("no_image")

    preview.short_description = _("preview")
    preview.allow_tags = True


class AutoGenSlug(TranslationAdmin):
    prepopulated_fields = {"slug": ("name",)}


admin.site.register(Item, CatalogItemAdmin)
admin.site.register(Tag, AutoGenSlug)
admin.site.register(Category, AutoGenSlug)
admin.site.register(MainImage, MainImageAdmin)
admin.site.register(ItemImages, ItemImagesAdmin)
