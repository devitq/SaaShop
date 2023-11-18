from datetime import timedelta

from django.db import models
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.views.generic import DetailView, ListView

import catalog.models

__all__ = ()


class ItemListView(ListView):
    template_name = "catalog/item_list.html"
    context_object_name = "items"

    def get_queryset(self):
        return catalog.models.Item.objects.published()


class NewItemListView(ItemListView):
    template_name = "catalog/item_list.html"

    def get_queryset(self):
        one_week_ago = timezone.now() - timedelta(days=7)
        ids = (
            catalog.models.Item.objects.published()
            .filter(created_at__gte=one_week_ago)
            .values_list("id", flat=True)
            .order_by("?")[:5]
        )
        return (
            (
                catalog.models.Item.objects.published()
                .filter(id__in=ids)
                .order_by("category", "name")
            )
            if ids
            else None
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = _("new_items")
        return context


class FridayItemListView(ItemListView):
    template_name = "catalog/item_list.html"

    def get_queryset(self):
        ids = (
            catalog.models.Item.objects.published()
            .filter(updated_at__week_day=6)
            .values_list("id", flat=True)
            .order_by("-updated_at")[:5]
        )
        return (
            (
                catalog.models.Item.objects.published()
                .filter(id__in=ids)
                .order_by("category", "name")
            )
            if ids
            else None
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = _("friday")
        return context


class UnverifiedItemListView(ItemListView):
    template_name = "catalog/item_list.html"

    def get_queryset(self):
        return catalog.models.Item.objects.published().filter(
            created_at=models.F("updated_at"),
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = _("unverified")
        return context


class ItemDetailView(DetailView):
    template_name = "catalog/item.html"
    context_object_name = "item"

    def get_object(self, queryset=None):
        item_id = self.kwargs.get("pk")
        return get_object_or_404(
            catalog.models.Item.objects.published(),
            pk=item_id,
        )
