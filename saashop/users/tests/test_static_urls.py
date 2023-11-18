from http import HTTPStatus

from django.test import Client, TestCase
from django.urls import reverse
import parameterized

__all__ = ()


class StaticURLTests(TestCase):
    @parameterized.parameterized.expand(
        [
            ("users:login",),
            ("users:signup",),
            ("users:password_reset"),
            ("users:user_list"),
        ],
    )
    def test_login_url(self, url):
        response = Client().get(reverse(url))
        self.assertEqual(response.status_code, HTTPStatus.OK)
