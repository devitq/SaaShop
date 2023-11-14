import sys

from django.contrib.auth.models import User, UserManager
from django.db import models

__all__ = ()


class ProfileManager(UserManager):
    def by_mail(self, email):
        return self.select_related("profile").get(email=email)

    def active(self):
        return self.select_related("profile").filter(is_active=True)


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

    class Meta:
        verbose_name = "профиль"
        verbose_name_plural = "профили"


class CustomUser(User):
    class Meta:
        proxy = True

    objects = ProfileManager()

    def active(self):
        return self.is_active


def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


models.signals.post_save.connect(create_profile, sender=User)

if "makemigrations" not in sys.argv and "migrate" not in sys.argv:
    User._meta.get_field("email")._unique = True
