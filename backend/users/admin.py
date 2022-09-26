from django.contrib import admin
from users.models import CustomUser


class CustomUserAdmin(admin.ModelAdmin):
    list_display = ("id", "username", "email", "first_name", "last_name")
    search_fields = ("username", "email")
    list_filter = ("username", "email")
    ordering = ("email",)
    fieldsets = (
        (None, {"fields": ("username", "email", "password")}),
        ("Personal", {"fields": ("first_name", "last_name")}),
        ("Permissions", {"fields": ("is_staff", "is_active")}),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("email", "password1", "password2", "is_staff", "is_active"),
            },
        ),
    )


admin.site.register(CustomUser, CustomUserAdmin)
