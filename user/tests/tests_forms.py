from django.test import TestCase
from user.forms import LoginForm, SignupForm
from user.models import User, PhoneNumber


class TestLoginForm(TestCase):
    
    def test_form_valid(self):
        form = LoginForm(
            {
                'username': 'test',
                'password': 'passowrd'
            }
        )
        self.assertTrue(form.is_valid())
    
    def test_form_invalid_username(self):
        form = LoginForm({
            'password': 'test'
        })
        self.assertFalse(form.is_valid())

    def test_form_invalid_password(self):
        form = LoginForm({
            'username': 'test'
        })
        self.assertFalse(form.is_valid())


class TestSignupForm(TestCase):
    def setUp(self):
        phone = PhoneNumber.objects.create(number='09123456789')
        User.objects.create(username = 'user1', password = 'password', number = phone)
    
    def test_valid_data(self):
        form = SignupForm({
            'username': 'user2',
            'password1': 'password',
            'password2': 'password',
            'accept_rules': True
        })
        self.assertTrue(form.is_valid())
    
    def test_invalid_data(self):
        form = SignupForm({
            'username': 'user1',
            'password1': 'password',
            'password2': 'passwordnew',
            'accept_rules': False
        })
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['username'][0], 'نام کاربری تکراری است')
        self.assertEqual(form.errors['accept_rules'][0], 'باید قوانین را بپذیرید')
        self.assertIn('password2', form.errors)
        self.assertEqual(form.errors['password2'][0], 'پسورد ها با هم یکی نیستند')
