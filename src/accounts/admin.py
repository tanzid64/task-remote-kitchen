from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUSerAdmin
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _

User = get_user_model()

# Register your models here.
@admin.register(User)
class UserAdmin(BaseUSerAdmin):
    list_display = (
        "id", 
        "email", 
        "username", 
        "user_type",
        "is_superuser",
    )
    list_display_links = ("id", "email", "username", )
    search_fields = ("email", "username", "first_name", "last_name", )
    ordering = ("-date_joined", )
    fieldset = (
        (_("Login Credentials"), {"fields": ("username", "password")}),
        (_("Personal Info"), {"fields": ("first_name", "last_name", "email", "user_type")}),
        (_("Permissions and Groups"), {"fields": ("is_superuser", "is_staff", "groups", "user_permission" )}),
        (_("Important dates"), {"fields": ("last_login", "date_joined")}),
    )

