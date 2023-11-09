from http import HTTPStatus

from django.http import HttpResponse
from django.shortcuts import render
from django.utils.translation import gettext_lazy as _

import catalog.models
from homepage.forms import EchoForm

__all__ = ()


def home(request):
    items = catalog.models.Item.objects.on_main()
    features = [
        {"title": _("feature_1_title"), "content": _("feature_1_content")},
        {"title": _("feature_2_title"), "content": _("feature_2_content")},
        {"title": _("feature_3_title"), "content": _("feature_3_content")},
        {"title": _("feature_4_title"), "content": _("feature_4_content")},
        {"title": _("feature_5_title"), "content": _("feature_5_content")},
        {"title": _("feature_6_title"), "content": _("feature_6_content")},
    ]
    context = {
        "items": items,
        "features": features,
    }
    return render(
        request=request,
        template_name="homepage/main.html",
        context=context,
    )


def coffee(request):
    return HttpResponse("Я чайник", status=HTTPStatus.IM_A_TEAPOT)


def echo(request):
    if request.method == "GET":
        form = EchoForm(request.POST or None, auto_id=True)
        context = {
            "form": form,
        }
    else:
        return HttpResponse(status=HTTPStatus.METHOD_NOT_ALLOWED)
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
        form = EchoForm()
    else:
        return HttpResponse(status=HTTPStatus.METHOD_NOT_ALLOWED)
    context = {"form": form}
    return render(
        request=request,
        template_name="homepage/echo.html",
        context=context,
    )
