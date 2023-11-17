import sys

from django.contrib.auth.models import User, UserManager
from django.db import models

__all__ = ()


class ProfileManager(UserManager):
    def by_mail(self, email):
        return self.select_related("profile").get(email=email)

    def active(self):
        return self.select_related("profile").filter(is_active=True)

    def normalize_email(self, email):
        email = email.lower()
        login, domain = email.split("@")
        if "+" in login:
            login = login.split("+")[0]
        domain = domain.replace("ya.ru", "yandex.ru")
        if domain == "yandex.ru":
            login = login.replace(".", "-")
        elif domain == "gmail.com":
            login = login.replace(".", "")
        email = f"{login}@{domain}"

        return super().normalize_email(email)


class Profile(models.Model):
    def get_path_for_file(self, filename):
        return f"avatars/{self.user_id}/{filename}"

    user = models.OneToOneField(
        User,
        related_name="profile",
        on_delete=models.CASCADE,
    )
    birthday = models.DateField(
        "дата рождения",
        null=True,
        blank=True,
    )
    image = models.ImageField(
        "аватарка",
        null=True,
        blank=True,
        upload_to=get_path_for_file,
    )
    coffee_count = models.PositiveIntegerField(
        "количество выпитого кофе",
        default=0,
        blank=True,
    )
    attempts_count = models.PositiveIntegerField(
        "количество попыток входа",
        editable=False,
        default=0,
        blank=True,
    )
    blocked_timestamp = models.DateTimeField(
        verbose_name="время последней блокировки",
        null=True,
    )

    class Meta:
        verbose_name = "профиль"
        verbose_name_plural = "профили"


class User(User):
    class Meta:
        proxy = True

    objects = ProfileManager()


def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


models.signals.post_save.connect(create_profile, sender=User)

if "makemigrations" not in sys.argv and "migrate" not in sys.argv:
    User._meta.get_field("email")._unique = True
