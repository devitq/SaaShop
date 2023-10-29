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

        cls.category_published = Category.objects.create(
            is_published=True,
            name="Тестовая категория 1",
            slug="test_category1",
            weight=100,
        )
        cls.category_unpublished = Category.objects.create(
            is_published=False,
            name="Тестовая категория 2",
            slug="test_category2",
            weight=100,
        )

        cls.tag_published = Tag.objects.create(
            is_published=True,
            name="Тестовый тег 1",
            slug="test_tag1",
        )
        cls.tag_unpublished = Tag.objects.create(
            is_published=True,
            name="Тестовый тег 2",
            slug="test_tag2",
        )

        cls.item_published = Item(
            name="Тест 1",
            text="превосходно",
        )
        cls.item_unpublished = Item(
            name="Тест 2",
            text="превосходно",
        )

        cls.category_published.save()
        cls.category_unpublished.save()

        cls.tag_published.save()
        cls.tag_unpublished.save()

        cls.item_published.clean()
        cls.item_published.save()
        cls.item_unpublished.clean()
        cls.item_unpublished.save()

        cls.item_published.tags.add(cls.tag_published.pk)
        cls.item_published.tags.add(cls.tag_unpublished)

    def test_item_list_context(self):
        response = Client().get(reverse("catalog:item_list"))
        self.assertIn("items", response.context)

    def test_item_list_count_item(self):
        response = Client().get(reverse("catalog:item_list"))
        items = response.context["items"]
        self.assertEqual(items.count(), 2)


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
