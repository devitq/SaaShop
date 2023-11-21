from http import HTTPStatus

from django.test import Client, TestCase
from django.urls import reverse
import parameterized

__all__ = ()


class DynamicURLTests(TestCase):
    @parameterized.parameterized.expand(
        [
            ("global_statistics:all_items",),
            ("global_statistics:user_items",),
            ("global_statistics:all_users",),
        ],
    )
    def test_statistics_endpoint(self, url):
        response = Client().get(
            reverse(url),
            follow=True,
        )
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_user_items_redirect(self):
        response = Client().get(
            reverse("global_statistics:user_items"),
        )
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
