from datetime import timedelta
import os

from django.test import TestCase
from django.utils import timezone
from freezegun import freeze_time

import users.models

__all__ = ()


class BirthdayContextProcessorTests(TestCase):
    def setUp(self):
        self.time_now = timezone.now()
        self.user = users.models.User.objects.create_user(
            username="testuser",
            password=os.getenv("DJANGO_SUPERUSER_PASSWORD", "1234"),
        )
        self.user_profile = self.user.profile
        self.user_profile.birthday = self.time_now
        self.user.profile.save()

    def test_birthday_context(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertTrue("users_with_birthday" in response.context)
        self.assertEqual(len(response.context["users_with_birthday"]), 1)

    def test_birthday_context_no_birthday(self):
        with freeze_time(self.time_now + timedelta(days=1, minutes=1)):
            response = self.client.get("/")
            self.assertEqual(response.status_code, 200)
            self.assertTrue("users_with_birthday" in response.context)
            self.assertEqual(len(response.context["users_with_birthday"]), 0)
