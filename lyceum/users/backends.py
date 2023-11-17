from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend
from django.core.mail import send_mail
from django.core.signing import TimestampSigner
from django.urls import reverse
from django.utils import timezone

import users.models


__all__ = ("AuthenticationBackend",)


class AuthenticationBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        user_model = get_user_model()

        if username is None:
            username = kwargs.get(user_model.USERNAME_FIELD)
        if password is None or username is None:
            return None

        try:
            if "@" in username:
                email = users.models.User.objects.normalize_email(username)
                user = users.models.User.objects.by_mail(
                    email=email,
                )
            else:
                user = users.models.User.objects.get(username=username)
        except users.models.User.DoesNotExist:
            user_model().set_password(password)

        if user.check_password(password):
            user.profile.attempts_count = 0
            user.profile.save()
            return user

        user.profile.attempts_count += 1
        user.profile.save()

        if (
            user.profile.attempts_count >= settings.MAX_AUTH_ATTEMPTS
            and user.is_active is True
        ):
            self._deactivate_user(request, user)

        return None

    def _deactivate_user(self, request, user):
        user.is_active = False
        user.save()
        user.profile.blocked_timestamp = timezone.now()
        user.profile.save()

        signer = TimestampSigner()
        token = signer.sign(user.username)
        url = request.build_absolute_uri(
            reverse(
                    "users:reactivate_account",
                    kwargs={"token": token},
            ),
        )
        send_mail(
            "Reactivate Your Account",
            url,
            settings.MAIL,
            [user.email],
            fail_silently=False,
        )
