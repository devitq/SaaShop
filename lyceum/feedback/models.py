from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import gettext_lazy as _

__all__ = ("Feedback", "StatusLog")


class Feedback(models.Model):
    RECEIVED = "R"
    PROCESSING = "P"
    ANSWERED = "A"
    STATUS_CHOICES = [
        (RECEIVED, "получено"),
        (PROCESSING, "в обработке"),
        (ANSWERED, "ответ дан"),
    ]
    status = models.CharField(
        _("status_feedback_models"),
        max_length=1,
        choices=STATUS_CHOICES,
        default=RECEIVED,
    )
    mail = models.EmailField(_("mail_models"))
    text = models.TextField(_("text_models"))
    created_on = models.DateTimeField(
        _("created_at_utc_models"),
        null=True,
        auto_now_add=True,
    )

    class Meta:
        verbose_name = _("feedback_models")
        verbose_name_plural = _("feedbacks_models")


class StatusLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    feedback = models.ForeignKey(Feedback, on_delete=models.CASCADE)
    from_status = models.CharField(max_length=1)
    to_status = models.CharField(max_length=1)
    timestamp = models.DateTimeField(
        auto_now_add=True,
        null=True,
    )

    class Meta:
        verbose_name = _("status_log_models")
        verbose_name_plural = _("status_logs_models")
