from betterforms.multiform import MultiModelForm
from django.conf import settings
from django.contrib import messages
from django.core.mail import send_mail
from django.shortcuts import redirect, render
from django.urls import reverse, reverse_lazy
from django.views import View

from feedback.forms import FeedbackForm, FilesForm, PersonalDataForm
from feedback.models import FeedbackFile

__all__ = ()


class FeedbackMultiForm(MultiModelForm):
    form_classes = {
        "personal_data_form": PersonalDataForm,
        "feedback_form": FeedbackForm,
        "files_form": FilesForm,
    }


class FeedbackView(View):
    template_name = "feedback/feedback.html"
    success_url = reverse_lazy("feedback:feedback")

    def get(self, request):
        form = FeedbackMultiForm()
        return render(
            request,
            template_name=self.template_name,
            context={"form": form},
        )

    def post(self, request):
        form = FeedbackMultiForm(request.POST, request.FILES)
        if form.is_valid():
            text = form["feedback_form"].cleaned_data.get("text")
            mail = form["personal_data_form"].cleaned_data.get("mail")
            personal_data = form["personal_data_form"].save()
            feedback = form["feedback_form"].save(commit=False)
            feedback.author = personal_data
            feedback.save()
            personal_data.feedback = feedback
            personal_data.save()
            files = request.FILES.getlist("files_form-file")
            for file in files:
                FeedbackFile.objects.create(feedback=feedback, file=file)
            send_mail(
                "New Feedback",
                text,
                settings.MAIL,
                [mail],
                fail_silently=False,
            )
            messages.success(request, "Form successfully submitted")
            return redirect(reverse("feedback:feedback"))

        return render(
            request,
            template_name=self.template_name,
            context={"form": form},
        )
