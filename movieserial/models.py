from django.db import models
from django.contrib.contenttypes import fields, models as c_model
from django.core.validators import MaxValueValidator, MinValueValidator
from user.models import User
from functools import partial


def folder_finder(instance, filename, folder):
    class_name = instance.__class__.__name__.lower()
    _type = 'movies' if class_name == 'movie' else 'serials'
    folder_path = f'images/{_type}/{folder}/{filename}'
    return folder_path


class Actor(models.Model):
    name = models.CharField(max_length=150, verbose_name='نام')
    photo = models.ImageField(upload_to='images/actor/', blank=True, verbose_name='عکس')
    imdb_link = models.URLField(blank=True, verbose_name='ادرس imdb')

    class Meta:
        verbose_name = 'بازیگر'
        verbose_name_plural = 'بازیگر ها'
        ordering = ['name']


    def __str__(self):
        return f'{self.name}: {self.id}'


class Ganers(models.Model):
    name = models.CharField(max_length=150, verbose_name='نام')
    slug = models.SlugField(unique=True, verbose_name='اسلاگ')

    class Meta:
        verbose_name = 'ژانر'
        verbose_name_plural = 'ژانر ها'
        ordering = ['name']


    def __str__(self):
        return self.name


class BaseMedia(models.Model):
    name = models.CharField(max_length=300, verbose_name='نام')
    persian_name = models.CharField(max_length=200, verbose_name='نام فارسی')
    ganers = models.ManyToManyField(Ganers, verbose_name='ژانر ها')
    description = models.CharField(max_length=500, blank=True, verbose_name='درباره')
    stars = models.ManyToManyField(Actor, blank=True, verbose_name='ستارگان')
    info = models.CharField(max_length=200, blank=True, verbose_name='جزیات')
    baner = models.ImageField(upload_to=partial(folder_finder, folder='baner'), verbose_name='عکس فیلم')
    background_baner = models.ImageField(upload_to=partial(folder_finder, folder='backgrounds'), blank=True, verbose_name='بک گراند')
    slug = models.SlugField(unique=True, verbose_name='اسلاگ')
    trailer = models.URLField(blank=True, verbose_name='تریلر')
    online_play = models.URLField(blank=True, verbose_name='لینک تماشای انلاین')
    imdb_link = models.URLField(blank=True, verbose_name='لینک(ارجاع به  imdb)')
    year_create = models.IntegerField(verbose_name='سال ساخت')
    duration = models.TimeField(verbose_name='زمان')
    release_date = models.DateTimeField(verbose_name='زمان پخش')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='زمان ساخت')
    is_subtitle = models.BooleanField(default=True, verbose_name='زیرنویس')
    is_sound_translate = models.BooleanField(default=False, verbose_name='دوبله')
    point = models.DecimalField(
                                max_digits=4,
                                decimal_places=2,
                                validators=[
                                    MaxValueValidator(10.0,),
                                    MinValueValidator(0.0)
                                    ],
                                verbose_name='امتیاز imdb'
                                )


    class Meta:
        abstract = True
        ordering = ['name']


    def __str__(self):
        return self.name


class DownloadLink(models.Model):
    name = models.CharField(max_length=150, verbose_name='نام')
    link = models.URLField(verbose_name='لینک دانلود مستقیم')
    size = models.IntegerField(verbose_name='اندازه')
    is_subtitle = models.BooleanField(default=True, verbose_name='زیرنویس')
    subtitle_types = (('nosub', 'بدون زیرنویس'), ('subsoft', 'subsoft'),)
    subtitle_type = models.CharField(max_length=150, choices=subtitle_types, verbose_name='نوع زیرنویس')
    is_persian_sound = models.BooleanField(verbose_name='ضدای فارسی')

    class Meta:
        verbose_name = 'لینک دانلود'
        verbose_name_plural = 'لینک های دانلود'
        ordering = ['name']


    def __str__(self):
        return f'{self.name}: {self.id}'


class Quality(models.Model):
    name = models.CharField(max_length=150, verbose_name='نام')
    episodes = models.ManyToManyField(DownloadLink, verbose_name='قسمت ها')

    class Meta:
        verbose_name = 'کیفیت'
        verbose_name_plural = 'کیفیت ها'
        ordering = ['name']


    def __str__(self):
        return f'{self.name}: {self.id}'


class Section(models.Model):
    name = models.CharField(max_length=150, verbose_name='نام')
    qualitys = models.ManyToManyField(Quality, verbose_name='کیفیت ها')
    status_types = (('creating', 'درحال تولید'),('completed', 'تکمیل شده'), ('canceled', 'کنسل شده'))
    status = models.CharField(max_length=150, choices=status_types, verbose_name='وضعیت')

    class Meta:
        verbose_name = 'بخش'
        verbose_name_plural = 'بخش ها'
        ordering = ['name']


    def __str__(self):
        return f'{self.name}: {self.id}'


class Serial(BaseMedia):
    sections = models.ManyToManyField(Section, blank=True, verbose_name='بخش ها')
    last_episod = models.CharField(max_length=200, verbose_name='آخرین قسمت')
    last_section = models.ForeignKey(Section, blank=True, null=True, on_delete=models.CASCADE, related_name='last_section', verbose_name='آخرین فصل')

    class Meta:
        verbose_name = 'سریال'
        verbose_name_plural = 'سریال ها'
        ordering = ['name']


    def __str__(self):
        return f'{self.name}: {self.id}'


class Movie(BaseMedia):
    qualitys = models.ManyToManyField(Quality, verbose_name='کیفیت ها')

    class Meta:
        verbose_name = 'سینمایی'
        verbose_name_plural = 'سینمایی ها'
        ordering = ['name']


    def __str__(self):
        return f'{self.name}: {self.id}'


class BaseComment(models.Model):
    text = models.TextField(verbose_name='متن')
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='کاربر ارسال کننده')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='زمان ساخت')
    is_spoil = models.BooleanField(default=False, verbose_name='نظر حاوی اسپویل')



class MovieComment(BaseComment):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, verbose_name='سینمایی')
    parent_comment = models.ForeignKey('MovieComment', on_delete=models.CASCADE, null=True, blank=True, verbose_name='کامنت پرنت')

    class Meta:
        verbose_name = 'کامنت فیلم'
        verbose_name_plural = 'کامنت های فیلم'


    def __str__(self):
        return f'{self.user.__str__()}: {self.id}'



class SerialComment(BaseComment):
    serial = models.ForeignKey(Serial, on_delete=models.CASCADE, verbose_name='سریال')
    parent_comment = models.ForeignKey('SerialComment', on_delete=models.CASCADE, null=True, blank=True, verbose_name='کامنت پرنت')


    class Meta:
        verbose_name = 'کامنت سریال'
        verbose_name_plural = 'کامنت های سریال'


    def __str__(self):
        return f'{self.user.__str__()}: {self.id}'
