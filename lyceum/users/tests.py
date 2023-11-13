import os
import datetime
from http import HTTPStatus
from unittest.mock import patch

from django.contrib.auth.models import User
from django.test import Client, override_settings, TestCase
from django.urls import reverse
from django.utils import timezone
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
import parameterized

from users.tokens import account_activation_token

__all__ = ()


class RegistrationActivationTests(TestCase):
    def setUp(self):
        self.signup_url = reverse("users:signup")
        self.activation_url = reverse(
            "users:activate_account",
            args=["uidb64", "token"],
        )
        self.mocked_now = timezone.now()

    @override_settings(DEFAULT_USER_IS_ACTIVE=False)
    @patch("django.utils.timezone.now")
    def test_user_registration_and_activation(self, mock_now):
        mock_now.return_value = self.mocked_now
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

        mock_now.return_value = self.mocked_now + datetime.timedelta(
            hours=12,
            minutes=1,
        )
        uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
        token = account_activation_token.make_token(user)

        response = self.client.get(
            self.activation_url.replace("uidb64", uidb64).replace(
                "token",
                token,
            ),
            follow=True,
        )
        self.assertEqual(response.status_code, HTTPStatus.OK)
        user.refresh_from_db()
        self.assertFalse(user.is_active)

        mock_now.return_value = self.mocked_now + datetime.timedelta(
            hours=11,
            minutes=59,
        )
        response = self.client.get(
            self.activation_url.replace("uidb64", uidb64).replace(
                "token",
                token,
            ),
        )
        self.assertEqual(
            response.status_code,
            HTTPStatus.FOUND,
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
