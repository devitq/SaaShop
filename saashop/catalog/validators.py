import re

from django.core.exceptions import ValidationError
from django.core.validators import BaseValidator
from django.utils.deconstruct import deconstructible

__all__ = ("ValidateMustContain",)


@deconstructible
class ValidateMustContain(BaseValidator):
    regex_pattern = r"\b({})\b"

    def __init__(self, *words_to_check, message=None, code=None):
        self.words_to_check = words_to_check
        self.regex_pattern = re.compile(
            self.regex_pattern.format(
                "|".join(words_to_check),
            ),
        )
        super().__init__(message, code)

    def __call__(self, value):
        if not self.regex_pattern.findall(value.lower()):
            formatted_words = ", ".join(self.words_to_check)
            raise ValidationError(
                f'"{value}" не содержит слова из списка: {formatted_words}',
            )
