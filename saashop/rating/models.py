from django.db import models
from django.utils.translation import gettext_lazy as _

from catalog.models import Item
from users.models import User


__all__ = ()


class RatingManager(models.Manager):
    def average_rating(self, item_id):
        queryset = self.get_queryset().filter(item_id=item_id)
        return get_rating_stats(queryset.all())

    def get_rating_with_user(self):
        return (
            self.get_queryset()
            .select_related(Rating.user.field.name)
            .select_related(
                f"{Rating.user.field.name}__profile",
            )
        )

    def get_item_with_rating(self, item_id):
        return (
            Item.objects.item_detail(item_id)
            .select_related(Item.main_image.field.name)
            .prefetch_related(
                models.Prefetch(
                    "ratings",
                    queryset=self.get_rating_with_user(),
                ),
            )
        )

    def get_rating_by_item_and_user(self, user_id, item_id):
        return self.get_queryset().filter(user_id=user_id, item_id=item_id)


def get_rating_stats(ratings):
    count_of_rating = len(ratings)
    if not count_of_rating:
        return {
            "count": 0,
            "avg": None,
        }
    average_rating = round(
        sum(r.rating for r in ratings) / count_of_rating,
        1,
    )
    return {
        "count": count_of_rating,
        "avg": average_rating,
    }


class Rating(models.Model):
    objects = RatingManager()

    RATING_CHOICES = (
        (1, "Ненависть"),
        (2, "Неприязнь"),
        (3, "Нейтрально"),
        (4, "Обожание"),
        (5, "Любовь"),
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
        related_name="ratings",
        related_query_name="ratings",
    )
    item = models.ForeignKey(
        Item,
        on_delete=models.CASCADE,
        related_name="ratings",
        related_query_name="ratings",
    )
    created_at = models.DateTimeField(
        _("created_at_utc_models"),
        null=True,
        auto_now_add=True,
    )

    class Meta:
        verbose_name = "Отзыв"
        verbose_name_plural = "Отзывы"
        unique_together = ("user", "item")
