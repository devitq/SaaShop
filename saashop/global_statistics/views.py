from django.contrib.auth.decorators import login_required
from django.db.models import Avg, Count, F, Max, Min, OuterRef, Subquery
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views import View
from django.views.generic import ListView

import catalog.models
import rating.models
import users.models


__all__ = ()


class AllItemsView(View):
    template_name = "global_statistics/items.html"

    def get(self, request):
        items = catalog.models.Item.objects.annotate(
            count_ratings=Count("ratings"),
            avg_rating=Avg("ratings__rating"),
            highest_rating_user=Subquery(
                rating.models.Rating.objects.filter(
                    item_id=OuterRef("id"),
                    user=OuterRef("ratings__user"),
                )
                .order_by("-rating")[:1]
                .values("user__username"),
            ),
            lowest_rating_user=Subquery(
                rating.models.Rating.objects.filter(
                    item_id=OuterRef("id"),
                    user=OuterRef("ratings__user"),
                )
                .order_by("rating")[:1]
                .values("user__username"),
            ),
        ).values(
            "id",
            "name",
            "highest_rating_user",
            "lowest_rating_user",
            "count_ratings",
            "avg_rating",
        )

        context = {"items": items}
        return render(request, self.template_name, context)


@method_decorator(login_required, name="dispatch")
class UserItemsView(ListView):
    model = catalog.models.Item
    template_name = "global_statistics/user_items.html"
    context_object_name = "items"

    def get_queryset(self):
        user_ratings = rating.models.Rating.objects.filter(
            user=self.request.user,
        )
        return (
            catalog.models.Item.objects.filter(ratings__in=user_ratings)
            .order_by("-ratings__rating")
            .only("id", "name")
            .distinct()
        )


class AllUsersView(View):
    template_name = "global_statistics/users.html"

    def get(self, request):
        user_list = users.models.User.objects.annotate(
            highest_rating_item_name=Max(
                "ratings__item__name",
                filter=F("ratings__rating"),
            ),
            lowest_rating_item_name=Min(
                "ratings__item__name",
                filter=F("ratings__rating"),
            ),
            total_ratings=Count("ratings"),
            avg_rating=Avg("ratings__rating"),
        ).values(
            "id",
            "username",
            "highest_rating_item_name",
            "lowest_rating_item_name",
            "total_ratings",
            "avg_rating",
        )

        context = {
            "users": user_list,
        }
        return render(request, self.template_name, context)
