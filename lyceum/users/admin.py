from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
import django.contrib.auth.models

from users.forms import CreateUserAdminForm, EditUserAdminForm
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
    min_num = 1
    max_num = 1


class UserAdmin(BaseUserAdmin):
    inlines = (ProfileInline,)
    form = EditUserAdminForm
    add_form = CreateUserAdminForm
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("username", "email", "password1", "password2"),
            },
        ),
    )


admin.site.unregister(django.contrib.auth.models.User)
admin.site.register(django.contrib.auth.models.User, UserAdmin)
