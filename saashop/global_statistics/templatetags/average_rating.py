from django import template
from django.db.models import Avg, Count, Max, Min

import rating.models

register = template.Library()


@register.filter(name="average_rating")
def average_rating(value, item_id):
    average = rating.models.Rating.objects.filter(item_id=item_id).aggregate(
        Count("rating"),
        Avg("rating"),
    )
    count = average["rating__count"]
    avg = str(average["rating__avg"])[:3]
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
        .values("user__username")
        .first()
    )
    lowest_item_rating = (
        rating.models.Rating.objects.filter(
            item_id=item_id,
            rating=reactions["rating__min"],
        )
        .order_by("-created_at")
        .values("user__username")
        .first()
    )

    return (count, avg, highest_item_rating, lowest_item_rating)


__all__ = ()
