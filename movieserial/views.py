from django.shortcuts import get_list_or_404, render
from .models import Ganers, Movie, Quality, Section, Serial, SerialComment
from django.views.generic import View
from user.utils import get_left_special_time
from django.db.models import Count, Sum, Prefetch
from .forms import SerialCommantForm


class HomeView(View):
    template_name = 'movieserial/home.html'

    def get(self, request, *args, **kwargs):
        # FIXME: problem on buy subscription after some days ago of buy subscription
        context = {
            'movies': Movie.objects.prefetch_related('ganers').all()[:14],
            'serials': Serial.objects.all()[:8],
            'serial_ganers': Ganers.objects.prefetch_related('serial_set').annotate(count = Count('serial')),
            'movie_ganers': Ganers.objects.prefetch_related('movie_set').annotate(count = Count('movie')),
            'serial_counts': Serial.objects.count(),
            'movie_counts': Movie.objects.count(),
            'page_name': 'home',
            'title_page': 'نت موی',
        }

        if request.user.is_authenticated:
            context.update({'special_time': get_left_special_time(request.user)})

        return render(request, self.template_name, context)


class SerialDetailsView(View):
    template_name = 'movieserial/details.html'

    def setup(self, request, slug, *args, **kwargs):
        sections_with_qualitys_and_total_size = Prefetch(
            'sections',
            queryset=Section.objects.prefetch_related(
                Prefetch(
                    'qualitys',
                    queryset = Quality.objects.prefetch_related('episodes').annotate(
                        total_size = Sum('episodes__size')
                    )
                )
            )
        )
        self.serial = Serial.objects.filter(slug = slug).prefetch_related(sections_with_qualitys_and_total_size).first()
        comments = SerialComment.objects.filter(serial = self.serial, parent_comment__isnull = True)
        comments_count = SerialComment.objects.filter(serial = self.serial).count()
        self.context = {
            'object': self.serial,
            'page_name': 'serial-details',
            'comments': comments,
            'comment_form': SerialCommantForm(),
            'comment_counts': comments_count
        }
        super().setup(request, slug, *args, **kwargs)


    def get(self, request, slug, *args, **kwargs):
        return render(request, self.template_name, self.context)

    def post(self, request, slug, *args, **kwargs):
        form = SerialCommantForm(request.POST, user = request.user, serial = self.serial)
        if form.is_valid():
            form.save()
        else:
            self.context['comment_form'] = form
        return render(request, self.template_name, self.context)
