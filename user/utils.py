from django.utils import timezone


def get_left_special_time(user):
    if user.special_time:
        current_time = (user.special_time - timezone.now())
        return current_time.days
    else:
        return 0
