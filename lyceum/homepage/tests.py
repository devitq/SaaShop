from http import HTTPStatus

from django.test import Client, override_settings, TestCase
from django.urls import reverse

from catalog.models import Category, Item, Tag
from lyceum import settings

__all__ = ("RussianReverseTests", "StaticURLTests")


class ModelsTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.published_category = Category(
            is_published=True,
            name="Опубликованная категория",
            slug="published_category",
            weight=100,
        )
        cls.unpublished_category = Category(
            is_published=False,
            name="Неопубликованная категория",
            slug="unpublished_category",
            weight=100,
        )

        cls.published_tag = Tag(
            is_published=True,
            name="Опубликованный тэг",
            slug="published_tag",
        )
        cls.unpublished_tag = Tag(
            is_published=False,
            name="Неопубликованный тэг",
            slug="unpublished_tag",
        )

        cls.pub_item_right_cat = Item(
            is_published=True,
            name="Товар с опубликованной категорией",
            text="превосходно",
            category=cls.published_category,
        )
        cls.pub_item_wrong_cat = Item(
            is_published=True,
            name="Товар с неопубликованной категорией",
            text="превосходно",
            category=cls.unpublished_category,
        )
        cls.pub_item_right_tag = Item(
            is_published=True,
            name="Товар с опубликованным тэгом",
            text="превосходно",
            category=cls.published_category,
        )
        cls.pub_item_wrong_tag = Item(
            is_published=True,
            name="Товар с неопубликованным тэгом",
            text="превосходно",
            category=cls.published_category,
        )
        cls.unpub_item = Item(
            is_published=False,
            name="Неопубликованный товар",
            text="превосходно",
            category=cls.published_category,
        )
        cls.pub_item_not_in_main = Item(
            is_published=True,
            name="Товар не на главной",
            text="превосходно",
            category=cls.published_category,
        )

        cls.published_category.save()
        cls.unpublished_category.save()

        cls.published_tag.save()
        cls.unpublished_tag.save()

        cls.pub_item_right_cat.clean()
        cls.pub_item_right_cat.save()
        cls.pub_item_wrong_cat.clean()
        cls.pub_item_wrong_cat.save()

        cls.pub_item_right_tag.clean()
        cls.pub_item_right_tag.save()
        cls.pub_item_wrong_tag.clean()
        cls.pub_item_wrong_tag.save()

        cls.pub_item_not_in_main.clean()
        cls.pub_item_not_in_main.save()

        cls.pub_item_right_tag.tags.add(cls.published_tag.pk)
        cls.pub_item_wrong_tag.tags.add(cls.unpublished_tag.pk)

        cls.unpub_item.clean()
        cls.unpub_item.save()

    def test_getting_right_context(self):
        response = Client().get(
            reverse("homepage:homepage"),
        )
        self.assertIn("items", response.context)

    def test_item_count(self):
        response = Client().get(
            reverse("homepage:homepage"),
        )
        items = response.context["items"]
        self.assertEqual(items.count(), 0)

    def test_item_categories(self):
        response = Client().get(
            reverse("homepage:homepage"),
        )
        items = response.context["items"]
        for item in items:
            self.assertNotEqual(
                item.category,
                self.unpublished_category,
            )

    def test_item_tags(self):
        response = Client().get(
            reverse("homepage:homepage"),
        )
        items = response.context["items"]
        for item in items:
            self.assertNotIn(
                self.unpublished_tag,
                item.tags.all(),
            )

    def test_unpublished_items(self):
        response = Client().get(
            reverse("homepage:homepage"),
        )
        items = response.context["items"]
        self.assertNotIn(
            self.unpub_item,
            items,
        )

    def test_item_not_on_main(self):
        response = Client().get(
            reverse("homepage:homepage"),
        )
        items = response.context["items"]
        self.assertNotIn(
            self.pub_item_not_in_main,
            items,
        )


class RussianReverseTests(TestCase):
    @override_settings(ALLOW_REVERSE=True)
    def test_reverse_russian_words_enabled(self):
        contents = {
            Client().get(reverse("homepage:coffee")).content for _ in range(10)
        }
        self.assertIn("Я чайник".encode(), contents)
        self.assertIn("Я кинйач".encode(), contents)

    def test_reverse_russian_words_enabled_default(self):
        if settings.ALLOW_REVERSE:
            contents = {
                Client().get(reverse("homepage:coffee")).content
                for _ in range(10)
            }
            self.assertIn("Я чайник".encode(), contents)
            self.assertIn("Я кинйач".encode(), contents)

    @override_settings(ALLOW_REVERSE=False)
    def test_reverse_russian_words_disabled(self):
        contents = {
            Client().get(reverse("homepage:coffee")).content for _ in range(10)
        }
        self.assertIn("Я чайник".encode(), contents)
        self.assertNotIn("Я кинйач".encode(), contents)


class StaticURLTests(TestCase):
    def test_home_endpoint(self):
        response = Client().get(reverse("homepage:homepage"))
        self.assertEqual(
            response.status_code,
            HTTPStatus.OK,
        )

    @override_settings(ALLOW_REVERSE=False)
    def test_coffee_endpoint(self):
        response = Client().get(reverse("homepage:coffee"))
        self.assertContains(
            response,
            "Я чайник",
            status_code=HTTPStatus.IM_A_TEAPOT,
        )
