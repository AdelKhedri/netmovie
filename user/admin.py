from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, PhoneNumber, Pakage, Subscription, Ticket, MessageSupport
from .forms import UserChangeForm, UserCreationForm
from django.utils.html import format_html


admin.site.register(PhoneNumber)

@admin.register(User)
class UserAdmin(BaseUserAdmin):
    model = User
    form = UserChangeForm
    add_form = UserCreationForm

    list_display = ['username', 'email', 'number', 'is_active', 'special_time']
    list_filter = ['is_active', 'is_superuser', 'is_staff']
    fieldsets = (
        (
            None,
            {'fields': [('email', 'username'), 'number', 'password']}
        ),
        (
            'Seens',
            {'fields': [('date_joined', 'special_time')]}
        ),
        (
            'Personal info',
            {'fields': [('first_name', 'last_name', 'gender')]}
        ),
        (
            'Permissions',
            {'fields': ['is_active', 'is_superuser', 'is_staff', 'groups', 'user_permissions']}
        ),
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



@admin.register(Pakage)
class PakageAdmin(admin.ModelAdmin):
    list_display = ['title', 'price', 'discountPrice', 'get_image']
    list_filter = ['is_active', ]
    
    def get_image(self, obj):
        return format_html(f'<img width="100px" hieght="100px" src="{obj.image.url if obj.image else ""}" alt="not image">')


@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ['user', 'pakage', 'days', 'price']
    search_fields = ['user']


@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = ['title', 'user', 'departeman']
    search_fields = ['title']
    list_filter = ['departeman']


@admin.register(MessageSupport)
class MessageSupportAdmin(admin.ModelAdmin):
    list_display = ['sender', 'ticket', 'get_simple_message']

    @admin.display(description='متن پیام')
    def get_simple_message(self, obj):
        return f'{obj.message[:100]} ...'