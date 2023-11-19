import os

from django.test import Client, TestCase
from django.urls import reverse

from catalog.models import Category, Item
from rating.models import Rating
from users.models import User


class TestFormCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.password = os.getenv("DJANGO_SUPERUSER_PASSWORD", "1234")
        cls.published_category = Category.objects.create(
            is_published=True,
            name="testform_cateory",
            slug="testform_cateory",
            weight=100,
        )

        cls.item = Item.objects.create(
            is_published=True,
            is_on_main=True,
            name="testform_item",
            text="превосходно",
            category=cls.published_category,
            main_image=None,
        )

        cls.user = User.objects.create(
            username="rating_testform_user",
            email="rating_testform_user@mail.ru",
            password=cls.password,
            is_active=True,
        )

    def test_avg_rating_in_context(self):
        response = Client().get(
            reverse("catalog:item_detail", args=[self.item.id]),
        )
        self.assertIn("avg_rating", response.context)

    def test_rating_creation(self):
        rating_count = Rating.objects.filter(item_id=self.item).count()
        self.client.force_login(user=self.user)
        self.client.post(
            path=reverse("catalog:item_detail", args=[self.item.id]),
            data={
                "rating": 2,
                "text": "Some text",
            },
            follow=True,
        )
        self.assertEqual(
            Rating.objects.filter(item_id=self.item).count(),
            rating_count + 1,
        )
        rating_count = Rating.objects.filter(item_id=self.item).count()

        self.client.post(
            path=reverse("catalog:item_detail", args=[self.item.id]),
            data={
                "rating": 4,
                "text": "Some text2",
            },
            follow=True,
        )
        self.assertEqual(
            Rating.objects.filter(item_id=self.item).count(),
            rating_count,
        )

    def test_rating_delete(self):
        self.client.force_login(user=self.user)
        self.client.post(
            path=reverse("catalog:item_detail", args=[self.item.id]),
            data={
                "rating": 4,
                "text": "Some text2",
            },
            follow=True,
        )
        rating_count = Rating.objects.filter(item_id=self.item).count()
        rating = Rating.objects.get_rating_by_item_and_user(
            self.user.id,
            self.item.id,
        ).first()
        self.client.get(
            path=reverse("rating:delete_rating", args=[rating.id]),
            follow=True,
        )
        self.assertEqual(
            Rating.objects.filter(item_id=self.item).count(),
            rating_count - 1,
        )


__all__ = ()
