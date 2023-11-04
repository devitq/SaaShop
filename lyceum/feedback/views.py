from django.shortcuts import render

__all__ = ()


def feedback(request):
    context = {}
    return render(
        request=request,
        template_name="feedback/feedback.html",
        context=context,
    )
