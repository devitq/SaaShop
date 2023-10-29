from http import HTTPStatus

from django.core.exceptions import ValidationError
from django.test import Client, override_settings, TestCase
from django.urls import reverse
from django.urls.exceptions import NoReverseMatch
import parameterized

from catalog.models import Category, Item, Tag

__all__ = ("DynamicURLTests", "ModelsTests", "StaticURLTests")


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

    @parameterized.parameterized.expand(
        [("Привет how?., дела А!_.,;:!?-()", "привет how делаа_")],
    )
    def test_name_tag(self, name1, name2):
        tag_count = Tag.objects.count()
        tag = Tag(name=name1, slug="fsd")
        tag.full_clean()
        tag.save()

        with self.assertRaises(ValidationError):
            self.tag1 = Tag(name=name2, slug="gdsfsd")
            self.tag1.full_clean()
            self.tag1.save()

        self.assertEqual(Tag.objects.count(), tag_count + 1)

    def test_unable_to_create_item_without_words(self):
        item_count = Item.objects.count()
        with self.assertRaises(ValidationError):
            self.item = Item(
                name="Тест",
                category=self.category_published,
                text="тест",
            )
            self.item.full_clean()
            self.item.save()
            self.item.tags.add(ModelsTests.tag_published)

        self.assertEqual(Item.objects.count(), item_count)

    def test_create_item(self):
        item_count = Item.objects.count()
        self.item = Item(
            name="Тест",
            category=self.category_published,
            text="превосходно",
        )
        self.item.full_clean()
        self.item.save()
        self.item.tags.add(ModelsTests.tag_published)

        self.assertEqual(Item.objects.count(), item_count + 1)

    def test_unable_create_item_core_unique(self):
        item_count = Item.objects.count()
        self.item = Item(name="Тестовый продукт", text="Превосходно")
        self.item.full_clean()
        self.item.save()
        with self.assertRaises(ValidationError):
            self.item = Item(name="Тестовый продукт", text="Превосходно")
            self.item.full_clean()
            self.item.save()

        self.assertEqual(Item.objects.count(), item_count + 1)

    @parameterized.parameterized.expand(
        [("Привет how?., дела А!_.,;:!?-()", "привет how делаа_")],
    )
    def test_name_category(self, name1, name2):
        category_count = Category.objects.count()
        category = Category(name=name1, slug="fsd")
        category.full_clean()
        category.save()

        with self.assertRaises(ValidationError):
            self.category1 = Category(name=name2, slug="gdsfsd")
            self.category1.full_clean()
            self.category1.save()

        self.assertEqual(Category.objects.count(), category_count + 1)


class StaticURLTests(TestCase):
    @override_settings(ALLOW_REVERSE=False)
    def test_item_list_endpoint(self):
        response = Client().get(reverse("catalog:item_list"))
        self.assertEqual(
            response.status_code,
            HTTPStatus.OK,
        )


class DynamicURLTests(TestCase):
    def test_unusual_item_detail_endpoint(self):
        with self.assertRaises(NoReverseMatch):
            unusual_response1 = Client().get(
                reverse("catalog:item_detail", args=[-1]),
            )
            self.assertEqual(
                unusual_response1.status_code,
                HTTPStatus.NOT_FOUND,
            )

            unusual_response2 = Client().get(
                reverse("catalog:item_detail", args=["text"]),
            )
            self.assertEqual(
                unusual_response2.status_code,
                HTTPStatus.NOT_FOUND,
            )

            unusual_response3 = Client().get(
                reverse("catalog:item_detail", args=[1.1]),
            )
            self.assertEqual(
                unusual_response3.status_code,
                HTTPStatus.NOT_FOUND,
            )

    def test_re_item_detail_endpoint(self):
        usual_response = Client().get(
            reverse("catalog:re_item_detail", args=[1]),
        )
        self.assertContains(usual_response, "1", status_code=HTTPStatus.OK)

    def test_unusual_re_item_detail_endpoint(self):
        with self.assertRaises(NoReverseMatch):
            unusual_response1 = Client().get(
                reverse("catalog:re_item_detail", args=[-1]),
            )
            self.assertEqual(
                unusual_response1.status_code,
                HTTPStatus.NOT_FOUND,
            )

            unusual_response2 = Client().get(
                reverse("catalog:re_item_detail", args=[0]),
            )
            self.assertEqual(
                unusual_response2.status_code,
                HTTPStatus.NOT_FOUND,
            )

            unusual_response3 = Client().get(
                reverse("catalog:re_item_detail", args=[1.1]),
            )
            self.assertEqual(
                unusual_response3.status_code,
                HTTPStatus.NOT_FOUND,
            )

            unusual_response4 = Client().get(
                reverse("catalog:re_item_detail", args=[-1]),
            )
            self.assertEqual(
                unusual_response4.status_code,
                HTTPStatus.NOT_FOUND,
            )

    def test_convert_item_detail_endpoint(self):
        usual_response = Client().get(
            reverse("catalog:converter_item_detail", args=[1]),
        )
        self.assertContains(usual_response, "1", status_code=HTTPStatus.OK)

    def test_unusual_convert_item_detail_endpoint(self):
        with self.assertRaises(NoReverseMatch):
            unusual_response1 = Client().get(
                reverse("catalog:converter_item_detail", args=[0]),
            )
            self.assertEqual(
                unusual_response1.status_code,
                HTTPStatus.NOT_FOUND,
            )

            unusual_response2 = Client().get(
                reverse("catalog:converter_item_detail", args=["text"]),
            )
            self.assertEqual(
                unusual_response2.status_code,
                HTTPStatus.NOT_FOUND,
            )

            unusual_response3 = Client().get(
                reverse("catalog:converter_item_detail", args=[1.1]),
            )
            self.assertEqual(
                unusual_response3.status_code,
                HTTPStatus.NOT_FOUND,
            )

            unusual_response4 = Client().get(
                reverse("catalog:converter_item_detail", args=[-1]),
            )
            self.assertEqual(
                unusual_response4.status_code,
                HTTPStatus.NOT_FOUND,
            )
