from datetime import timedelta
from http import HTTPStatus

from django.core.exceptions import ValidationError
from django.db.models import QuerySet
from django.test import Client, TestCase
from django.urls import reverse
from django.utils import timezone
from freezegun import freeze_time
import parameterized

from catalog.models import Category, Item, Tag

__all__ = ("ModelsTests",)


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

        with freeze_time(timezone.now() - timedelta(days=8)):
            cls.old_item = Item.objects.create(
                is_published=True,
                name="Старый товар",
                text="Превосходно стар",
                category=cls.published_category,
            )

        with freeze_time("2009-10-23"):
            cls.friday_item = Item.objects.create(
                is_published=True,
                name="Пятничный товар",
                text="Превосходно пятничнен",
                category=cls.published_category,
            )

        cls.changed_item = Item.objects.create(
            is_published=True,
            name="Изменённый товар",
            text="Превосходно изменён",
            category=cls.published_category,
        )
        with freeze_time(timezone.now() - timedelta(seconds=1)):
            cls.changed_item.name = "Изменили изменённый товар"
            cls.changed_item.save()

    def test_new_item_list(self):
        response = Client().get(reverse("catalog:new_item_list"))

        items = response.context["items"]
        self.assertNotIn(self.old_item, items)

    def test_friday_item_list(self):
        response = Client().get(reverse("catalog:new_item_list"))

        items = response.context["items"]
        self.assertNotIn(self.friday_item, items)

    def test_unverified_item_list(self):
        response = Client().get(reverse("catalog:unverified_item_list"))
        items = response.context["items"]
        self.assertNotIn(self.changed_item, items)

    def test_getting_prefetched(self):
        response = Client().get(reverse("catalog:item_list"))
        items = response.context["items"]
        for item in items:
            self.assertIn("tags", item.__dict__["_prefetched_objects_cache"])

    def test_getting_right_context(self):
        response = Client().get(reverse("catalog:item_list"))
        self.assertIn("items", response.context)
        self.assertIsInstance(response.context["items"], QuerySet)

    def test_item_count(self):
        response = Client().get(reverse("catalog:item_list"))
        self.assertEqual(len(response.context["items"]), 6)

    def test_item_categories(self):
        response = Client().get(reverse("catalog:item_list"))
        items = response.context["items"]
        for item in items:
            self.assertNotEqual(
                item.category,
                self.unpublished_category,
            )

    def test_item_tags(self):
        response = Client().get(reverse("catalog:item_list"))
        items = response.context["items"]
        for item in items:
            self.assertNotIn(
                self.unpublished_tag,
                item.tags.all(),
            )

    def test_unpublished_items(self):
        response = Client().get(reverse("catalog:item_list"))
        items = response.context["items"]
        self.assertNotIn(self.unpub_item, items)

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
