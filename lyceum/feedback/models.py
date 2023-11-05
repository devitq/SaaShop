from django.db import models

__all__ = ("Feedback",)


class Feedback(models.Model):
    mail = models.EmailField("почта")
    text = models.TextField("текст")
    created_on = models.DateTimeField(
        "дата создания",
        null=True,
        auto_now_add=True,
    )
