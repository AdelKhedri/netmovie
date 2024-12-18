from django.shortcuts import render, get_object_or_404
from .models import Ganers, Movie, Serial
from django.views.generic import View
from user.utils import get_left_special_time
from django.db.models import Count

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
