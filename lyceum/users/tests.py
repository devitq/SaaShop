from http import HTTPStatus
import os

from django.conf import settings
from django.contrib.auth.models import User
from django.core import mail
from django.test import Client, override_settings, TestCase
from django.urls import reverse
from django.utils import timezone
from freezegun import freeze_time
import parameterized

from users.models import CustomUser

__all__ = ()


class RegistrationActivationTests(TestCase):
    def setUp(self):
        self.signup_url = reverse("users:signup")
        self.activation_url = reverse(
            "users:activate_account",
            args=["token"],
        )
        self.time_now = timezone.now()

    @override_settings(DEFAULT_USER_IS_ACTIVE=False)
    def test_user_registration_and_activation(self):
        response = self.client.post(
            self.signup_url,
            {
                "username": "testuser",
                "password1": "testpassword",
                "password2": "testpassword",
                "email": "testuser@example.com",
            },
        )
        self.assertEqual(
            response.status_code,
            HTTPStatus.FOUND,
        )
        user = User.objects.get(username="testuser")
        user.refresh_from_db()
        self.assertFalse(user.is_active)
        link = mail.outbox[0].body

        with freeze_time(
            self.time_now + timezone.timedelta(hours=12, minutes=1),
        ):
            response = self.client.get(
                link,
                follow=True,
            )
            self.assertEqual(response.status_code, HTTPStatus.OK)
            user.refresh_from_db()
            self.assertFalse(user.is_active)

        with freeze_time(
            self.time_now + timezone.timedelta(hours=11, minutes=59),
        ):
            response = self.client.get(
                link,
                follow=True,
            )
            self.assertEqual(
                response.status_code,
                HTTPStatus.OK,
            )

            user.refresh_from_db()
            self.assertTrue(user.is_active)


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


class AuthenticationTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.username = "testuser"
        self.email = "testuser@example.com"
        self.password = os.getenv("DJANGO_SUPERUSER_PASSWORD", "1234")
        self.user = User.objects.create_user(
            username=self.username,
            email=self.email,
            password=self.password,
        )
        self.time_now = timezone.now()
        self.reactivation_url = reverse(
            "users:reactivate_account",
            args=["token"],
        )

    def test_login_by_username(self):
        response = self.client.post(
            reverse("login"),
            {"username": self.username, "password": self.password},
        )
        self.assertEqual(response.status_code, HTTPStatus.FOUND)

    def test_login_by_email(self):
        response = self.client.post(
            reverse("login"),
            {"username": self.email, "password": self.password},
        )
        self.assertEqual(response.status_code, HTTPStatus.FOUND)

    @override_settings(DEFAULT_USER_IS_ACTIVE=3)
    def test_account_deactivation_and_reactivation(self):
        for _ in range(settings.MAX_AUTH_ATTEMPTS):
            self.client.post(
                reverse("login"),
                {"username": self.username, "password": "wrong_pass"},
            )
        self.user.refresh_from_db()
        self.assertFalse(self.user.is_active)
        link = mail.outbox[0].body
        with freeze_time(
            self.time_now + timezone.timedelta(weeks=1, minutes=1),
        ):
            response = self.client.get(
                link,
                follow=True,
            )
            self.assertEqual(response.status_code, HTTPStatus.OK)
            self.user.refresh_from_db()
            self.assertFalse(self.user.is_active)

        with freeze_time(self.time_now + timezone.timedelta(days=6)):
            response = self.client.get(
                link,
                follow=True,
            )
            self.assertEqual(response.status_code, HTTPStatus.OK)
            self.user.refresh_from_db()
            self.assertTrue(self.user.is_active)


class EmailNormalizerTests(TestCase):
    def test_email_normalizer_for_yandex(self):
        normalized_email = CustomUser.objects.normalize_email(
            "itqHfsdFE..W.Fs.fdev+fsdf@ya.ru",
        )
        self.assertEqual(normalized_email, "itqhfsdfe--w-fs-fdev@yandex.ru")

    def test_email_normalizer_for_gmail(self):
        normalized_email = CustomUser.objects.normalize_email(
            "itqHfsdFE..W.Fs.fdev+fsdf@gmail.com",
        )
        self.assertEqual(normalized_email, "itqhfsdfewfsfdev@gmail.com")
