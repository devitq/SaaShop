from django.db import models
from django.shortcuts import get_object_or_404, render

import catalog.models

__all__ = ()


def item_list(response):
    items = catalog.models.Item.objects.published().values("category")
    categories = (
        catalog.models.Category.objects.only("name")
        .annotate(
            has_items=models.Exists(
                catalog.models.Item.objects.only("id").filter(
                    category=models.OuterRef("pk"),
                ),
            ),
        )
        .prefetch_related(
            models.Prefetch(
                "item",
                queryset=catalog.models.Item.objects.published(),
            ),
        )
        .filter(models.Exists(items.filter(category=models.OuterRef("pk"))))
        .all()
    )
    context = {
        "categories": categories,
    }
    return render(
        request=response,
        template_name="catalog/item_list.html",
        context=context,
    )


def item_detail(response, item_id):
    item = get_object_or_404(
        catalog.models.Item.objects.item_detail(),
        pk=item_id,
    )
    context = {
        "item": item,
    }
    return render(
        request=response,
        template_name="catalog/item.html",
        context=context,
    )


def re_item_detail(response, item_id):
    return render(
        request=response,
        template_name="catalog/item.html",
        context={},
    )


def convert_item_detail(response, item_id):
    return render(
        request=response,
        template_name="catalog/item.html",
        context={},
    )
