from django.conf import settings
from django.contrib import messages
from django.core.mail import send_mail
from django.shortcuts import redirect, render
from django.urls import reverse

from feedback.forms import FeedbackForm, FilesForm, PersonalDataForm
from feedback.models import FeedbackFile

__all__ = ()


def feedback(request):
    feedback_form = FeedbackForm(request.POST or None, auto_id=True)
    personal_data_form = PersonalDataForm(request.POST or None, auto_id=True)
    files_form = FilesForm(
        request.POST or None,
        request.FILES or None,
        auto_id=True,
    )
    context = {
        "forms": [
            personal_data_form,
            feedback_form,
            files_form,
        ],
    }
    if request.method == "POST":
        if feedback_form.is_valid() and personal_data_form.is_valid():
            text = feedback_form.cleaned_data.get("text")
            mail = personal_data_form.cleaned_data.get("mail")
            personal_data = personal_data_form.save()
            feedback = feedback_form.save(commit=False)
            feedback.author = personal_data
            feedback.save()
            personal_data.feedback = feedback
            personal_data.save()
            files = request.FILES.getlist("file")
            for file in files:
                FeedbackFile.objects.create(feedback=feedback, file=file)
            send_mail(
                "Новый фидбек",
                text,
                settings.MAIL,
                [mail],
                fail_silently=False,
            )
            files = files_form.cleaned_data["file"]
            messages.success(request, "Форма успешно отправлена")
            return redirect(reverse("feedback:feedback"))

    return render(
        request=request,
        template_name="feedback/feedback.html",
        context=context,
    )
