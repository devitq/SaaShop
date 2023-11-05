from http import HTTPStatus

from django.http import HttpResponse
from django.shortcuts import render

import catalog.models
from homepage.forms import EchoForm

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


def echo(request):
    form = EchoForm(request.POST or None, auto_id=True)
    context = {
        "form": form,
    }
    return render(
        request=request,
        template_name="homepage/echo.html",
        context=context,
    )


def echo_submit(request):
    if request.method == "POST":
        form = EchoForm(request.POST or None)
        if form.is_valid():
            text = form.cleaned_data["text"]
            return HttpResponse(text)
    else:
        form = EchoForm()
    context = {"form": form}
    return render(
        request=request,
        template_name="homepage/echo.html",
        context=context,
    )
