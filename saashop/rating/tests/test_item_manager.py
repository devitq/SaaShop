import os

from django.test import TestCase

from catalog.models import Category, Item
from rating.models import Rating
from users.models import User


class ItemManagerTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.password = os.getenv("DJANGO_SUPERUSER_PASSWORD", "1234")
        cls.published_category = Category.objects.create(
            is_published=True,
            name="rating_testmanager_cateory",
            slug="rating_testmanager_cateory",
            weight=100,
        )

        cls.item = Item.objects.create(
            is_published=True,
            is_on_main=True,
            name="rating_testmanager_item",
            text="превосходно",
            category=cls.published_category,
            main_image=None,
        )

        cls.user1 = User.objects.create(
            username="rating_testmanager_user1",
            email="rating_testmanager_user1@mail.ru",
            password=cls.password,
        )
        cls.user2 = User.objects.create(
            username="rating_testmanager_user2",
            email="rating_testmanager_user2@mail.ru",
            password=cls.password,
        )

        cls.rating1 = Rating.objects.create(
            rating=2,
            text="Some text",
            user=cls.user1,
            item=cls.item,
        )
        cls.rating2 = Rating.objects.create(
            rating=5,
            text="Some text",
            user=cls.user2,
            item=cls.item,
        )

    def test_average_rating_method(self):
        avg = Rating.objects.average_rating(self.item.id)
        self.assertEqual({"count": 2, "avg": 3.5}, avg)

    def test_get_item_with_rating_method(self):
        item = Rating.objects.get_item_with_rating(self.item.id).first()
        self.assertEqual(item.ratings.count(), 2)

    def test_get_rating_by_item_and_user_method(self):
        rating = Rating.objects.get_rating_by_item_and_user(
            self.user1.id,
            self.item.id,
        )
        self.assertEqual(rating.count(), 1)
        rating = rating.first()
        self.assertEqual(rating.user.id, self.user1.id)
        self.assertEqual(rating.item.id, self.item.id)


__all__ = ()
