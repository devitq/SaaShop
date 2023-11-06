from django.contrib import admin

from feedback.models import Feedback, StatusLog

__all__ = ()


class FeedbackAdmin(admin.ModelAdmin):
    def save(self, *args, **kwargs):
        if self.pk:
            original_status = Feedback.objects.get(pk=self.pk).status
            if original_status != self.status:
                StatusLog.objects.create(
                    user=self.user,
                    feedback=self,
                    from_status=original_status,
                    to_status=self.status,
                )
        super().save(*args, **kwargs)

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
                to_status=obj.status,
            )


admin.site.register(Feedback, FeedbackAdmin)
admin.site.register(StatusLog)
