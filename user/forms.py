from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django import forms
from .models import User
from django.core.exceptions import ValidationError


input_attrs = {'class': 'input-bg-slate'}

class UserCreationForm(forms.ModelForm):
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = '__all__'
    
    def clean_password2(self):
        password1 = self.cleaned_data['password1']
        password2 = self.cleaned_data['password2']
        if password1 != password2:
            raise ValidationError('Passwords dont match')
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password2'])
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField()

    
    class Meta:
        model = User
        exclude = ['last_login']


class LoginForm(forms.Form):
    error_class = 'text-red-500'
    username = forms.CharField(max_length=150 ,label="نام کاربری" , widget=forms.TextInput(attrs=input_attrs))
    password = forms.CharField(max_length=150 ,label="پسورد" , widget=forms.PasswordInput(attrs=input_attrs))
