from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View
from .forms import LoginForm, SignupForm

# Auth imports
from django.contrib.auth import authenticate, login, logout
from .mixins import RedirectAuthenticatedUser
from django.conf import settings


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


def logoutView(request):
    if request.user.is_authenticated:
        logout(request)
    return redirect(reverse('login'))

def home(request):
    return render(request, 'main/auth.html')
