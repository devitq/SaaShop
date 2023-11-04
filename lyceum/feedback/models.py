from django.db import models

__all__ = ("Feedback",)


class Feedback(models.Model):
    text = models.TextField("текст")
    created_at = models.DateTimeField(
        "дата создания",
        null=True,
        auto_now_add=True,
    )
    mail = models.EmailField("почта")
