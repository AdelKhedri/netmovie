from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, PhoneNumber, Pakage, Subscription, Ticket, MessageSupport, Request
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
    list_display = ['title', 'user', 'get_status', 'departeman']
    search_fields = ['title']
    list_filter = ['departeman']

    @admin.display(description = 'وضعیت')
    def get_status(self, obj):
        if obj.status == 'pending':
            color = 'amber'
        elif obj.status == 'answered':
            color = 'green'
        elif obj.status == 'closed':
            color = 'red'
        else:
            color = ''
        return format_html(f'<span class="bg-{color}-500/30 text-{color}-500 rounded-lg p-1">{obj.get_status_display()} </span>')
    
    
    class Media:
        css = {
            'all': ['admin/css/style.css']
        }


@admin.register(MessageSupport)
class MessageSupportAdmin(admin.ModelAdmin):
    list_display = ['sender', 'ticket', 'get_simple_message']

    @admin.display(description='متن پیام')
    def get_simple_message(self, obj):
        return f'{obj.message[:100]} ...'


@admin.register(Request)
class RequestAdmin(admin.ModelAdmin):
    list_display = ['name', 'user', 'year', 'get_status']
    list_filter = ['status']
    search_fields = ['name', 'user']

    @admin.display(description='وضعیت')
    def get_status(self, obj):
        if obj.status == 'pending':
            color = 'amber'
        elif obj.status == 'accept':
            color = 'green'
        elif obj.status == 'reject':
            color = 'red'
        else:
            color = ''
        response = format_html(f'<span class="bg-{color}-500/30 text-{color}-500 rounded-lg p-1">{obj.get_status_display()} </span>')
        return response
    
    class Media:
        css = {
            'all': ['admin/css/style.css']
        }