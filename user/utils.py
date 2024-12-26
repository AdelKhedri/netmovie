from django.utils import timezone


def get_left_special_time(user):
    if user.special_time and user.special_time > timezone.now():
        current_time = (user.special_time - timezone.now())
        return current_time.days
    else:
        return 0

def get_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.splite(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip