from django import forms

__all__ = ("EchoForm",)


class EchoForm(forms.Form):
    text = forms.CharField(
        label="Текст",
        help_text="Введите какой-нибудь текст",
        widget=forms.Textarea(attrs={"rows": 5}),
    )

    def __init__(self, *args, **kwargs):
        super(EchoForm, self).__init__(*args, **kwargs)
        for field in self.visible_fields():
            field.field.widget.attrs["class"] = "form-control"
            if field.errors:
                field.field.widget.attrs["class"] = "form-control is-invalid"
