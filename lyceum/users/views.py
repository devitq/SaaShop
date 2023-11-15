from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.core.signing import BadSignature, SignatureExpired, TimestampSigner
from django.shortcuts import redirect, render
from django.urls import reverse, reverse_lazy
from django.utils import timezone
from django.views.generic import (
    CreateView,
    DetailView,
    ListView,
    View,
)

from users.forms import (
    UserChangeForm,
    UserForm,
    UserSignupForm,
)


__all__ = ()


class ActivateAccountView(View):
    def get(self, request, token):
        signer = TimestampSigner()
        try:
            username = signer.unsign(
                token,
                max_age=timezone.timedelta(hours=12),
            )
            user = User.objects.get(username=username)
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
            user = User.objects.get(username=username)
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
    model = User
    context_object_name = "users"
    queryset = User.objects.only(
        User.username.field.name,
    ).all()


class UserDetailView(DetailView):
    template_name = "users/user_detail.html"
    model = User
    context_object_name = "user"

    def get_queryset(self):
        return User.objects.select_related("profile").only(
            User.username.field.name,
            User.email.field.name,
            User.first_name.field.name,
            User.last_name.field.name,
            User.is_active.field.name,
        )


@login_required
def profile_edit(request):
    user_form = UserForm(instance=request.user)
    profile_form = UserChangeForm(instance=request.user.profile)

    if request.method == "POST":
        user_form = UserForm(request.POST, instance=request.user)
        profile_form = UserChangeForm(
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
        "users/profile.html",
        {"user_form": user_form, "profile_form": profile_form},
    )
