from django.http import Http404
from django.shortcuts import get_list_or_404, render
from .models import Ganers, Movie, MovieComment, Quality, Section, Serial, SerialComment
from django.views.generic import View
from user.utils import get_left_special_time
from django.db.models import Count, Sum, Prefetch
from .forms import SerialCommentForm, MovieCommentForm
from django.core.paginator import Paginator


def get_page(queryset, page, item_per_page):
    paginator = Paginator(queryset, item_per_page)
    page = page if str(page).isnumeric() else 1
    return paginator.page(page)


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
        if not self.serial:
            raise Http404()
        comments = SerialComment.objects.filter(serial = self.serial, parent_comment__isnull = True)
        comments_count = SerialComment.objects.filter(serial = self.serial).count()
        self.context = {
            'page_name': 'serial-details',
            'title_page': f'جزیات سریال {self.serial.name}',
            'serial_ganers': Ganers.objects.prefetch_related('serial_set').annotate(count = Count('serial')),
            'movie_ganers': Ganers.objects.prefetch_related('movie_set').annotate(count = Count('movie')),
            'serial_counts': Serial.objects.count(),
            'movie_counts': Movie.objects.count(),
            'object': self.serial,
            'comments': comments,
            'comment_form': SerialCommentForm(),
            'comment_count': comments_count
        }
        super().setup(request, slug, *args, **kwargs)


    def get(self, request, slug, *args, **kwargs):
        return render(request, self.template_name, self.context)

    def post(self, request, slug, *args, **kwargs):
        form = SerialCommentForm(request.POST, user = request.user, serial = self.serial)
        if form.is_valid():
            form.save()
        else:
            self.context['comment_form'] = form
        return render(request, self.template_name, self.context)


class MovieDetailsView(View):
    template_name = 'movieserial/details.html'

    def setup(self, request, slug, *args, **kwargs):
        try:
            self.movie = Movie.objects.get(slug = slug)
        except:
            raise Http404()
        
        movie_comments = MovieComment.objects.filter(movie = self.movie, parent_comment__isnull = True)
        comment_count = MovieComment.objects.filter(movie = self.movie).count()
        self.context = {
            'page_name': 'movie-details',
            'title_page': f'جزیات فیلم {self.movie.name}',
            'object': self.movie,
            'comments': movie_comments,
            'comment_count': comment_count,
            'comment_form': MovieCommentForm(),
            'serial_ganers': Ganers.objects.prefetch_related('serial_set').annotate(count = Count('serial')),
            'movie_ganers': Ganers.objects.prefetch_related('movie_set').annotate(count = Count('movie')),
            'serial_counts': Serial.objects.count(),
            'movie_counts': Movie.objects.count()
        }
        super().setup(request, slug, *args, **kwargs)

    def post(self, request, slug, *args, **kwargs):
        form = MovieCommentForm(request.POST, user = request.user, movie = self.movie)
        if form.is_valid():
            form.save()
        else:
            self.context['comment_form'] = form
        return render(request, self.template_name, self.context)

    def get(self, request, slug, *args, **kwargs):
        return render(request, self.template_name, self.context)


class SerialGanerView(View):
    template_name = 'movieserial/filter.html'

    def setup(self, request, slug, *args, **kwargs):
        self.context = {
            'page_name': 'serial-ganer',
            'ganers': Ganers.objects.all(),
            'serial_ganers': Ganers.objects.prefetch_related('serial_set').annotate(count = Count('serial')),
            'movie_ganers': Ganers.objects.prefetch_related('movie_set').annotate(count = Count('movie')),
            'serial_counts': Serial.objects.count(),
            'movie_counts': Movie.objects.count(),
        }

        try:
            ganer = Ganers.objects.get(slug = slug)
        except:
            raise Http404()

        self.serials = Serial.objects.filter(ganers=ganer)
        self.context.update({
            'ganer': ganer,
            'media_ganer': self.serials,
            'title_page': f'ژانر { ganer.name } | نت موی',
            })
        super().setup(request, slug, *args, **kwargs)

    def get(self, request, slug, *args, **kwargs):
        imdb_point = request.GET.get('point', None)
        ordering = request.GET.get('ordering', None)
        page = request.GET.get('page', 1)
        order_list = ['newset', 'imdb_point', 'release_year']

        if imdb_point and imdb_point.isnumeric():
            self.serials = self.serials.filter(point__gte = imdb_point)

        if ordering and ordering in order_list:
            if ordering == 'imdb_point':
                self.serials = self.serials.order_by('-point')
            elif ordering == 'release_year':
                self.serials = self.serials.order_by('year_create')
        self.context['media_ganer'] = get_page(self.serials, page, 21)

        return render(request, self.template_name, self.context)


class MovieGanerView(View):
    template_name = 'movieserial/filter.html'

    def setup(self, request, slug, *args, **kwargs):
        self.context = {
            'page_name': 'movie-ganer',
            'ganers': Ganers.objects.all(),
            'serial_ganers': Ganers.objects.prefetch_related('serial_set').annotate(count = Count('serial')),
            'movie_ganers': Ganers.objects.prefetch_related('movie_set').annotate(count = Count('movie')),
        }

        try:
            ganer = Ganers.objects.get(slug = slug)
        except:
            raise Http404()

        self.ganer_movies = Movie.objects.filter(ganers = ganer)
        self.context.update({
            'ganer': ganer,
            'ganer_movies': self.ganer_movies
        })
        super().setup(request, slug, *args, **kwargs)

    def get(self, request, slug, *args, **kwargs):
        imdb_point = request.GET.get('point', None)
        ordering = request.GET.get('ordering', None)
        page = request.GET.get('page', 1)
        ordering_list = ['newset', 'imdb_point', 'release_year']

        if ordering and ordering in ordering_list:
            if ordering == 'imdb_point':
                self.ganer_movies = self.ganer_movies.order_by('-point')
            elif ordering == 'release_year':
                self.ganer_movies = self.ganer_movies.order_by('-year_create')

        if imdb_point and imdb_point.isnumeric():
                self.ganer_movies = self.ganer_movies.filter(point__gte = imdb_point)

        self.context['media_ganer'] = get_page(self.ganer_movies, page, 21)
        return render(request, self.template_name, self.context)
