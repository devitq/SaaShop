from django import template

import rating.models


register = template.Library()


@register.filter(name="item_ratings")
def item_ratings(value, item_id):
    return rating.models.Rating.objects.filter(item_id=item_id).exists()


__all__ = ()
