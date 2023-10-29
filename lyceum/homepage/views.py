from http import HTTPStatus

from django.http import HttpResponse
from django.shortcuts import render

import catalog.models

__all__ = ()


def home(response):
    items = catalog.models.Item.objects.on_main()
    context = {
        "items": items,
    }
    return render(
        request=response,
        template_name="homepage/main.html",
        context=context,
    )


def coffee(response):
    return HttpResponse("Я чайник", status=HTTPStatus.IM_A_TEAPOT)
