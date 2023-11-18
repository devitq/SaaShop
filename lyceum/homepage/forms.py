from django import forms

from lyceum.mixins import BaseFormMixin

__all__ = ("EchoForm",)


class EchoForm(forms.Form, BaseFormMixin):
    text = forms.CharField(
        label="Текст",
        help_text="Введите какой-нибудь текст",
        widget=forms.Textarea(attrs={"rows": 5}),
        required=True,
    )

    def __init__(self, *args, **kwargs):
        super(EchoForm, self).__init__(*args, **kwargs)
        self.set_field_attributes()
