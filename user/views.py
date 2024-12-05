from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.views import View
from .forms import LoginForm, SignupForm, UpdateProfileForm, PhoneNumberForm
from django.db.models import F
import datetime
from django.utils import timezone
from .utils import get_left_special_time
from django.core.paginator import Paginator


# Auth imports
from django.contrib.auth import authenticate, login, logout
from .mixins import RedirectAuthenticatedUser
from django.contrib.auth.mixins import LoginRequiredMixin
from django.conf import settings

from .models import User, Pakage, Subscription


class LoginView(RedirectAuthenticatedUser, View):
    template_name = 'main/auth.html'
    context = {'page_name': 'ورود',
               'form': LoginForm()}

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, self.context)
    
    def post(self, request, *args, **kwargs):
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username = username, password = password)

            if user is not None:
                login(request, user)
                next_url = request.GET.get('next', None) # to prevent auto logout after login(next)
                return redirect(next_url if next_url and next_url != '/logout' else reverse('home'))
            else:
                self.context.update({'msg': 'کاربری با این مشخصات یافت نشد'})
        else:
            self.context.update({'msg': 'فرم کامل نشده', 'form': form})
        return render(request, self.template_name, self.context)


class SignupView(RedirectAuthenticatedUser, View):
    template_name = 'main/auth.html'
    context = {
        'page_name': 'ثبت نام',
        'form': SignupForm()
    }

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, self.context)

    def post(self, request, *args, **kwargs):
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            if settings.LOGIN_AFTER_SIGNUP:
                login(request, user)
                next_url = request.GET.get('next', None) # to prevent auto logout after login(next)
            return redirect(next_url if next_url and next_url != '/logout' else reverse('home'))
        else:
            self.context.update({'form': form})
        return render(request, self.template_name, self.context)


class ProfileView(LoginRequiredMixin, View):
    template_name = 'user/profile.html'

    def setup(self, request, *args, **kwargs):
        # LoginRequiredMixin dose not work with setup method
        super().setup(request, *args, **kwargs)
        if request.user.is_authenticated:
            self.context = {
                'user_form': UpdateProfileForm(instance=request.user),
                'phone_form': PhoneNumberForm(user=request.user),
                'page_name': 'profile',
                'title_page': 'آپدیت پروفایل | نت موی',
                'current_time': timezone.now(),
            'special_time': get_left_special_time(request.user)
            }
        else:
            return redirect(reverse('login'))

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, self.context)

    def post(self, request, *args, **kwargs):
        user_form = UpdateProfileForm(request.POST, instance=request.user)
        phone_form = PhoneNumberForm(request.POST, user=request.user)

        if user_form.is_valid():
            email = user_form.cleaned_data['email']
            if User.objects.filter(email = email).exclude(id=request.user.id).exists():
                user_form.add_error('email', 'ایمیل تکراری است')
            else:
                user_form.save()
        self.context['user_form'] = user_form

        if phone_form.has_changed():
            if phone_form.is_valid() and request.user.number is None:
                phone = phone_form.save()
                user = User.objects.get(pk=request.user.pk)
                user.number = phone
                user.save()
            self.context['phone_form'] = phone_form
        return render(request, self.template_name, self.context)


class ChangePasswordView(LoginRequiredMixin, View):
    template_name = 'user/change-password.html'
    def setup(self, request, *args, **kwargs):
        self.context = {
                'page_name': 'change password',
                'title_page': 'تغییر پسورد | نت موی',
                'current_time': timezone.now(),
                'special_time': get_left_special_time(request.user)
            }
        return super().setup(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, self.context)

    def post(self, request, *args, **kwargs):
        last_password = request.POST.get('last_password')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        user = authenticate(request, username = request.user.username, password = last_password)
        if user is not None:
            if password1 == password2:
                user.set_password(password1)
                user.save()
                return redirect(reverse('login'))
            else:
                self.context['msg'] = 'پسورد ها با هم یکی نیستند'
        else:
            self.context['msg'] = 'پسورد قبلی اشتباه است'
        return render(request, self.template_name, self.context)


class BuySubscriptionView(LoginRequiredMixin, View):
    template_name = 'user/buy-subscription.html'

    def get(self, request, *args, **kwargs):
        context = {
            'page_name': 'buy subscription',
            'title_page': 'خرید اشتراک | نت موی',
            'pakages': Pakage.objects.filter(is_active = True),
            'current_time': timezone.now(),
            'special_time': get_left_special_time(request.user)
        }
        pakage_id = request.GET.get('pakage', None)

        if pakage_id:
            pakage = get_object_or_404(Pakage, is_active = True, id=pakage_id)
            Subscription.objects.create(user = request.user, pakage = pakage, price = pakage.get_price(), days = pakage.dates)
            time = datetime.timedelta(days=pakage.dates)
            user = User.objects.get(id=request.user.id)
            if user.special_time:
                user.special_time = F('special_time') + time
            else:
                user.special_time = datetime.datetime.now() + time
            user.save()

            request.user.refresh_from_db()
            context.update({
                'msg': 'success',
                'daytes': pakage.dates,
                'special_time': get_left_special_time(request.user)
            })
        return render(request, self.template_name, context)


class HistorySubscriptionView(LoginRequiredMixin, View):
    template_name = 'user/history-subscription.html'

    def get(self, request, *args, **kwargs):
        p = Paginator(Subscription.objects.filter(user=request.user).order_by('actived_at'), 20)
        page = request.GET.get('page', 1)

        context = {
            'page_name': 'history subscription',
            'title_page': 'سابقه خرید | نت موی',
            'special_time': get_left_special_time(request.user),
            'page': p.page(page),
            'current_time': timezone.now(),
        }
        return render(request, self.template_name, context)


def logoutView(request):
    if request.user.is_authenticated:
        logout(request)
    return redirect(reverse('login'))

def home(request):
    return render(request, 'main/auth.html')
