import sys

import django.contrib.auth.models
from django.db import models

__all__ = ()


class UserManager(django.contrib.auth.models.UserManager):
    def get_queryset(self):
        # Всегда грузим профиль
        return super().get_queryset().select_related("profile")

    def by_mail(self, email):
        return self.get_queryset().get(email=email)

    def active(self):
        return self.get_queryset().filter(is_active=True)

    def normalize_email(self, email):
        if email:
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
        django.contrib.auth.models.User,
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


class User(django.contrib.auth.models.User):
    class Meta:
        proxy = True

    objects = UserManager()


def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


def normalize_user_email(sender, instance, **kwargs):
    instance.email = User.objects.normalize_email(instance.email)


models.signals.post_save.connect(create_profile, sender=User)
models.signals.post_save.connect(
    create_profile,
    sender=django.contrib.auth.models.User,
)
models.signals.pre_save.connect(normalize_user_email, sender=User)
models.signals.pre_save.connect(
    normalize_user_email,
    sender=django.contrib.auth.models.User,
)

if "makemigrations" not in sys.argv and "migrate" not in sys.argv:
    User._meta.get_field("email")._unique = True
    User._meta.get_field("email").blank = False
    User._meta.get_field("email").null = False
