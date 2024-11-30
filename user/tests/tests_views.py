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


class TestSignupView(TestCase):

    def setUp(self):
        user = User.objects.create(username = 'user1')
        user.set_password('password')
        user.save()
    
    def test_url(self):
        response = self.client.get(reverse('signup'))
        self.assertEqual(response.status_code, 200)
    
    def test_template_used(self):
        response = self.client.get(reverse('signup'))
        self.assertTemplateUsed(response, 'main/auth.html')

    def test_signup_successful(self):
        data = {
            'username': 'user2',
            'password1': 'password',
            'password2': 'password',
            'accept_rules': True
        }
        response = self.client.post(reverse('signup'), data=data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('home'))
        self.assertTrue(response.wsgi_request.user.is_authenticated)

    def test_signup_failed(self):
        data = {
            'username': 'user1',
            'password1': 'password',
            'password2': 'password2',
            'accept_rules': False
        }
        response = self.client.post(reverse('signup'), data=data)
        self.assertContains(response, 'نام کاربری تکراری است')
        self.assertContains(response, 'باید قوانین را بپذیرید')
        self.assertContains(response, 'پسورد ها با هم یکی نیستند')

    def test_redirect_authenticated_user(self):
        res = self.client.post(reverse('login'), {'username': 'user1', 'password': 'password'})
        response = self.client.get(reverse('signup'))
        self.assertEqual(response.status_code, 302)

class TestLogoutView(TestCase):
    def setUp(self):
        user = User.objects.create(username = 'user1', password = 'password')
        user.set_password('password')
        user.save()

    def test_logout(self):
        self.client.post(reverse('login'), {'username': 'user1', 'password': 'password'})
        response = self.client.get(reverse('logout'))
        response2 = self.client.get(reverse('logout'))
        self.assertTrue(response.wsgi_request.user.is_anonymous)
        self.assertRedirects(response2, reverse('login'))