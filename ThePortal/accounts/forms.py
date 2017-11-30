from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import FeedBack, Post, MyComments


Roles = [
    ('students', 'Student'),
    ('teachers', 'Teacher'),
    {'parents', 'Parent'},
]


class RegisterationForm(UserCreationForm):
    email = forms.EmailField(required = True)
    MyRole = forms.CharField(label='Your role in portal :', widget=forms.Select(choices=Roles))

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2', 'MyRole')

    def save(self, commit=True):
        user = super(RegisterationForm, self).save(commit=False)
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.email = self.cleaned_data['email']

        if commit:
            user.save()

        return user


class EditProfile(UserChangeForm):

    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name', 'password')


class GetFeedBack(forms.ModelForm):
    topic = forms.CharField()
    feed = forms.CharField()

    class Meta:
        model = FeedBack
        fields = ['topic', 'feed']


class MakePost(forms.ModelForm):

    class Meta:
        model = Post
        fields = ['post', ]


class CommentsForm(forms.ModelForm):

    class Meta:
        model = MyComments
        fields = ['comment', ]


