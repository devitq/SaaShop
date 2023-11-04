from datetime import timedelta

from django.db import models
from django.shortcuts import get_object_or_404, render
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

import catalog.models

__all__ = ()


def item_list(request):
    items = catalog.models.Item.objects.published()
    context = {
        "items": items,
        "title": _("all_items"),
    }
    return render(
        request=request,
        template_name="catalog/item_list.html",
        context=context,
    )


def new_item_list(request):
    one_week_ago = timezone.now() - timedelta(days=7)
    ids = (
        catalog.models.Item.objects.published()
        .filter(created_at__gte=one_week_ago)
        .values_list("id", flat=True)
        .order_by("?")[:5]
    )
    if ids:
        items = (
            catalog.models.Item.objects.published()
            .filter(id__in=ids)
            .order_by("category", "name")
        )
    else:
        items = None
    context = {
        "items": items,
        "title": _("new_items"),
    }
    return render(
        request=request,
        template_name="catalog/item_list.html",
        context=context,
    )


def friday_item_list(request):
    ids = (
        catalog.models.Item.objects.published()
        .filter(updated_at__week_day=6)
        .values_list("id", flat=True)
        .order_by("-updated_at")[:5]
    )
    if ids:
        items = (
            catalog.models.Item.objects.published()
            .filter(id__in=ids)
            .order_by("category", "name")
        )
    else:
        items = None
    context = {
        "items": items,
        "title": _("friday"),
    }
    return render(
        request=request,
        template_name="catalog/item_list.html",
        context=context,
    )


def unverified_item_list(request):
    items = catalog.models.Item.objects.published().filter(
        created_at=models.F("updated_at"),
    )
    context = {
        "items": items,
        "title": _("unverified"),
    }
    return render(
        request=request,
        template_name="catalog/item_list.html",
        context=context,
    )


def item_detail(request, item_id):
    item = get_object_or_404(
        catalog.models.Item.objects.item_detail(),
        pk=item_id,
    )
    context = {
        "item": item,
    }
    return render(
        request=request,
        template_name="catalog/item.html",
        context=context,
    )


def re_item_detail(request, item_id):
    return render(
        request=request,
        template_name="catalog/item.html",
        context={},
    )


def convert_item_detail(request, item_id):
    return render(
        request=request,
        template_name="catalog/item.html",
        context={},
    )
