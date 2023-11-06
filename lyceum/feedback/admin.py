from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from feedback.models import Feedback, StatusLog

__all__ = ()


class FeedbackAdmin(admin.ModelAdmin):
    def save_model(self, request, obj, form, change):
        original_status = None

        if obj.pk:
            original_status = Feedback.objects.get(pk=obj.pk).status

        super().save_model(request, obj, form, change)

        if original_status and original_status != obj.status:
            StatusLog.objects.create(
                user=request.user,
                feedback=obj,
                From=original_status,
                To=obj.status,
            )


class StatusLogAdmin(admin.ModelAdmin):
    list_display = [
        "title",
        StatusLog.From.field.name,
        StatusLog.To.field.name,
    ]
    readonly_fields = [
        StatusLog.From.field.name,
        StatusLog.To.field.name,
    ]

    def title(self, obj):
        return f'Изменение статуса для "{obj.feedback.__str__()}"'

    title.short_description = _("title_models")


admin.site.register(Feedback, FeedbackAdmin)
admin.site.register(StatusLog,  StatusLogAdmin)
