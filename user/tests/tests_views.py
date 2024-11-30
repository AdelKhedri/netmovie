from django.test import TestCase
from django.urls import reverse
from user.models import User

from django.conf import settings


class TestLoginView(TestCase):
    def setUp(self):
        user = User.objects.create(username='usertest1', password='passwordtest')
        user.set_password('passwordtest')
        user.save()
    
    def test_url(self):
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)
    
    def test_template_used(self):
        response = self.client.get(reverse('login'))
        self.assertTemplateUsed(response, 'main/auth.html')
    
    def test_login_successful(self):
        response = self.client.post(reverse('login'), {
            'username': 'usertest1',
            'password': 'passwordtest'
        })
        self.assertTrue(response.wsgi_request.user.is_authenticated)
        self.assertRedirects(response, reverse('home'))
    
    def test_login_failed(self):
        response = self.client.post(reverse('login'), {
            'username': 'usertest2',
            'password': 'passwords'
        })
        self.assertContains(response, 'کاربری با این مشخصات یافت نشد')
        self.assertFalse(response.wsgi_request.user.is_authenticated)
    
    def test_login_failed_invalid_form(self):
        response = self.client.post(reverse('login'), {
            'username': 'usertest2'
        })
        self.assertContains(response, 'فرم کامل نشده')
        self.assertFalse(response.wsgi_request.user.is_authenticated)

    def test_login_address_in_settings(self):
        response = self.client.get(settings.LOGIN_URL)
        self.assertEqual(response.status_code, 200)

    def test_redirect_authenticated_user(self):
        self.client.post(reverse('login'), {
            'username': 'usertest1',
            'password': 'passwordtest'
        })
        response = self.client.get(reverse('login'))
        response_post = self.client.post(reverse('login'),{})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response_post.status_code, 302)
