from django.contrib import admin
from django.utils.html import format_html
from django.contrib.contenttypes.models import ContentType
from .models import (
    Actor, Ganers, DownloadLink, Quality, Section, Serial, Movie, MovieComment,
    SerialComment)


# Inlines

class MovieCommentInline(admin.TabularInline):
    model = MovieComment
    raw_id_fields = ['user', 'movie']
    extra = 4


class SerialCommentInline(admin.TabularInline):
    model = SerialComment
    raw_id_fields = ['user', 'serial']
    extra = 4


# Mixins
class MediaMethods:
    @admin.display(description='ژانر ها')
    def get_ganers(self, obj):
        html = ''
        for i in obj.ganers.all():
            html += f'<span>{i.name}</span>'
        return format_html(html)

    @admin.display(description='عکس کوچک فیلم')
    def get_baner(self, obj):
        return format_html(f'<img src="{obj.baner.url if obj.baner else ""}" style="width:100px;height:130px;">')


# Registraions
@admin.register(Actor)
class ActorAdmin(admin.ModelAdmin):
    list_display = ['name', 'imdb_link', 'get_photo']

    @admin.display(description='عکس بازیگر')
    def get_photo(self, obj):
        return format_html(f'<img src="{obj.photo.url if obj.photo else ""}" style="width:100px;heigth:130px;">')


@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin, MediaMethods):
    list_display = ['name', 'get_ganers', 'year_create', 'release_date', 'point', 'get_baner']
    list_filter = ['ganers', ]
    search_fields = ['name', 'persian_name', 'description', 'slug', ]
    inlines = [MovieCommentInline, ]


@admin.register(Serial)
class SeriaAdmin(admin.ModelAdmin, MediaMethods):
    list_display = ['name', 'get_ganers', 'year_create', 'release_date', 'point', 'get_baner']
    list_filter = ['ganers', ]
    search_fields = ['name', 'persian_name', 'description', 'slug', ]
    inlines = [SerialCommentInline, ]


@admin.register(ContentType)
class ContentTypeAdmin(admin.ModelAdmin):
    list_display = ['model']
    search_fields = ['content_type']


admin.site.register(Ganers)
admin.site.register(DownloadLink)
admin.site.register(Quality)
admin.site.register(Section)
admin.site.register(MovieComment)
admin.site.register(SerialComment)