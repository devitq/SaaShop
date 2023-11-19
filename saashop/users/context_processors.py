from django.utils import timezone
import pytz

from users.models import User

__all__ = ("birthday_context",)


def birthday_context(request):
    tzname = request.COOKIES.get("django_timezone", "UTC")
    today = timezone.now().astimezone(pytz.timezone(tzname)).date()
    users_with_birthday = (
        User.objects.select_related("profile")
        .filter(
            profile__birthday__day=today.day,
            profile__birthday__month=today.month,
            is_active=True,
        )
        .only("username", "profile__birthday")
    )

    return {
        "users_with_birthday": users_with_birthday,
    }
