from django.shortcuts import render

__all__ = ()


def description(request):
    return render(
        request=request,
        template_name="about/about.html",
        context={},
    )
