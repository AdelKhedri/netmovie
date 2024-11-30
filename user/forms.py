from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django import forms
from .models import User, PhoneNumber

# validate
from django.core.exceptions import ValidationError
from .validators import validate_phone_number, validate_username


input_attrs = {'class': 'input-bg-slate'}
checkbox_attrs = {'class': 'checkbox'}

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


class SignupForm(forms.ModelForm):
    """ 
    ## Sign up users without phone number
    phone number is unique but is not required

    """
    # phone_number = forms.CharField(label='شماره تلفن', validators=[validate_phone_number], widget=forms.NumberInput(attrs=input_attrs))
    username = forms.CharField(label='نام کاریری', validators=[validate_username], widget=forms.TextInput(attrs=input_attrs))
    password1 = forms.CharField(label='رمز', widget=forms.PasswordInput(attrs=input_attrs))
    password2 = forms.CharField(label='تکرار رمز', widget=forms.PasswordInput(attrs=input_attrs))
    accept_rules = forms.BooleanField(
                                    label='قوانین را می پذیرم',
                                    error_messages={'required': 'باید قوانین را بپذیرید'},
                                    widget=forms.CheckboxInput(attrs=checkbox_attrs))

    class Meta:
        model = User
        fields = ['username']
    
    def clean_password2(self):
        password1 = self.cleaned_data['password1']
        password2 = self.cleaned_data['password2']
        if password1 != password2:
            raise ValidationError('پسورد ها با هم یکی نیستند')
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password2'])
        user.save()
        return user
        # phone = self.cleaned_data['phone_number']
        # if phone:
        #     phone = PhoneNumber.objects.create(number=phone)
        #     user.number = phone
        # else:
        #     raise ValidationError('شماره تلفن باید وارد شود')
