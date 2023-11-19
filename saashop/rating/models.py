from django.db import models

from catalog.models import Item
from users.models import User

__all__ = ()


class Rating(models.Model):
    ONE_RATING = 1
    TWO_RATING = 2
    THREE_RATING = 3
    FOUR_RATING = 4
    FIVE_RATING = 5
    RATING_CHOICES = (
        (ONE_RATING, "Ненависть"),
        (TWO_RATING, "Неприязнь"),
        (THREE_RATING, "Нейтрально"),
        (FOUR_RATING, "Обожание"),
        (FIVE_RATING, "Любовь"),
    )
    rating = models.PositiveIntegerField(
        "оценка",
        choices=RATING_CHOICES,
    )
    text = models.TextField(
        "ваш отзыв о товаре",
        blank=True,
        null=True,
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
    )
    item = models.ForeignKey(
        Item,
        on_delete=models.CASCADE,
    )
