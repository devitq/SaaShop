from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _

__all__ = ("Feedback", "StatusLog")


def upload_file_to_path(instance, filename):
    return f"uploads/{instance.feedback.id}/{filename}"


class PersonalData(models.Model):
    name = models.CharField(
        _("name_models"),
        max_length=1478,
        null=True,
        blank=True,
    )
    mail = models.EmailField(
        _("mail_models"),
    )

    class Meta:
        verbose_name = _("personal_data_models")
        verbose_name_plural = _("personal_datas_models")


class Feedback(models.Model):
    RECEIVED = "R"
    PROCESSING = "P"
    ANSWERED = "A"
    STATUS_CHOICES = [
        (RECEIVED, _("received")),
        (PROCESSING, _("processing")),
        (ANSWERED, _("answered")),
    ]
    author = models.ForeignKey(
        PersonalData,
        verbose_name=_("author"),
        related_name="feedbacks",
        on_delete=models.CASCADE,
        null=False,
    )
    status = models.CharField(
        _("status_feedback_models"),
        max_length=1,
        choices=STATUS_CHOICES,
        default=RECEIVED,
    )
    text = models.TextField(
        _("text_models"),
    )
    created_on = models.DateTimeField(
        _("created_at_utc_models"),
        null=True,
        auto_now_add=True,
    )

    def __str__(self) -> str:
        return f"Обратная связь от, ID:{self.id}"

    class Meta:
        verbose_name = _("feedback_models")
        verbose_name_plural = _("feedbacks_models")


class StatusLog(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name=_("author"),
        on_delete=models.CASCADE,
    )
    feedback = models.ForeignKey(
        Feedback,
        verbose_name=_("feedback_models"),
        on_delete=models.CASCADE,
    )
    from_status = models.CharField(
        _("from_status_models"),
        max_length=1,
        choices=Feedback.STATUS_CHOICES,
        editable=False,
        db_column="from",
    )
    to = models.CharField(
        _("to_status_models"),
        max_length=1,
        choices=Feedback.STATUS_CHOICES,
        editable=False,
    )
    timestamp = models.DateTimeField(
        auto_now_add=True,
        null=True,
    )

    def __str__(self):
        return f'Изменение статуса для "{self.feedback.__str__()}"'

    class Meta:
        verbose_name = _("status_log_models")
        verbose_name_plural = _("status_logs_models")


class FeedbackFile(models.Model):
    feedback = models.ForeignKey(
        Feedback,
        on_delete=models.CASCADE,
        null=True,
        related_query_name="files",
        verbose_name=_("feedback_models"),
        related_name="files",
    )
    file = models.FileField(
        _("file_models"),
        upload_to=upload_file_to_path,
        null=True,
    )

    def __str__(self) -> str:
        return f"Файл обратной связи №{self.id}"

    class Meta:
        verbose_name = _("feedback_file_models")
        verbose_name_plural = _("feedback_files_models")
