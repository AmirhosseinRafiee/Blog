from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth import get_user_model
from .models import Profile

User = get_user_model()


class CustomUserAdmin(UserAdmin):
    model = User
    list_display = ('email', 'is_superuser', 'is_verified', 'is_active')
    list_filter = ('email', 'is_superuser', 'is_verified', 'is_active')
    searching_fields = ('email',)
    ordering = ('email',)
    fieldsets = (
        ('Authentication', {
            "fields": (
                'email', 'password'
            ),
        }),
        ('permissions', {
            "fields": (
                'is_verified', 'is_staff', 'is_active', 'is_superuser'
            ),
        }),
        ('group permissions', {
            "fields": (
                'groups', 'user_permissions'
            ),
        }),
        ('important date', {
            "fields": (
                'last_login',
            ),
        }),

    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1','password2', 'is_verified', 'is_staff', 'is_active', 'is_superuser')}
         ),
    )

admin.site.register(User, CustomUserAdmin)
admin.site.register(Profile)