from http import HTTPStatus

from django.http import HttpResponse
from django.shortcuts import render

__all__ = ()


def home(response):
    return render(
        request=response,
        template_name="homepage/main.html",
        context={},
    )


def coffee(response):
    return HttpResponse("Я чайник", status=HTTPStatus.IM_A_TEAPOT)
