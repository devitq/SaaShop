from django import forms
from django.utils.translation import gettext_lazy as _

from feedback.models import Feedback, FeedbackFile, PersonalData

__all__ = ("FeedbackForm",)


class MultipleFileInput(forms.ClearableFileInput):
    allow_multiple_selected = True


class MultipleFileField(forms.FileField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("widget", MultipleFileInput())
        super().__init__(*args, **kwargs)

    def clean(self, data, initial=None):
        single_file_clean = super().clean
        if isinstance(data, (list, tuple)):
            return [single_file_clean(d, initial) for d in data]
        return single_file_clean(data, initial)


class FilesForm(forms.ModelForm):
    file = MultipleFileField(required=False)

    def __init__(self, *args, **kwargs):
        super(FilesForm, self).__init__(*args, **kwargs)
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
        model = FeedbackFile
        fields = "__all__"
        exclude = [
            "feedback",
        ]


class PersonalDataForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(PersonalDataForm, self).__init__(*args, **kwargs)
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
        model = PersonalData
        fields = "__all__"
        exclude = [
            "feedback",
        ]
        labels = {
            PersonalData.mail.field.name: _("mail_label"),
            PersonalData.name.field.name: _("name_label"),
        }
        help_texts = {
            PersonalData.mail.field.name: _("mail_help_text"),
            PersonalData.name.field.name: _("name_help_text"),
        }


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
            Feedback.author.field.name,
        ]
        labels = {
            Feedback.text.field.name: _("text_label"),
        }
        help_texts = {
            Feedback.text.field.name: _("text_help_text"),
        }
        widgets = {
            Feedback.text.field.name: forms.Textarea(
                attrs={
                    "rows": "5",
                },
            ),
        }
