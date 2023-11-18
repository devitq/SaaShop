from http import HTTPStatus

from django.test import Client, override_settings, TestCase
from django.urls import reverse

__all__ = ()


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
