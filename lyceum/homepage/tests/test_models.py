from django.test import Client, TestCase
from django.urls import reverse

from catalog.models import Category, Item, Tag

__all__ = ()


class ModelsTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.published_category = Category.objects.create(
            is_published=True,
            name="Опубликованная категория",
            slug="published_category",
            weight=100,
        )
        cls.unpublished_category = Category.objects.create(
            is_published=False,
            name="Неопубликованная категория",
            slug="unpublished_category",
            weight=100,
        )
        cls.published_tag = Tag.objects.create(
            is_published=True,
            name="Опубликованный тэг",
            slug="published_tag",
        )
        cls.unpublished_tag = Tag.objects.create(
            is_published=False,
            name="Неопубликованный тэг",
            slug="unpublished_tag",
        )
        cls.pub_item_right_cat = Item.objects.create(
            is_published=True,
            name="Товар с опубликованной категорией",
            text="превосходно",
            category=cls.published_category,
        )
        cls.pub_item_wrong_cat = Item.objects.create(
            is_published=True,
            name="Товар с неопубликованной категорией",
            text="превосходно",
            category=cls.unpublished_category,
        )
        cls.pub_item_right_tag = Item.objects.create(
            is_published=True,
            name="Товар с опубликованным тэгом",
            text="превосходно",
            category=cls.published_category,
        )
        cls.pub_item_wrong_tag = Item.objects.create(
            is_published=True,
            name="Товар с неопубликованным тэгом",
            text="превосходно",
            category=cls.published_category,
        )
        cls.unpub_item = Item.objects.create(
            is_published=False,
            name="Неопубликованный товар",
            text="превосходно",
            category=cls.published_category,
        )
        cls.pub_item_not_in_main = Item.objects.create(
            is_published=True,
            name="Товар не на главной",
            text="превосходно",
            category=cls.published_category,
        )
        cls.pub_item_in_main = Item.objects.create(
            is_on_main=True,
            is_published=True,
            name="Товар на главной",
            text="превосходно",
            category=cls.published_category,
        )
        cls.pub_item_right_tag.tags.add(cls.published_tag.pk)
        cls.pub_item_wrong_tag.tags.add(cls.unpublished_tag.pk)

    def test_getting_right_context(self):
        response = Client().get(reverse("homepage:homepage"))
        self.assertIn("items", response.context)
        self.assertIn("features", response.context)

    def test_item_count(self):
        response = Client().get(reverse("homepage:homepage"))
        items = response.context["items"]
        self.assertEqual(items.count(), 1)

    def test_item_categories(self):
        response = Client().get(reverse("homepage:homepage"))
        items = response.context["items"]
        for item in items:
            self.assertNotEqual(
                item.category,
                self.unpublished_category,
            )

    def test_item_tags(self):
        response = Client().get(reverse("homepage:homepage"))
        items = response.context["items"]
        for item in items:
            self.assertNotIn(
                self.unpublished_tag,
                item.tags.all(),
            )

    def test_unpublished_items(self):
        response = Client().get(reverse("homepage:homepage"))
        items = response.context["items"]
        self.assertNotIn(self.unpub_item, items)

    def test_item_not_on_main(self):
        response = Client().get(reverse("homepage:homepage"))
        items = response.context["items"]
        self.assertNotIn(self.pub_item_not_in_main, items)
