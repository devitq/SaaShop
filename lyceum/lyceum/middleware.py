import re

from django.conf import settings

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
        def reverse_word(match):
            return match.group()[::-1]

        res = re.sub(r"[а-яА-ЯёЁ]+", reverse_word, s)
        return res