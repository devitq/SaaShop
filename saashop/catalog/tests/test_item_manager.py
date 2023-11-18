from django.test import TestCase

from catalog.models import Category, Item, Tag

__all__ = ()


class ItemManagerTests(TestCase):
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

    def test_published_method_fields_pos(self):
        items = Item.objects.published()
        item_necessary_values = ["id", "name", "text", "category_id"]
        tag_necessary_values = ["id", "name"]
        category_necessary_values = ["id", "name"]

        for item in items:
            for value in item_necessary_values:
                self.assertIn(value, item.__dict__)

            for tag in item.tags.all():
                for value in tag_necessary_values:
                    self.assertIn(value, tag.__dict__)

            category = item.category
            for value in category_necessary_values:
                self.assertIn(value, category.__dict__)

    def test_published_method_fields_neg(self):
        items = Item.objects.published()
        item_unnecessary_values = [
            "main_image_id",
            "is_published",
            "is_on_main",
            "created_at",
            "updated_at",
        ]
        tag_unnecessary_values = ["is_published", "unique_name", "slug"]
        category_unnecessary_values = [
            "is_published",
            "unique_name",
            "slug",
            "weight",
        ]

        for item in items:
            for value in item_unnecessary_values:
                self.assertNotIn(value, item.__dict__)

            for tag in item.tags.all():
                for value in tag_unnecessary_values:
                    self.assertNotIn(value, tag.__dict__)

            category = item.category
            for value in category_unnecessary_values:
                self.assertNotIn(value, category.__dict__)

    def test_on_main_method_fields_pos(self):
        items = Item.objects.on_main()
        item_necessary_values = ["id", "name", "text", "category_id"]
        tag_necessary_values = ["id", "name"]
        category_necessary_values = ["id", "name"]

        for item in items:
            for value in item_necessary_values:
                self.assertIn(value, item.__dict__)

            for tag in item.tags.all():
                for value in tag_necessary_values:
                    self.assertIn(value, tag.__dict__)

            category = item.category
            for value in category_necessary_values:
                self.assertIn(value, category.__dict__)

    def test_on_main_method_fields_neg(self):
        items = Item.objects.on_main()
        item_unnecessary_values = [
            "main_image_id",
            "is_published",
            "is_on_main",
            "created_at",
            "updated_at",
        ]
        tag_unnecessary_values = ["is_published", "unique_name", "slug"]
        category_unnecessary_values = [
            "is_published",
            "unique_name",
            "slug",
            "weight",
        ]

        for item in items:
            for value in item_unnecessary_values:
                self.assertNotIn(value, item.__dict__)

            for tag in item.tags.all():
                for value in tag_unnecessary_values:
                    self.assertNotIn(value, tag.__dict__)

            category = item.category
            for value in category_unnecessary_values:
                self.assertNotIn(value, category.__dict__)

    def test_item_detail_method_fields_pos(self):
        items = Item.objects.item_detail()
        item_necessary_values = [
            "id",
            "name",
            "text",
            "category_id",
            "main_image_id",
        ]
        tag_necessary_values = ["id", "name"]
        category_necessary_values = ["id", "name"]

        for item in items:
            for value in item_necessary_values:
                self.assertIn(value, item.__dict__)

            for tag in item.tags.all():
                for value in tag_necessary_values:
                    self.assertIn(value, tag.__dict__)

            category = item.category
            for value in category_necessary_values:
                self.assertIn(value, category.__dict__)

    def test_item_detail_method_fields_neg(self):
        items = Item.objects.item_detail()
        item_unnecessary_values = [
            "is_published",
            "is_on_main",
            "created_at",
            "updated_at",
        ]
        tag_unnecessary_values = ["is_published", "unique_name", "slug"]
        category_unnecessary_values = [
            "is_published",
            "unique_name",
            "slug",
            "weight",
        ]

        for item in items:
            for value in item_unnecessary_values:
                self.assertNotIn(value, item.__dict__)

            for tag in item.tags.all():
                for value in tag_unnecessary_values:
                    self.assertNotIn(value, tag.__dict__)

            category = item.category
            for value in category_unnecessary_values:
                self.assertNotIn(value, category.__dict__)
