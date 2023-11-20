from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect
from django.utils.decorators import method_decorator
from django.views import View

from rating.forms import RatingForm
from rating.models import Rating

__all__ = ()


@method_decorator(login_required, name="dispatch")
class RatingDeleteView(View):
    def get(self, request, pk):
        rating = get_object_or_404(
            Rating.objects,
            pk=pk,
        )
        item_id = rating.item.id
        if request.user.is_superuser or request.user.id == rating.user.id:
            rating.delete()
            messages.success(
                request,
                "Отзыв удалён",
            )
            return redirect("catalog:item_detail", pk=item_id)
        raise Http404()


@method_decorator(login_required, name="dispatch")
class RatingUpdateView(View):
    def post(self, request, pk):
        rating = get_object_or_404(
            Rating.objects.all(),
            pk=pk,
        )
        if not request.user.is_superuser and request.user.id != rating.user.id:
            raise Http404()
        form = RatingForm(request.POST, instance=rating)
        if form.is_valid():
            if rating:
                rating.text = form.cleaned_data["text"]
                rating.rating = form.cleaned_data["rating"]
                rating.save()
                messages.success(
                    request,
                    "Изменения сохранены",
                )
                return redirect("catalog:item_detail", pk=rating.item.id)
        return Http404()
