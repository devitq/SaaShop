from django import template
from django.db.models import Avg, Count, Max, Min

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
        .values("name")
        .order_by("-ratings__created_at")
        .first()
    )
    lowest_rating = (
        catalog.models.Item.objects.filter(
            ratings__user_id=user_id,
            ratings__rating=reactions["rating__min"],
        )
        .values("name")
        .order_by("-ratings__created_at")
        .first()
    )

    average = rating.models.Rating.objects.filter(user_id=user_id).aggregate(
        Count("rating"),
        Avg("rating"),
    )

    return (
        highest_rating,
        lowest_rating,
        average["rating__count"],
        str(average["rating__avg"])[:3],
    )


__all__ = ()
