from django import template
from django.db.models import Max, Min

import catalog.models
import rating.models


register = template.Library()


@register.filter(name="user_ratings")
def user_ratings(value, user_id):
    reactions = rating.models.Rating.objects.filter(user_id=user_id).aggregate(
        Max("rating"),
        Min("rating"),
    )
    highest_rating = (
        catalog.models.Item.objects.filter(
            ratings__user_id=user_id,
            ratings__rating=reactions["rating__max"],
        )
        .order_by("-ratings__created_at")
        .first()
    )
    lowest_rating = (
        catalog.models.Item.objects.filter(
            ratings__user_id=user_id,
            ratings__rating=reactions["rating__min"],
        )
        .order_by("-ratings__created_at")
        .first()
    )
    average_dirty = rating.models.Rating.objects.average_rating_by_user(
        user_id=user_id,
    )
    number_od_ratings = average_dirty["count"]
    average = average_dirty["avg"]
    return (highest_rating, lowest_rating, number_od_ratings, average)


__all__ = ()
