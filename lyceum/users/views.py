from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail
from django.shortcuts import redirect, render
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.utils import timezone
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
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
from users.tokens import account_activation_token


__all__ = ()


class ActivateAccountView(View):
    def get(self, request, uidb64, token):
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

        if user is not None and account_activation_token.check_token(
            user,
            token,
        ):
            if (timezone.now() - user.date_joined).seconds < 43200:
                user.is_active = True
                user.save()
                messages.success(
                    self.request,
                    "Your account has been successfully activated.",
                )
            else:
                messages.error(
                    self.request,
                    "Activation link has expired. Please register again.",
                )
        else:
            messages.error(self.request, "Invalid activation link.")

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
            message = render_to_string(
                "users/account_activation_email.html",
                {
                    "user": user,
                    "domain": get_current_site(self.request).domain,
                    "uid": urlsafe_base64_encode(
                        force_bytes(user.pk),
                    ),
                    "token": account_activation_token.make_token(user),
                },
            )
            send_mail(
                "Activate Your Account",
                message,
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
