from django.test import TestCase
from django.urls import reverse
from user.models import PhoneNumber, User, Pakage, Subscription

from django.utils import timezone
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


class TestProfileUpdateView(TestCase):
    
    @classmethod
    def setUpTestData(cls):
        User.objects.create(username='usertest', email='usertest@test.test')
        user = User.objects.create(username='user1')
        PhoneNumber.objects.create(number='09123456780')
        user.set_password('pass')
        cls.user = user.save()
    
    def setUp(self):
        user_info = {
            'username': 'user1',
            'password': 'pass'
        }
        self.client.post(reverse('login'), user_info)

    def test_url(self):
        user_info = {
            'username': 'user1',
            'password': 'pass'
        }
        response = self.client.get(reverse('dashboard:profile'))
        self.assertEqual(response.status_code, 200)

    def test_template_used(self):
        response = self.client.get(reverse('dashboard:change-password'))
        self.assertTemplateUsed(response, 'user/change-password.html')

    def test_update_phone_success(self):
        data = {
            'number': '09123456789'
        }
        self.client.post(reverse('dashboard:profile'), data=data)
        response = self.client.get(reverse('dashboard:profile'))
        self.assertEqual(response.wsgi_request.user.number.number, '09123456789')
    
    def test_update_phone_not_access(self):
        """
        Number can be edited only once
        """

        data = { 'number': '09123456789' }
        data2 = { 'number': '09912345678'}
        self.client.post(reverse('dashboard:profile'), data=data)
        response = self.client.get(reverse('dashboard:profile'), data=data2)
        self.assertEqual(response.wsgi_request.user.number.number, '09123456789')

    def test_update_phone_errors(self):
        phone_less = { 'number': '9123456789' }
        phone_without_09 = { 'number': '08123456789' }

        response = self.client.post(reverse('dashboard:profile'), data=phone_less)
        self.assertContains(response, 'شماره تلفن اشتباه است')

        response = self.client.post(reverse('dashboard:profile'), data=phone_without_09)
        self.assertContains(response, 'شماره تلفن اشتباه است')

    def test_update_phone_error_unique(self):
        phone_number = { 'number': '09123456780' }
        response = self.client.post(reverse('dashboard:profile'), data=phone_number)
        self.assertContains(response, 'شماره تلفن قبلا استفاده شده')


    def test_update_email_success(self):
        data = {
            'username': 'user1',
            'email': 'test@test.test',
            'last_name': 'test',
            'first_name': 'user',
            'gender': 'male'
        }
        response = self.client.post(reverse('dashboard:profile'), data=data)
        self.assertEqual(response.wsgi_request.user.email, 'test@test.test')
    
    def test_update_email_error_unique(self):
        data ={
            'username': 'user1',
            'email': 'usertest@test.test',
            'last_name': 'test',
            'first_name': 'user',
            'gender': 'male'
        }
        response = self.client.post(reverse('dashboard:profile'), data=data)
        self.assertContains(response, 'ایمیل تکراری است')

    def test_update_gender(self):
        data ={
            'username': 'user1',
            'email': 'usertest@test.test',
            'last_name': 'test',
            'first_name': 'user',
            'gender': 'female'
        }
        response = self.client.post(reverse('dashboard:profile'), data=data)
        self.assertEqual(response.wsgi_request.user.gender, 'female')


class TestChangePasswordView(TestCase):
    def setUp(self):
        data = {
            'username': 'user1',
            'password': 'password'
        }
        user = User.objects.create(**data)
        user.set_password('password')
        user.save()
        self.client.post(reverse('login'), data = data)

    def test_url(self):
        response = self.client.get(reverse('dashboard:change-password'))
        self.assertEqual(response.status_code, 200)

    def test_template_used(self):
        response = self.client.get(reverse('dashboard:change-password'))
        self.assertTemplateUsed(response, 'user/change-password.html')

    def test_change_password_success(self):
        data = {
            'last_password': 'password',
            'password1': 'new_password',
            'password2': 'new_password',
        }
        data_login = {
            'username': 'user1',
            'password': 'new_password'
        }
        response1 = self.client.post(reverse('dashboard:change-password'), data = data)
        response2 = self.client.post(reverse('login'), data = data_login)
        self.assertEqual(response1.status_code, 302)
        self.assertEqual(response2.wsgi_request.user.username, 'user1')

    def test_redirect_after_change_password(self):
        data = {
            'last_password': 'password',
            'password1': 'new_password',
            'password2': 'new_password',
        }
        response = self.client.post(reverse('dashboard:change-password'), data = data)
        self.assertEqual(response.status_code, 302)
    
    def test_logout_after_change_password(self):
        data = {
            'last_password': 'password',
            'password1': 'new_password',
            'password2': 'new_password',
        }
        response = self.client.post(reverse('dashboard:change-password',), data = data, follow = True)
        self.assertFalse(response.wsgi_request.user.is_authenticated)

    def test_change_password_error_last_password(self):
        data = {
            'last_password': 'passwordw',
            'password1': 'new_password',
            'password2': 'new_password',
        }
        response = self.client.post(reverse('dashboard:change-password'), data = data)
        self.assertContains(response, 'پسورد قبلی اشتباه است')
    
    def test_change_password_error_password_not_match(self):
        data = {
            'last_password': 'password',
            'password1': 'new_password',
            'password2': 'new_pass',
        }
        response = self.client.post(reverse('dashboard:change-password'), data = data)
        self.assertContains(response, 'پسورد ها با هم یکی نیستند')


class TestBuySubscriptionView(TestCase):
    def setUp(self):
        data = {
            'username': 'user1',
            'password': 'password'
        }
        user = User.objects.create(**data)
        user.set_password(data['password'])
        user.save()
        pakages = [
            Pakage(
                title = "نقره",
                is_active = False,
                dates = 30,
                price = 250000
                ),
            Pakage(
                title = "طلا",
                is_active = True,
                dates = 30,
                price = 50000
                ),
            Pakage(
                title = "الماس",
                is_active = True,
                dates = 40,
                price = 30000
                )
        ]
        Pakage.objects.bulk_create(pakages)
        response = self.client.post(reverse('login'), data = data)

    def test_url(self):
        response = self.client.get(reverse('dashboard:buy-subscription'))

    def test_template_used(self):
        response = self.client.get(reverse('dashboard:buy-subscription'))
        self.assertTemplateUsed(response, 'user/buy-subscription.html')
        self.assertEqual(response.status_code, 200)

    def test_buy_subscription_success(self):
        response = self.client.get(reverse('dashboard:buy-subscription') + '?pakage=2')
        self.assertContains(response, 'خرید موفقیت امیز بود')

        diffrence = (response.wsgi_request.user.special_time - timezone.now()).days
        self.assertEqual(diffrence, 29)

    def test_buy_subscription_failed_not_found(self):
        response = self.client.get(reverse('dashboard:buy-subscription') + '?pakage=1')
        self.assertEqual(response.status_code, 404)


class TestHistorySubscriptionView(TestCase):
    def setUp(self):
        pakage = Pakage.objects.create(title = 'pakage1', description = 'test', price = 22, dates = 30)
        user = User.objects.create(username = 'user1')
        user.set_password('password')
        user.save()
        self.client.post(reverse('login'), data = {'username': 'user1', 'password': 'password'})
        subscriptions = []
        for i in range(0, 35):
            subscriptions.append(
                Subscription(
                    user = user,
                    pakage = pakage,
                    price = pakage.get_price(),
                    days = pakage.dates
                    )
                )
        Subscription.objects.bulk_create(subscriptions)

    def test_url(self):
        response = self.client.get(reverse('dashboard:history-subscription'))
        self.assertEqual(response.status_code, 200)

    def test_template_used(self):
        response = self.client.get(reverse('dashboard:history-subscription'))
        self.assertTemplateUsed(response, 'user/history-subscription.html')

    def test_item_per_page(self):
        response = self.client.get(reverse('dashboard:history-subscription'))
        self.assertEqual(len(response.context['page'].object_list), 20)
        self.assertEqual(response.context['page'].object_list[0].id, 1)


class TestTicketView(TestCase):

    def setUp(self):
        user = User.objects.create(username = 'user')
        user.set_password('password')
        user.save()
        self.client.post(reverse('login'), data={'username': 'user', 'password': 'password'})
    
    def test_url(self):
        response = self.client.get(reverse('dashboard:ticket'))
        self.assertEqual(response.status_code, 200)
    
    def test_template_used(self):
        response = self.client.get(reverse('dashboard:ticket'))
        self.assertTemplateUsed(response, 'user/tickets.html')
    
    def test_create_ticket_success(self):
        data = {
            'title': 'new ticket',
            'departeman': 'finance and sales',
            'message': 'this a test ticket',
        }
        response = self.client.post(reverse('dashboard:ticket'), data = data)
        self.assertEqual(response.context['tickets'].first().title, data['title'])

    def test_create_ticket_failed_invalid_departeman(self):
        data = {
            'title': 'new ticket',
            'departeman': 'fincanc test',
            'message': 'this a test ticket',
        }
        response = self.client.post(reverse('dashboard:ticket'), data = data)
        self.assertEqual(response.context['form'].errors['departeman'][0], 'لطفا گذینه درست رو انتخاب کنید.')
    
    def test_create_ticket_failed_required_title(self):
        data = {
            'departeman': 'fincanc test',
            'message': 'this a test ticket',
        }
        response = self.client.post(reverse('dashboard:ticket'), data = data)
        self.assertEqual(response.context['form'].errors['title'][0], 'این فیلد اجباری است.')

    def test_create_ticket_failed_required_departeman(self):
        data = {
            'title': 'test',
            'message': 'this a test ticket',
        }
        response = self.client.post(reverse('dashboard:ticket'), data = data)
        self.assertEqual(response.context['form'].errors['departeman'][0], 'این فیلد اجباری است.')

    def test_create_ticket_failed_required_message(self):
        data = {
            'departeman': 'fincanc test',
            'title': 'this a test ticket',
        }
        response = self.client.post(reverse('dashboard:ticket'), data = data)
        self.assertEqual(response.context['form'].errors['message'][0], 'این فیلد اجباری است.')

    def test_redirect_anonymoususer(self):
        self.client.get(reverse('logout'))
        response = self.client.get(reverse('dashboard:ticket'))
        self.assertEqual(response.status_code, 302)


class TestTicketDetailsView(TestCase):

    def setUp(self):
        user = User.objects.create(username = 'user')
        user.set_password('password')
        user.save()
        self.client.post(reverse('login'), data = {'username': 'user', 'password': 'password'})
        ticket_data = {
            'title': 'test',
            'departeman': 'finance and sales',
            'message': 'test'
        }
        self.client.post(reverse('dashboard:ticket'), data = ticket_data)
    
    def test_url(self):
        response = self.client.get(reverse('dashboard:ticket-details', args = [1]))
        self.assertEqual(response.status_code, 200)

    def test_template_used(self):
        response = self.client.get(reverse('dashboard:ticket-details', args=[1]))
        self.assertTemplateUsed(response, 'user/ticket-details.html')
    
    def test_send_message_success(self):
        response = self.client.post(reverse('dashboard:ticket-details', args=[1]), data = {'message': 'test2'})
        self.assertEqual(response.context['messages'].count(), 2)
        self.assertEqual(response.context['messages'].last().message, 'test2')

    def test_update_ticket_update_at_with_signal(self):
        response1 = self.client.get(reverse('dashboard:ticket-details', args=[1]))
        response2 = self.client.post(reverse('dashboard:ticket-details', args=[1]), data = {'message': 'tes2'})
        self.assertGreater(response2.context['ticket'].update_at, response1.context['ticket'].update_at)

    def test_send_message_failed_required_message(self):
        response = self.client.post(reverse('dashboard:ticket-details', args=[1]))
        self.assertContains(response, 'این فیلد اجباری است.')
    
    def test_404_notfound_ticket(self):
        response = self.client.get(reverse('dashboard:ticket-details', args=[2]))
        self.assertEqual(response.status_code, 404)

    def test_redirect_anonymoususer(self):
        self.client.get(reverse('logout'))
        response = self.client.get(reverse('dashboard:ticket-details', args=[1]))
        self.assertEqual(response.status_code, 302)
