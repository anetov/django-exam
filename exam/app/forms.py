from .models import Profile, Post, Comment
from django.contrib.auth.models import User
from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm


class SignUpForm(UserCreationForm):
    password1 = forms.CharField(max_length=15, required=True, widget = forms.PasswordInput(attrs={"class": "w-100 py-3 px-6 rounded-2"}))
    password2 = forms.CharField(max_length=15, required=True, widget = forms.PasswordInput(attrs={"class": "w-100 py-3 px-6 rounded-2"}))
    
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

class UserLoginForm(AuthenticationForm):
    username = forms.CharField(max_length=25, required=True, widget=forms.TextInput(attrs={"class": "w-100 py-3 px-6 rounded-2"}))
    password = forms.CharField(max_length=25, required=True, widget=forms.PasswordInput(attrs={"class": "w-100 py-3 px-6 rounded-2"}))

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('title', 'content', 'image')
        widgets = {
            'created_at': forms.DateTimeInput(attrs={'type': 'datetime-local'}, format='%Y-%m-%dT%H:%M'),
        }

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('content',)