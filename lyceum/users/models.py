from django.contrib.auth.models import User
from django.db import models

__all__ = ()


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


def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


models.signals.post_save.connect(create_profile, sender=User)
