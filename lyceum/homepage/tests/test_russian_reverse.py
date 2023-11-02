from django.test import Client, override_settings, TestCase
from django.urls import reverse

from lyceum import settings

__all__ = ("RussianReverseTests",)


class RussianReverseTests(TestCase):
    @override_settings(ALLOW_REVERSE=True)
    def test_reverse_russian_words_enabled(self):
        contents = {
            Client().get(reverse("homepage:coffee")).content for _ in range(10)
        }
        self.assertIn("Я чайник".encode(), contents)
        self.assertIn("Я кинйач".encode(), contents)

    def test_reverse_russian_words_enabled_default(self):
        if settings.ALLOW_REVERSE:
            contents = {
                Client().get(reverse("homepage:coffee")).content
                for _ in range(10)
            }
            self.assertIn("Я чайник".encode(), contents)
            self.assertIn("Я кинйач".encode(), contents)

    @override_settings(ALLOW_REVERSE=False)
    def test_reverse_russian_words_disabled(self):
        contents = {
            Client().get(reverse("homepage:coffee")).content for _ in range(10)
        }
        self.assertIn("Я чайник".encode(), contents)
        self.assertNotIn("Я кинйач".encode(), contents)
