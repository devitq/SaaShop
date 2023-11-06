from django import forms
from django.utils.translation import gettext_lazy as _

from feedback.models import Feedback

__all__ = ("FeedbackForm",)


class FeedbackForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(FeedbackForm, self).__init__(*args, **kwargs)
        has_submitted = False
        for field in self.visible_fields():
            field.field.widget.attrs["class"] = "form-control"
            if len(field.errors) != 0:
                field.field.widget.attrs["class"] = "form-control is-invalid"
                has_submitted = True
        for field in self.visible_fields():
            if len(field.errors) != 1 and has_submitted:
                field.field.widget.attrs["class"] = "form-control is-valid"

    class Meta:
        model = Feedback
        fields = "__all__"
        exclude = [
            Feedback.created_on.field.name,
            Feedback.status.field.name,
        ]
        labels = {
            Feedback.mail.field.name: _("mail_label"),
            Feedback.text.field.name: _("text_label"),
            Feedback.name.field.name: _("name_label"),
        }
        help_texts = {
            Feedback.mail.field.name: _("mail_help_text"),
            Feedback.text.field.name: _("text_help_text"),
            Feedback.name.field.name: _("name_help_text"),
        }
        widgets = {
            Feedback.text.field.name: forms.Textarea(
                attrs={
                    "rows": "5",
                },
            ),
        }
