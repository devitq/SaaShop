from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User

from users.models import Profile

__all__ = ()


class ProfileInline(admin.TabularInline):
    model = Profile
    can_delete = False
    readonly_fields = (
        Profile.coffee_count.field.name,
        Profile.attempts_count.field.name,
        Profile.blocked_timestamp.field.name,
    )


class UserAdmin(BaseUserAdmin):
    inlines = (ProfileInline,)


admin.site.unregister(User)
admin.site.register(User, UserAdmin)
