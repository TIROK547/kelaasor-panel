from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _
from user.models import User

class UserAdmin(BaseUserAdmin):
    ordering = ['date_created']
    list_display = ['phone_number', 'email', 'user_name', 'is_staff']
    search_fields = ['phone_number', 'email', 'user_name']
    list_filter = ['is_staff', 'is_superuser', 'gender']

    fieldsets = (
        (None, {'fields': ('phone_number', 'password')}),
        (_('اطلاعات شخصی'), {'fields': ('email', 'user_name', 'national_id', 'gender')}),
        (_('دسترسی‌ها'), {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        (_('تاریخ‌ها'), {'fields': ('last_login',)}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('phone_number', 'password1', 'password2', 'is_staff', 'is_superuser'),
        }),
    )

admin.site.register(User, UserAdmin)
