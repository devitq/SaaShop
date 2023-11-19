import re
import zoneinfo

from django.conf import settings
from django.utils import timezone

__all__ = ("ReverseRussianMiddleware",)


class ReverseRussianMiddleware:
    count = 0

    def __init__(self, get_response):
        self.get_response = get_response

    @classmethod
    def check_need_reverse(cls):
        if not settings.ALLOW_REVERSE:
            return False

        cls.count += 1
        if cls.count != 10:
            return False
        cls.count = 0
        return True

    def __call__(self, request):
        if not self.check_need_reverse():
            return self.get_response(request)

        response = self.get_response(request)
        response.content = self.reverse_russian_words(
            response.content.decode(),
        )

        return response

    def reverse_russian_words(self, s):
        russian_word_regex = r"\b[а-яА-ЯёЁ]+\b"
        return re.sub(
            russian_word_regex,
            lambda match: match.group()[::-1],
            s,
        )


class TimezoneMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        try:
            tzname = request.COOKIES.get("django_timezone")
            if tzname:
                timezone.activate(zoneinfo.ZoneInfo(tzname))
            else:
                timezone.deactivate()
        except Exception:
            timezone.deactivate()

        return self.get_response(request)
