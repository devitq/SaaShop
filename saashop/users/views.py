from betterforms.multiform import MultiModelForm
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.core.signing import BadSignature, SignatureExpired, TimestampSigner
from django.shortcuts import redirect, render
from django.urls import reverse, reverse_lazy
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.views.generic import (
    CreateView,
    DetailView,
    ListView,
    View,
)

from users.forms import (
    UserChangeForm,
    UserProfileChangeForm,
    UserSignupForm,
)
import users.models


__all__ = ()


class ActivateAccountView(View):
    def get(self, request, token):
        signer = TimestampSigner()
        try:
            username = signer.unsign(
                token,
                max_age=timezone.timedelta(hours=12),
            )
            user = users.models.User.objects.get(username=username)
            user.is_active = True
            user.save()
            messages.success(
                request,
                "Аккаунт успешно активирован",
            )
        except SignatureExpired:
            messages.error(
                request,
                "Срок действия ссылки истёк :(",
            )
        except BadSignature:
            messages.error(
                request,
                "Сломанная ссылка!",
            )

        return redirect("users:login")


class ReactivateAccountView(View):
    def get(self, request, token):
        signer = TimestampSigner()
        try:
            username = signer.unsign(
                token,
                max_age=timezone.timedelta(days=7),
            )
            user = users.models.User.objects.get(username=username)
            user.is_active = True
            user.save()
            messages.success(
                request,
                "Аккаунт успешно активирован",
            )
        except SignatureExpired:
            messages.error(
                request,
                "Срок действия ссылки истёк :(",
            )
        except BadSignature:
            messages.error(
                request,
                "Сломанная ссылка!",
            )

        return redirect("users:login")


class UserSignupView(CreateView):
    template_name = "users/signup.html"
    form_class = UserSignupForm
    success_url = reverse_lazy("users:login")

    def form_valid(self, form):
        if not self.request.user.is_authenticated:
            user = form.save(commit=False)
            user.is_active = settings.DEFAULT_USER_IS_ACTIVE
            user.save()
            self.object = user
            signer = TimestampSigner()
            token = signer.sign(user.username)
            url = self.request.build_absolute_uri(
                reverse(
                    "users:activate_account",
                    kwargs={"token": token},
                ),
            )
            send_mail(
                "Activate Your Account",
                url,
                settings.MAIL,
                [form.cleaned_data.get("email")],
                fail_silently=False,
            )

            messages.success(
                self.request,
                "Please check your email to activate your account.",
            )

            return super().form_valid(form)
        return super().form_invalid(form)


class UserListView(ListView):
    template_name = "users/user_list.html"
    model = users.models.User
    context_object_name = "users"
    queryset = users.models.User.objects.only(
        users.models.User.username.field.name,
    ).all()


class UserDetailView(DetailView):
    template_name = "users/user_detail.html"
    model = users.models.User
    context_object_name = "user"

    def get_queryset(self):
        return users.models.User.objects.select_related("profile").only(
            users.models.User.username.field.name,
            users.models.User.email.field.name,
            users.models.User.first_name.field.name,
            users.models.User.last_name.field.name,
            users.models.User.is_active.field.name,
        )


class UserProfileMultiForm(MultiModelForm):
    form_classes = {
        "user_form": UserChangeForm,
        "profile_form": UserProfileChangeForm,
    }


@method_decorator(login_required, name="dispatch")
class ProfileEditView(View):
    template_name = "users/profile.html"

    def get(self, request, *args, **kwargs):
        user_form = UserChangeForm(instance=request.user)
        profile_form = UserProfileChangeForm(instance=request.user.profile)
        return render(
            request,
            self.template_name,
            {"user_form": user_form, "profile_form": profile_form},
        )

    def post(self, request, *args, **kwargs):
        user_form = UserChangeForm(request.POST, instance=request.user)
        profile_form = UserProfileChangeForm(
            request.POST,
            request.FILES,
            instance=request.user.profile,
        )

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, "Profile updated successfully!")
            return redirect("users:profile")

        return render(
            request,
            self.template_name,
            {"user_form": user_form, "profile_form": profile_form},
        )
