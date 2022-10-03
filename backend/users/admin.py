from django.contrib import admin

from users.models import CustomUser, Subscribe


class CustomUserAdmin(admin.ModelAdmin):
    list_display = ("id", "username", "email", "first_name", "last_name")
    search_fields = ("username", "email")
    list_filter = ("is_staff", "is_superuser")
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


class SubscribeAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "user",
        "author",
    )
    search_fields = ("user__username", "user__email", "author__username", "author__email")


admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Subscribe, SubscribeAdmin)
