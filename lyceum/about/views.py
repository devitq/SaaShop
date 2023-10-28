from django.shortcuts import render

__all__ = ()


def description(response):
    return render(
        request=response,
        template_name="about/about.html",
        context={},
    )
