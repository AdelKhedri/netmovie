from django.test import TestCase
from django.urls import reverse
from user.models import User
from movieserial.models import (Movie, Serial, Ganers)
from netmovie.settings import BASE_DIR
from django.core.files.uploadedfile import SimpleUploadedFile


class TestHomeView(TestCase):
    
    def setUp(self):
        user = User.objects.create(username = 'user')
        user.set_password('password')
        user.save()
        self.client.post(reverse('login'), data = {'username': 'user', 'passowrd': 'password'})

        ganer_horror = Ganers.objects.create(name = 'ترسناک', slug = 'horror')
        ganer_action = Ganers.objects.create(name = 'اکشن', slug = 'action')
        ganers = [ganer_action, ganer_horror]

        media_data = {
            'name': 'movie1',
            'persian_name': 'فیلم1',
            'baner': '',
            'slug': 'movie1',
            'online_play': 'https://google.com/',
            'imdb_link': 'jttps://google.com/imdb',
            'year_create': 1386,
            'duration': '01:45:00',
            'release_date': '2024-08-06 12:05:55+00',
            'is_subtitle': True,
            'is_sound_translate': False,
            'point': 7.3,
        }

        for i in range(16):
            with open(BASE_DIR / 'movieserial/tests/img/test_baner_movie.png', 'rb') as f:
                file = SimpleUploadedFile(f'baner{i}.jpg', f.read(), content_type='image/png')
            media_data['baner'] = file
            media_data.update({'slug': f'{media_data["slug"]}{i}'})
            movie = Movie.objects.create(**media_data)
            movie.ganers.set(ganers)
            movie.save()

            serial = Serial.objects.create(**media_data)
            serial.ganers.set(ganers)
            serial.save()


    def test_url(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)

    def test_template_used(self):
        response = self.client.get(reverse('home'))
        self.assertTemplateUsed(response, 'movieserial/home.html')

    def test_movies_count(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.context['movies'].count(), 14)

    def test_serials_count(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.context['serials'].count(), 8)

    def test_serial_count_of_ganers(self):
        response = self.client.get(reverse('home'))
        # ganer 0
        self.assertEqual(response.context['serial_ganers'][0].count, 16)
        self.assertEqual(response.context['serial_ganers'][1].count, 16)

    def test_movie_count_of_ganers(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.context['serial_ganers'][0].count, 16)

    def tearDown(self):
        import os
        baners = [f'baner{i}.jpg' for i in range(16)]
        for i in baners:
            os.remove(BASE_DIR / f'media/images/movies/baner/{i}')
            os.remove(BASE_DIR / f'media/images/serials/baner/{i}')
        return super().tearDown()