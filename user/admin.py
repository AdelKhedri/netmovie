from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, PhoneNumber
from .forms import UserChangeForm, UserCreationForm

admin.site.register(PhoneNumber)

@admin.register(User)
class UserAdmin(BaseUserAdmin):
    model = User
    form = UserChangeForm
    add_form = UserCreationForm

    list_display = ['username', 'email', 'number', 'is_active']
    list_filter = ['is_active', 'is_superuser', 'is_staff']
    fieldsets = (
        (
            None,
            {'fields': [('email', 'username'), 'number', 'password']}
        ),
        (
            'Personal info',
            {'fields': [('first_name', 'last_name', 'gender')]}
        ),
        (
            'Permissions',
            {'fields': ['is_active', 'is_superuser', 'is_staff', 'groups', 'user_permissions']}
        ),
        (
            'Seens',
            {'fields': [('date_joined')]}
        )
    )

    add_fieldsets = [
        (
            None,
            {
                "classes": ["wide"],
                "fields": ["username", "is_active", "password1", "password2"],
            },
        ),
    ]
