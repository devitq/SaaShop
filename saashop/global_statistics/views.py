from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views import View
from django.views.generic import ListView

import catalog.models
import users.models


class AllItemsView(View):
    template_name = "global_statistics/all_items.html"

    def get(self, request):
        items = catalog.models.Item.objects.all()
        context = {"items": items}
        return render(request, self.template_name, context)


@method_decorator(login_required, name="dispatch")
class UserItemsView(ListView):
    model = catalog.models.Item
    template_name = "global_statistics/user_items.html"
    context_object_name = "items"

    def get_queryset(self):
        return (
            super()
            .get_queryset()
            .filter(ratings__user=self.request.user)
            .order_by("-ratings__rating")
            .distinct()
        )


class AllUsersView(View):
    template_name = "global_statistics/all_users.html"

    def get(self, request):
        user_list = users.models.User.objects.all().values("id", "username")
        context = {
            "users": user_list,
        }
        return render(request, self.template_name, context)


__all__ = ()
