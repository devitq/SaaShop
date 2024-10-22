from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from feedback.models import Feedback, FeedbackFile, PersonalData, StatusLog

__all__ = ()


class FilesInline(admin.TabularInline):
    model = FeedbackFile
    extra = 1


class PersonalDataInline(admin.TabularInline):
    model = PersonalData
    can_delete = False
    max_num = 1
    min_num = 1


class FeedbackAdmin(admin.ModelAdmin):
    list_display = [
        "title",
        "author",
        Feedback.status.field.name,
    ]
    inlines = [
        FilesInline,
        PersonalDataInline,
    ]

    def save_model(self, request, obj, form, change):
        original_status = None

        if obj.pk:
            original_status = Feedback.objects.get(pk=obj.pk).status

        super().save_model(request, obj, form, change)

        if original_status and original_status != obj.status:
            StatusLog.objects.create(
                user=request.user,
                feedback=obj,
                from_status=original_status,
                to=obj.status,
            )

    def title(self, obj):
        return obj

    title.short_description = _("title_models")


class StatusLogAdmin(admin.ModelAdmin):
    list_display = [
        "title",
        StatusLog.user.field.name,
        StatusLog.from_status.field.name,
        StatusLog.to.field.name,
    ]
    readonly_fields = [
        StatusLog.feedback.field.name,
        StatusLog.user.field.name,
        StatusLog.from_status.field.name,
        StatusLog.to.field.name,
    ]

    def title(self, obj):
        return obj

    title.short_description = _("title_models")


admin.site.register(Feedback, FeedbackAdmin)
admin.site.register(StatusLog, StatusLogAdmin)
admin.site.register(PersonalData)
admin.site.register(FeedbackFile)
