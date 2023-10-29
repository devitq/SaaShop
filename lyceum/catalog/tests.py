from http import HTTPStatus

from django.core.exceptions import ValidationError
from django.test import Client, override_settings, TestCase
from django.urls import reverse
from django.urls.exceptions import NoReverseMatch
import parameterized

from catalog.models import Category, Item, Tag

__all__ = ("DynamicURLTests", "ModelsTests", "StaticURLTests")


class ItemManagerTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.published_category = Category.objects.create(
            is_published=True,
            name="Опубликованная категория",
            slug="published_category",
            weight=100,
        )

        cls.published_tag = Tag.objects.create(
            is_published=True,
            name="Опубликованный тэг",
            slug="published_tag",
        )

        cls.item_with_all_fields = Item.objects.create(
            is_published=True,
            is_on_main=True,
            name="Товар со всеми полями",
            text="превосходно",
            category=cls.published_category,
            main_image=None,
        )
        cls.item_with_all_fields.tags.add(cls.published_tag)

    def test_published_method_fields(self):
        items = Item.objects.published()

        for item in items:
            self.assertIsNotNone(item.id)
            self.assertIsNotNone(item.name)
            self.assertIsNotNone(item.text)
            self.assertIsNotNone(item.category_id)
            self.assertIsNotNone(item.category.id)
            self.assertIsNotNone(item.category.name)
            self.assertIsNotNone(item.is_published)
            self.assertEqual(len(item.tags.all()), 1)

            self.assertIsNone(item.main_image)
            self.assertEqual(len(item.images.all()), 0)

    def test_on_main_method_fields(self):
        items = Item.objects.on_main()

        for item in items:
            self.assertIsNotNone(item.id)
            self.assertIsNotNone(item.name)
            self.assertIsNotNone(item.text)
            self.assertIsNotNone(item.category_id)
            self.assertIsNotNone(item.category.id)
            self.assertIsNotNone(item.category.name)
            self.assertIsNotNone(item.is_published)
            self.assertEqual(len(item.tags.all()), 1)

            self.assertIsNone(item.main_image)
            self.assertEqual(len(item.images.all()), 0)

    def test_item_detail_method_fields(self):
        item = get_object_or_404(Item.objects.item_detail(), pk=1)
        self.assertIsNotNone(item.id)
        self.assertIsNotNone(item.name)
        self.assertIsNotNone(item.text)
        self.assertIsNotNone(item.category.name)

        self.assertIsNone(item.main_image)
        self.assertEqual(len(item.tags.all()), 1)


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
        cls.pub_item_right_tag.tags.add(cls.published_tag.pk)
        cls.pub_item_wrong_tag.tags.add(cls.unpublished_tag.pk)

    def test_getting_right_context(self):
        response = Client().get(reverse("catalog:item_list"))
        self.assertIn("items", response.context)

    def test_item_count(self):
        response = Client().get(reverse("catalog:item_list"))
        items = response.context["items"]
        self.assertEqual(items.count(), 3)

    def test_item_categories(self):
        response = Client().get(reverse("catalog:item_list"))
        categories = response.context["categories"].all()
        for category in categories:
            for item in category.item.all():
                self.assertNotEqual(
                    item.category,
                    self.unpublished_category,
                )

    def test_item_tags(self):
        response = Client().get(reverse("catalog:item_list"))
        categories = response.context["categories"].all()
        for category in categories:
            for item in category.item.all():
                self.assertNotIn(
                    self.unpublished_tag,
                    item.tags.all(),
                )

    def test_unpublished_items(self):
        response = Client().get(reverse("catalog:item_list"))
        categories = response.context["categories"].all()
        for category in categories:
            self.assertNotIn(self.unpub_item, category.item.all())

    def test_could_reach_published_item(self):
        response = Client().get(
            reverse("catalog:item_detail", args=[self.pub_item_right_cat.pk]),
        )
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_couldnt_reach_unpublished_item(self):
        response = Client().get(
            reverse("catalog:item_detail", args=[self.unpub_item.pk]),
        )
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)

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
                category=self.published_category,
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
            category=self.published_category,
            text="превосходно",
        )
        self.item.full_clean()
        self.item.save()
        self.item.tags.add(ModelsTests.published_tag)

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
