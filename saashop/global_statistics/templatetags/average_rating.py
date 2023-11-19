from django import template
from django.db.models import Max, Min

import rating.models


register = template.Library()


@register.filter(name="average_rating")
def average_rating(value, item_id):
    average_item_rating = rating.models.Rating.objects.average_rating_by_item(
        item_id,
    )
    reactions = rating.models.Rating.objects.filter(item_id=item_id).aggregate(
        Max("rating"),
        Min("rating"),
    )
    highest_item_rating = (
        rating.models.Rating.objects.filter(
            item_id=item_id,
            rating=reactions["rating__max"],
        )
        .order_by("-created_at")
        .values("user_id")
        .first()
    )
    lowest_item_rating = (
        rating.models.Rating.objects.filter(
            item_id=item_id,
            rating=reactions["rating__min"],
        )
        .order_by("-created_at")
        .values("user_id")
        .first()
    )

    return (average_item_rating, highest_item_rating, lowest_item_rating)


__all__ = ()
