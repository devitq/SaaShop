from django import forms

from rating.models import Rating
from saashop.mixins import BaseFormMixin

__all__ = ()


class RatingForm(forms.ModelForm, BaseFormMixin):
    def __init__(self, *args, **kwargs):
        super(RatingForm, self).__init__(*args, **kwargs)
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


class RatingAdminForm(forms.ModelForm):
    class Meta:
        model = Rating
        fields = "__all__"

    def clean(self):
        cleaned_data = super().clean()
        user = cleaned_data.get("user")
        item = cleaned_data.get("item")

        existing_rating = Rating.objects.filter(user=user, item=item).first()

        if existing_rating:
            raise forms.ValidationError(
                "Пользователь уже оставлял свой отзыв на этот товар",
            )
