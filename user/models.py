from django.db import models
from django.contrib.auth.models import AbstractUser, UserManager
from django.core.exceptions import ValidationError


class PhoneNumber(models.Model):
    number = models.CharField(max_length=11, verbose_name="شماره تلفن")

    def __str__(self):
        return str(self.number)


class Manager(UserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not password:
            raise ValidationError('The password must be set.')

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)


class User(AbstractUser):
    gender_types = (("male", "مرد"), ("female", "زن"))
    gender = models.CharField(choices=gender_types, max_length=6, default="male")
    number = models.ForeignKey(PhoneNumber, on_delete=models.CASCADE, blank=True, null=True, verbose_name="شماره")
    special_time = models.DateTimeField(blank=True, null=True, verbose_name="مدت اشتراک")
    objects = Manager()

    class Meta:
        verbose_name = "کاربر"
        verbose_name_plural = "کاربرها"



    def __str__(self):
        return self.get_full_name() if self.get_full_name() else self.username


class Pakage(models.Model):
    title = models.CharField(max_length=150, verbose_name="موضوع")
    image = models.ImageField(blank=True, upload_to='images', verbose_name="عکس")
    description = models.TextField(verbose_name="جزیات")
    price = models.PositiveIntegerField(verbose_name="قیمت")
    is_active = models.BooleanField(default=True, verbose_name="فعال")
    discountPrice = models.PositiveIntegerField(default=0, verbose_name="قیمت تخفیف خورده")
    dates = models.IntegerField(verbose_name="مدت بسته")

    class Meta:
        verbose_name = 'بسته'
        verbose_name_plural = 'بسته ها'
        ordering = ['price']


    def get_price(self):
        return self.price - self.discountPrice

    def __str__(self):
        return self.title


class Subscription(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="کاربر")
    pakage = models.ForeignKey(Pakage, on_delete=models.SET_NULL, null=True, verbose_name="پکیج")
    price = models.PositiveIntegerField(verbose_name="قیمت")
    days = models.IntegerField(verbose_name="مدت اشتراک")
    actived_at = models.DateTimeField(auto_now_add=True, verbose_name="زمان خرید")

    class Meta:
        verbose_name = 'اشتراک'
        verbose_name_plural = 'اشتراک ها'


    def __str__(self):
        return f"{self.user}: {self.price}"


class Ticket(models.Model):
    departeman_types = (('finance and sales', 'مالی و فروش'), ('technical', 'پشتیبانی فنی'))
    title = models.CharField(max_length=200, verbose_name="عنوان تیکت")
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='سازنده')
    departeman = models.CharField(choices=departeman_types, max_length=17, default='finance and sales', verbose_name='دپارتمان')
    update_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'تیکت'
        verbose_name_plural = 'تیکت ها'
        ordering = ['-update_at']

    def __str__(self):
        return f'{self.user}: {self.title[:50]} ...'


class MessageSupport(models.Model):
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE, verbose_name='تیکت')
    message = models.TextField(verbose_name = 'پیام')
    sender = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='فرستنده')

    class Meta:
        verbose_name = 'پیام پشتیبانی'
        verbose_name_plural = 'پیام های پشتیبانی'


    def __str__(self):
        return self.sender.__str__()
