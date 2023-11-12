from django import forms
from django.contrib.auth.forms import (
    AuthenticationForm,
    PasswordChangeForm,
    PasswordResetForm,
    SetPasswordForm,
    UserCreationForm,
)
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


class UserProfileForm(forms.ModelForm, BaseFormMixin):
    def __init__(self, *args, **kwargs):
        super(UserProfileForm, self).__init__(*args, **kwargs)
        has_submitted = False
        self.set_field_attributes(has_submitted)

    class Meta:
        model = Profile
        fields = ["birthday", "image"]


class UserSignupForm(UserCreationForm, BaseFormMixin):
    def __init__(self, *args, **kwargs):
        super(UserSignupForm, self).__init__(*args, **kwargs)
        has_submitted = False
        self.set_field_attributes(has_submitted)

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]


class MyLoginForm(AuthenticationForm, BaseFormMixin):
    def __init__(self, *args, **kwargs):
        super(MyLoginForm, self).__init__(*args, **kwargs)
        has_submitted = False
        self.set_field_attributes(has_submitted)


class MyPasswordChangeForm(PasswordChangeForm, BaseFormMixin):
    def __init__(self, *args, **kwargs):
        super(MyPasswordChangeForm, self).__init__(*args, **kwargs)
        has_submitted = False
        self.set_field_attributes(has_submitted)


class MyPasswordResetForm(PasswordResetForm, BaseFormMixin):
    def __init__(self, *args, **kwargs):
        super(MyPasswordResetForm, self).__init__(*args, **kwargs)
        has_submitted = False
        self.set_field_attributes(has_submitted)


class MyPasswordConfirmForm(SetPasswordForm, BaseFormMixin):
    def __init__(self, *args, **kwargs):
        super(MyPasswordConfirmForm, self).__init__(*args, **kwargs)
        has_submitted = False
        self.set_field_attributes(has_submitted)
