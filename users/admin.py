from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import User


class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = User
    list_display = ("username", "email", "first_name", "last_name", "date_of_birth", "avatar", "city",
                    "country", "bio", "instagram", "telegram", "is_staff", "is_active", "all_tags", "is_verified")
    list_filter = ("username", "email", "first_name", "last_name", "date_of_birth", "avatar", "city",
                   "country", "bio", "instagram", "telegram", "is_staff", "is_active", 'tags', "is_verified")
    fieldsets = (
        (None, {"fields": ("username", "email", "first_name", "last_name", "date_of_birth", "avatar",
         "city", "country", "follows", "black_list", "bio", "instagram", "telegram", 'tags', "password", "is_verified")}),
        ("Permissions", {"fields": ("is_staff", "is_active")}),
    )
    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": (
                "username", "email", "first_name", "last_name", "date_of_birth", "avatar", "city", "country", "bio", "follows", "black_list", "instagram", "telegram", 'tags', "password1", "password2", "is_staff",
                "is_active", "is_verified"
            )}
         ),
    )
    search_fields = ("username", "email")
    ordering = ("username", "email")


admin.site.register(User, CustomUserAdmin)
