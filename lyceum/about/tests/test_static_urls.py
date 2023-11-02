from http import HTTPStatus

from django.test import Client, override_settings, TestCase
from django.urls import reverse

__all__ = ("StaticURLTests",)


class StaticURLTests(TestCase):
    @override_settings(ALLOW_REVERSE=False)
    def test_description_endpoint(self):
        response = Client().get(reverse("about:about"))
        self.assertEqual(
            response.status_code,
            HTTPStatus.OK,
        )
