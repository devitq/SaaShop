from django.test import TestCase

import users.models

__all__ = ()


class EmailNormalizerTests(TestCase):
    def test_email_normalizer_for_yandex(self):
        normalized_email = users.models.User.objects.normalize_email(
            "itqHfsdFE..W.Fs.fdev+fsdf@ya.ru",
        )
        self.assertEqual(normalized_email, "itqhfsdfe--w-fs-fdev@yandex.ru")

    def test_email_normalizer_for_gmail(self):
        normalized_email = users.models.User.objects.normalize_email(
            "itqHfsdFE..W.Fs.fdev+fsdf@gmail.com",
        )
        self.assertEqual(normalized_email, "itqhfsdfewfsfdev@gmail.com")
