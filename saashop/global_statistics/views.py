from django.contrib.auth.decorators import login_required
from django.shortcuts import render

import catalog.models
import users.models


def all_items(request):
    template = "global_statistics/all_items.html"
    items = catalog.models.Item.objects.all()
    context = {"items": items}
    return render(request, template, context)


@login_required
def user_items(request):
    template = "global_statistics/user_items.html"
    items = (
        catalog.models.Item.objects.filter(ratings__user=request.user)
        .order_by("-ratings__rating")
        .distinct()
    )
    context = {
        "items": items,
    }
    return render(request, template, context)


def all_users(request):
    template = "global_statistics/all_users.html"
    user_list = users.models.User.objects.all()
    context = {
        "users": user_list,
    }
    return render(request, template, context)


__all__ = ()
