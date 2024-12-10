from django.test import TestCase
from user.forms import LoginForm, SignupForm, PhoneNumberForm, UpdateProfileForm, TicketForm
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

class TestPhoneNumberForm(TestCase):

    def setUp(self):
        phone = PhoneNumber.objects.create(number = '09123456789')
        user = User.objects.create(username='user1')
        user.number = phone
        user.save()

    def test_first_update(self):
        data = {
            'phone': '0912345678'
        }
        phone_form = PhoneNumberForm(data = data)
        self.assertTrue(phone_form.is_valid())
    
    def test_second_update_not_allowed(self):
        user = User.objects.get(id=1)
        form = PhoneNumberForm(user = user)
        self.assertTrue(form.fields['number'].disabled)


class TestUpdateProfileForm(TestCase):

    def setUp(self):
        self.user = User.objects.create(username = 'user1')
    
    def test_first_update_email(self):
        data = {
            'username': 'user1',
            'email': 'user@gmail.com',
            'gender': 'male'
        }
        form = UpdateProfileForm(instance = self.user, data=data)
        self.assertTrue(form.is_valid())
        self.assertFalse(form.fields['email'].disabled)
    
    def test_second_update_email_not_allowed(self):
        self.user.email = 'user@gmail.com'
        self.user.save()
        
        data = {
            'username': 'user1',
            'email': 'user@gmail.com',
            'gender': 'male'
        }
        form = UpdateProfileForm(instance = self.user, data = data)
        self.assertTrue(form.fields['email'].disabled)
    
    def test_update_username_not_allowed(self):
        data = {
            'username': 'user1',
            'email': 'user@gmail.com',
            'gender': 'male'
        }
        form = UpdateProfileForm(instance = self.user, data = data)
        self.assertTrue(form.fields['username'].disabled)


class TestTicketForm(TestCase):

    def test_valid_data(self):
        data = {
            'title': 'new ticket',
            'departeman': 'finance and sales',
            'message': 'this a test ticket',
        }
        form = TicketForm(data = data)
        self.assertTrue(form.is_valid())
    
    def test_invalid_data_required_title(self):
        data = {
            'departeman': 'finance and sales',
            'message': 'this a test ticket',
        }
        form = TicketForm(data = data)
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['title'][0], 'این فیلد اجباری است.')

    def test_invalid_data_required_description(self):
        data = {
            'title': 'new ticket',
            'message': 'this a test ticket',
        }
        form = TicketForm(data = data)
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['departeman'][0], 'این فیلد اجباری است.')

    def test_invalid_data_required_message(self):
        data = {
            'title': 'new ticket',
            'departeman': 'finance and sales',
        }
        form = TicketForm(data = data)
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['message'][0], 'این فیلد اجباری است.')

    def test_invalid_data_departeman_invalid_choice(self):
        data = {
            'title': 'new ticket',
            'departeman': 'test',
            'message': 'this a test ticket',
        }
        form = TicketForm(data = data)
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['departeman'][0], 'لطفا گذینه درست رو انتخاب کنید.')