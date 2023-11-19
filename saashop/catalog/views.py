from datetime import timedelta

from django.contrib import messages
from django.db import models
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.views.generic import DetailView, ListView

import catalog.models
from rating.forms import RatingForm
from rating.models import Rating

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

    def get(self, request, pk):
        item_id = self.kwargs.get("pk")

        item = get_object_or_404(
            Rating.objects.get_item_with_rating(pk),
            pk=item_id,
        )

        user_rating = None
        if request.user.is_authenticated:
            user_rating = Rating.objects.get_rating_by_item_and_user(
                request.user.id,
                pk,
            ).first()

        avg_rating = Rating.objects.average_rating(pk)
        form = RatingForm(instance=user_rating)

        context = {
            "item": item,
            "avg_rating": avg_rating,
            "form": form,
        }
        return render(
            request,
            template_name=self.template_name,
            context=context,
        )

    def post(self, request, pk):
        item_id = self.kwargs.get("pk")
        item = get_object_or_404(
            Rating.objects.get_item_with_rating(pk),
            pk=item_id,
        )
        if not request.user.is_authenticated:
            messages.error(
                request,
                "Пользователь не авторизован",
            )
            redirect("catalog:item_detail", pk=pk)
        form = RatingForm(request.POST)
        user_rating = None
        if request.user.is_authenticated:
            user_rating = Rating.objects.get_rating_by_item_and_user(
                request.user.id,
                pk,
            ).first()
        if form.is_valid():
            if user_rating:
                user_rating.text = form.cleaned_data["text"]
                user_rating.rating = form.cleaned_data["rating"]
                user_rating.save()
                return redirect("catalog:item_detail", pk=pk)
            rating = form.save(commit=False)
            rating.user = request.user
            rating.item = item
            rating.save()
        return redirect("catalog:item_detail", pk=pk)
