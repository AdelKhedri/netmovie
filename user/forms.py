from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django import forms
from .models import User, PhoneNumber

# validate
from django.core.exceptions import ValidationError
from .validators import validate_phone_number, validate_username


input_attrs = {'class': 'input-bg-slate'}
checkbox_attrs = {'class': 'checkbox'}
radio_input = {'class': ''}
input_dark_attrs = {'class': 'input-dark'}

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


class PhoneNumberForm(forms.ModelForm):
    number = forms.CharField(validators=[validate_phone_number], required=False, widget=forms.NumberInput(attrs=input_dark_attrs))

    class Meta:
        model = PhoneNumber
        fields = ['number']

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user and user.number:
            self.fields['number'].disabled = True
            self.fields['number'].initial = user.number.number


class UpdateProfileForm(forms.ModelForm):
    username = forms.CharField(disabled=True, widget=forms.TextInput(attrs=input_dark_attrs))
    email = forms.CharField(required=False, widget=forms.EmailInput(attrs=input_dark_attrs))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if len(self.instance.email) > 0:
            self.fields['email'].disabled = True
            self.fields['email'].initial = self.instance.email

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'gender']

        widgets = {
            'first_name': forms.TextInput(attrs=input_dark_attrs),
            'last_name': forms.TextInput(attrs=input_dark_attrs),
            'gender': forms.RadioSelect(attrs=radio_input)
        }