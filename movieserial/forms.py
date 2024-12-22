from django import forms
from .models import MovieComment, SerialComment, ContactUs
from user.forms import input_full_dark_attrs, checkbox_attrs


input_full_zinc = {'class': 'input-full-dark simple-input bg-zinc-900'}
class BaseCommentFrom(forms.ModelForm):
    class Meta:
        fields = ['text', 'parent_comment', 'is_spoil']

        widgets = {
            'text': forms.Textarea(attrs=input_full_dark_attrs),
            'parent_comment': forms.NumberInput(attrs=input_full_dark_attrs),
            'is_spoil': forms.CheckboxInput(attrs=checkbox_attrs),
        }

        error_messages = {
            'text': {
                'required': 'این فیلد اجباری است',
            }
        }
    

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)


    def save(self, commit = True):
        obj = super().save(commit = False)
        obj.user = self.user
        if hasattr(self, 'serial'):
            obj.serial = self.serial
            print(f'ss{self.cleaned_data["parent_comment"]}')
            try:
                comment = SerialComment.object.get(id = self.cleaned_data['parent_comment'])
                print(comment)
                obj.parent_comment = comment
            except:
                pass
        elif hasattr(self, 'movie'):
            obj.movie = self.movie
            try:
                comment = MovieComment.object.get(id = self.cleaned_data['parent_comment'])
                obj.parent_comment = comment
            except:
                pass
        if commit:
            obj.save()
        return obj


class SerialCommentForm(BaseCommentFrom):
    class Meta(BaseCommentFrom.Meta):
        model = SerialComment


    def __init__(self, *args, **kwargs):
        self.serial = kwargs.pop('serial', None)
        super().__init__(*args, **kwargs)


class MovieCommentForm(BaseCommentFrom):
    class Meta(BaseCommentFrom.Meta):
        model = MovieComment


    def __init__(self, *args, **kwargs):
        self.movie = kwargs.pop('movie', None)
        super().__init__(*args, **kwargs)


class ContactUsForm(forms.ModelForm):
    class Meta:
        model = ContactUs
        fields = "__all__"
    
        widgets = {
            'name' : forms.TextInput(attrs=input_full_zinc),
            'phone': forms.NumberInput(attrs=input_full_zinc),
            'email': forms.EmailInput(attrs=input_full_zinc),
            'subject': forms.TextInput(attrs=input_full_zinc),
            'message': forms.Textarea(attrs=input_full_zinc)
        }
