from http import HTTPStatus

from django.http import HttpResponse
from django.shortcuts import render
from django.utils.translation import gettext_lazy as _
from django.views import View

import catalog.models
from homepage.forms import EchoForm

__all__ = ()


class HomeView(View):
    template_name = "homepage/main.html"

    def get(self, request):
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
            request,
            template_name=self.template_name,
            context=context,
        )


class CoffeeView(View):
    def get(self, request):
        if request.user.is_authenticated:
            profile = request.user.profile
            profile.coffee_count += 1
            profile.save()
        return HttpResponse("Я чайник", status=HTTPStatus.IM_A_TEAPOT)


class EchoView(View):
    template_name = "homepage/echo.html"
    form_class = EchoForm

    def get(self, request):
        context = {
            "form": self.form_class,
        }
        return render(
            request,
            template_name=self.template_name,
            context=context,
        )


class EchoSubmitView(View):
    template_name = "homepage/echo.html"

    def post(self, request):
        form = EchoForm(request.POST or None)
        if form.is_valid():
            text = form.cleaned_data["text"]
            return HttpResponse(text)
        form = EchoForm()
        context = {"form": form}
        return render(
            request,
            template_name=self.template_name,
            context=context,
        )

    def get(self, request):
        return HttpResponse(status=HTTPStatus.METHOD_NOT_ALLOWED)
