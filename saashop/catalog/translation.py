from modeltranslation.translator import register, TranslationOptions

from catalog.models import Category, Item, Tag

__all__ = ()


@register(Item)
class ItemTranslationOptions(TranslationOptions):
    fields = (Item.name.field.name, Item.text.field.name)


@register(Tag)
class TagTranslationOptions(TranslationOptions):
    fields = (Tag.name.field.name,)


@register(Category)
class CategoryTranslationOptions(TranslationOptions):
    fields = (Category.name.field.name,)
