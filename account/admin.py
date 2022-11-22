from django.contrib import admin
from .models import User
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin


class UserAdmin(BaseUserAdmin):

    list_display = ("id", "email", "name", "tc", "is_admin")
    list_filter = ("is_admin",)
    fieldsets = (
        ("User Credentials", {"fields": ("email", "password")}),
        ("Personal info", {"fields": ("name", "tc")}),
        ("Permissions", {"fields": ("is_admin",)}),
    )
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("email", "name", "password1", "tc", "password2"),
            },
        ),
    )
    search_fields = ("email",)
    ordering = ("email", "id")
    filter_horizontal = ()


# Now register the new UserAdmin...
admin.site.register(User, UserAdmin)
