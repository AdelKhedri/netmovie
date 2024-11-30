from django.shortcuts import render, redirect
from django.views import View
from .forms import LoginForm

# Auth imports
from django.contrib.auth import authenticate, login
from .mixins import RedirectAuthenticatedUser


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
                next = request.GET.get('next', None)
                return redirect(next if next else 'home')
            else:
                self.context.update({'msg': 'کاربری با این مشخصات یافت نشد'})
        else:
            self.context.update({'msg': 'فرم کامل نشده', 'form': form})
        return render(request, self.template_name, self.context)


def home(request):
    return render(request, 'main/auth.html')
