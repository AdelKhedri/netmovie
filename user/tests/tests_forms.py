from django.test import TestCase
from user.forms import LoginForm, SignupForm, PhoneNumberForm, UpdateProfileForm, TicketForm, MessageSupportForm, RequestForm
from user.models import Ticket, User, PhoneNumber
from django.urls import reverse
from django.utils import timezone


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


class TestMessageSupportForm(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create(username = 'user')
        cls.user.set_password('password')
        cls.user.save()
        cls.ticket = Ticket.objects.create(title = 'test', departeman = 'finance and sales', user = cls.user)

    def test_valid_form(self):
        form = MessageSupportForm(data = {'message': 'test'})
        self.assertTrue(form.is_valid())

    def test_invalid_form_required_message(self):
        form = MessageSupportForm(data = {}, user = self.user, ticket = self.ticket)
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['message'][0], 'این فیلد اجباری است.')

    def test_save_message(self):
        ticket_data = {
            'title': 'test',
            'departeman': 'finance and sales',
            'message': 'test' 
        }
        message_data = {
            'message': 'test2'
        }
        form1 = TicketForm(data = ticket_data, user = self.user)
        ticket = form1.save()
        form2 = MessageSupportForm(data = message_data, user = self.user, ticket = ticket)
        form2.save()
        self.client.post(reverse('login'), data = {'username': 'user', 'password': 'password'})
        response = self.client.get(reverse('dashboard:ticket-details', args=[ticket.id]))
        self.assertEqual(response.context['messages'].last().message, 'test2')


class TestRequestForm(TestCase):

    def test_valid_form(self):
        data = {
            'name': 'test',
            'year': 2020,
            'request_type': 'serial'
        }
        form = RequestForm(data = data)
        self.assertTrue(form.is_valid())

    def test_invalid_form_required_name(self):
        data = {
            'year': 2020,
            'request_type': 'serial'
        }
        form = RequestForm(data = data)
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['name'][0], 'این فیلد اجباری است.')

    def test_invalid_form_required_request_type(self):
        data = {
            'year': 2020,
            'name': 'test',
        }
        form = RequestForm(data = data)
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['request_type'][0], 'این فیلد اجباری است.')

    def test_invalid_form_invalid_choice_request_type(self):
        data = {
            'year': 2020,
            'request_type': 'sesadwawdwrial',
            'name': 'test',
        }
        form = RequestForm(data = data)
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['request_type'][0], 'لطفا گذینه درست رو انتخاب کنید.')

    def test_invalid_form_required_year(self):
        data = {
            'request_type': 'movie',
            'name': 'test',
        }
        form = RequestForm(data = data)
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['year'][0], 'این فیلد اجباری است.')

    def test_invalid_form_max_year(self):
        data = {
            'year': timezone.now().year + 1,
            'request_type': 'movie',
            'name': 'test',
        }
        form = RequestForm(data = data)
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['year'][0], 'سال انتشار نباید از امسال بیشتر باشد.')

    def test_invalid_form_max_year(self):
        data = {
            'year': 1815,
            'request_type': 'movie',
            'name': 'test',
        }
        form = RequestForm(data = data)
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['year'][0], 'سال انتشار نمیتواند قبل از اختراع دوربین باشد.')

    def test_invalid_form_max_year(self):
        data = {
            'year': 'ss',
            'request_type': 'movie',
            'name': 'test',
        }
        form = RequestForm(data = data)
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['year'][0], 'سال انتشار باید عددی باشد.')

    def test_save_request_with_current_user(self):
        data = {
            'year': 2022,
            'request_type': 'movie',
            'name': 'test',
        }
        user = User.objects.create(username = 'user')
        user.set_password('password')
        user.save()
        self.client.post(reverse('dashboard:request'), data = {'username': 'user', 'password': 'password'})
        form = RequestForm(data = data, user = user)
        self.assertTrue(form.is_valid())
        request = form.save()
        self.assertIsInstance(request.user, User)
        self.assertEqual(request.user, user)