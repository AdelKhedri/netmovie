from django.core.exceptions import ValidationError
from .models import PhoneNumber, User


def validate_phone_number(value):
    if str(value)[0:2] != '09':
        raise ValidationError('شماره تلفن اشتباه است')
    elif len(str(value)) != 11:
        raise ValidationError('شماره تلفن اشتباه است')
    if PhoneNumber.objects.filter(number=value).exists():
        raise ValidationError('شماره تلفن قبلا استفاده شده')

def validate_username(value):
    if User.objects.filter(username=value).exists():
        raise ValidationError('نام کاربری تکراری است')
