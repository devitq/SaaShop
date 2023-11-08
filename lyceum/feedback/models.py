from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _

__all__ = ("Feedback", "StatusLog")


def upload_file_to_path(instance, filename):
    return f"uploads/{instance.feedback.id}/{filename}"


class Feedback(models.Model):
    RECEIVED = "R"
    PROCESSING = "P"
    ANSWERED = "A"
    STATUS_CHOICES = [
        (RECEIVED, _("received")),
        (PROCESSING, _("processing")),
        (ANSWERED, _("answered")),
    ]
    author = models.OneToOneField(
        "PersonalData",
        verbose_name=_("author_models"),
        related_name="feedbacks",
        on_delete=models.PROTECT,
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
        verbose = _("feedback_models").capitalize()
        from_verbose = _("from_in_text_models")
        return f"{verbose} {from_verbose} {self.author.mail}, ID:{self.id}"

    class Meta:
        verbose_name = _("feedback_models")
        verbose_name_plural = _("feedbacks_models")


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
    feedback = models.OneToOneField(
        Feedback,
        verbose_name=_("feedback_models"),
        related_name="feedbacks",
        on_delete=models.CASCADE,
        null=True,
    )

    def __str__(self) -> str:
        return self.mail

    class Meta:
        verbose_name = _("personal_data_models")
        verbose_name_plural = _("personal_datas_models")


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

    def __str__(self) -> str:
        verbose = _("status_log_models").capitalize()
        for_verbose = _("for_in_text_models")
        return f'{verbose} {for_verbose} "{self.feedback}"'

    class Meta:
        verbose_name = _("status_log_models")
        verbose_name_plural = _("status_logs_models")


class FeedbackFile(models.Model):
    def get_path_for_file(self, filename):
        return f"uploads/{self.feedback_id}/{filename}"

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
        upload_to=get_path_for_file,
        null=True,
    )

    def __str__(self) -> str:
        verbose = _("feedback_file_models").capitalize()
        return f"{verbose}, ID:{self.id}"

    class Meta:
        verbose_name = _("feedback_file_models")
        verbose_name_plural = _("feedback_files_models")
