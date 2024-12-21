from django import forms
from .models import MovieComment, SerialComment, Ganers
from user.forms import input_full_dark_attrs, checkbox_attrs


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


# class GanerFilterForm(forms.Form):
#     imdb_point_types = (
#         ("3", "بیشتر از 3"),
#         ("4", "بیشتر از 4"),
#         ("5", "بیشتر از 5"),
#         ("6", "بیشتر از 6"),
#         ("7", "بیشتر از 7"),
#         ("8", "بیشتر از 8"),
#         ("9", "بیشتر از 9"),
#         ("all", "همه"),
#     )
#     order_types = (
#         ("newest", "جدیدترین"),
#         ("most_recent", "بروزترین"),
#         ("popular", "محبوب ترین"),
#         ("imdb_point", "امتیاز IMDB"),
#         ("release_year", "سال انتشار"),
#     )
#     ganer = forms.ModelChoiceField(queryset=Ganers.objects.all(), required=False)
#     imdb_point = forms.ChoiceField(widget=forms.Select(choices=imdb_point_types), required=False)
#     ordering = forms.ChoiceField(widget=forms.Select(choices=order_types), required=False)
