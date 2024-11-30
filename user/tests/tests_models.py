from django.test import TestCase
from user.models import User, Manager
from django.contrib.auth import get_user_model


class TestUserManager(TestCase):

    def test_create_user(self):
        user = get_user_model().objects.create_user(username='user1', email=None, password='test')
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_superuser)
        self.assertFalse(user.is_staff)

        with self.assertRaises(TypeError):
            User.objects.create_user()

    def test_create_superuser(self):
        user = User.objects.create_superuser(username='user2', email=None, password='esasa')
        self.assertEqual(user.username, 'user2')
        self.assertTrue(user.is_active)
        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)
