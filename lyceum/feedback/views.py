from django.conf import settings
from django.contrib import messages
from django.core.mail import send_mail
from django.shortcuts import redirect, render
from django.urls import reverse

from feedback.forms import FeedbackForm
from feedback.models import Feedback

__all__ = ()


def feedback(request):
    form = FeedbackForm(request.POST or None, auto_id=True)
    context = {
        "form": form,
    }
    if request.method == "POST":
        if form.is_valid():
            text = form.cleaned_data.get("text")
            mail = form.cleaned_data.get("mail")
            Feedback.objects.create(
                text=text,
                mail=mail,
            )
            send_mail(
                "Новый фидбек",
                text,
                settings.MAIL,
                [mail],
                fail_silently=False,
            )
            messages.success(request, "Форма успешно отправлена")
            return redirect(reverse("feedback:feedback"))
    return render(
        request=request,
        template_name="feedback/feedback.html",
        context=context,
    )
