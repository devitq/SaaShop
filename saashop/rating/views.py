from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect
from django.views import View

from rating.models import Rating


class RatingDelete(View):
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
        messages.error(
            request,
            "У вас нет прав на удаление отзыва",
        )
        return redirect("catalog:item_detail", pk=item_id)


__all__ = ()
