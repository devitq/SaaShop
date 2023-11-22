from django.contrib import admin

from rating.forms import RatingAdminForm
from rating.models import Rating

__all__ = ()


class RatingAdmin(admin.ModelAdmin):
    form = RatingAdminForm


admin.site.register(Rating, RatingAdmin)
