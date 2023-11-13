from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from users.models import Profile


__all__ = ()


class BaseFormMixin:
    def set_field_attributes(self, has_submitted):
        for field in self.visible_fields():
            field.field.widget.attrs["class"] = "form-control"
            if len(field.errors) != 0:
                field.field.widget.attrs["class"] = "form-control is-invalid"
                has_submitted = True
        for field in self.visible_fields():
            if len(field.errors) == 0 and has_submitted:
                field.field.widget.attrs["class"] = "form-control is-valid"


class UserForm(forms.ModelForm, BaseFormMixin):
    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)
        has_submitted = False
        self.set_field_attributes(has_submitted)

    class Meta:
        model = User
        fields = ["username", "email", "first_name"]


class UserChangeForm(forms.ModelForm, BaseFormMixin):
    def __init__(self, *args, **kwargs):
        super(UserChangeForm, self).__init__(*args, **kwargs)
        self.fields["coffee_count"].widget.attrs["disabled"] = True
        self.fields["coffee_count"].widget.attrs["required"] = False
        self.fields["birthday"].widget.attrs["required"] = False
        has_submitted = False
        self.set_field_attributes(has_submitted)

    class Meta:
        model = Profile
        fields = (
            Profile.birthday.field.name,
            Profile.image.field.name,
            Profile.coffee_count.field.name,
        )
        widgets = {
            Profile.birthday.field.name: forms.DateInput(
                attrs={"type": "date", "placeholder": "yyyy-mm-dd (DOB)"},
            ),
        }


class UserSignupForm(UserCreationForm, BaseFormMixin):
    def __init__(self, *args, **kwargs):
        super(UserSignupForm, self).__init__(*args, **kwargs)
        has_submitted = False
        self.set_field_attributes(has_submitted)

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ["username", "email", "password1", "password2"]
