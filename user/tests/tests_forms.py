from django.test import TestCase
from user.forms import LoginForm


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