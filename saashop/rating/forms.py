from django import forms

from rating.models import Rating
from saashop.mixins import BaseFormMixin


class RatingCreationForm(forms.ModelForm, BaseFormMixin):
    def __init__(self, *args, **kwargs):
        super(RatingCreationForm, self).__init__(*args, **kwargs)
        self.set_field_attributes()

    class Meta:
        model = Rating
        fields = (
            model.rating.field.name,
            model.text.field.name,
        )

        exclude = (
            model.user.field.name,
            model.item.field.name,
            model.created_at.field.name,
        )

        widgets = {
            model.text.field.name: forms.Textarea(
                attrs={
                    "rows": "5",
                },
            ),
        }


__all__ = ()
