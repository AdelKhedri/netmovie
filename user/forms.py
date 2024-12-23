from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django import forms
from .models import Request, User, PhoneNumber, Ticket, MessageSupport

# validate
from django.utils import timezone
from django.core.exceptions import ValidationError
from .validators import validate_phone_number, validate_username


input_attrs = {'class': 'input-bg-slate'}
checkbox_attrs = {'class': 'checkbox'}
radio_input = {'class': ''}
input_dark_attrs = {'class': 'input-dark'}
input_full_dark_attrs = {'class': 'input-full-dark simple-input'}

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


class TicketForm(forms.ModelForm):
    message = forms.CharField(widget=forms.Textarea(attrs=input_full_dark_attrs),
                              label='توضیحات',
                              error_messages = {
                                'required': 'این فیلد اجباری است.'
                            })

    class Meta:
        model = Ticket
        fields = ['title', 'departeman']

        widgets = {
            'title': forms.TextInput(attrs=input_full_dark_attrs),
        }

        error_messages = {
            'departeman': {
                'required': 'این فیلد اجباری است.',
                'invalid_choice': 'لطفا گذینه درست رو انتخاب کنید.'
            },
            'title': {
                'required': 'این فیلد اجباری است.'
            }
        }


    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

    def save(self, commit = True):
        obj = super().save(commit = False)
        obj.user = self.user
        if commit:
            obj.save()
        MessageSupport.objects.create(message = self.cleaned_data['message'], sender = self.user, ticket = obj)
        return obj


class MessageSupportForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        self.ticket = kwargs.pop('ticket', None)
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

    def save(self, commit = True):
        obj = super().save(commit = False)
        obj.ticket = self.ticket
        obj.sender = self.user
        if commit:
            obj.save()
        return obj

    class Meta:
        model = MessageSupport
        fields = ['message',]

        widgets = {
            'message': forms.Textarea(attrs=input_full_dark_attrs)
        }

        error_messages = {
            'message': {
                'required': 'این فیلد اجباری است.'
            }
        }


class RequestForm(forms.ModelForm):
    # the camera Invented in 1816
    year = forms.IntegerField(max_value=timezone.now().year,
                              min_value=1816,
                              widget=forms.NumberInput(attrs=input_full_dark_attrs),
                              error_messages = {
                                    'required': 'این فیلد اجباری است.',
                                    'max_value': 'سال انتشار نباید از امسال بیشتر باشد.',
                                    'min_value': 'سال انتشار نمیتواند قبل از اختراع دوربین باشد.',
                                    'invalid': 'سال انتشار باید عددی باشد.'
                                })
    
    class Meta:
        model = Request
        fields = ['name', 'year', 'request_type']

        widgets = {
            'name': forms.TextInput(attrs=input_full_dark_attrs),
            'request_type': forms.RadioSelect(),
        }

        error_messages = {
            'name': {
                'required': 'این فیلد اجباری است.'
            },
            'request_type': {
                'required': 'این فیلد اجباری است.',
                'invalid_choice': 'لطفا گذینه درست رو انتخاب کنید.'
            }
        }


    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

    def save(self, commit = True):
        obj = super().save(False)
        obj.user = self.user
        if commit:
            obj.save()
        return obj
