from http import HTTPStatus

from django.http import HttpResponse
from django.shortcuts import render

import catalog.models

__all__ = ()


def home(request):
    items = catalog.models.Item.objects.on_main()
    context = {
        "items": items,
    }
    return render(
        request=request,
        template_name="homepage/main.html",
        context=context,
    )


def coffee(request):
    return HttpResponse("Я чайник", status=HTTPStatus.IM_A_TEAPOT)
