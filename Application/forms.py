#encoding:utf-8

from django import forms
from Application.models import UserProfile
from django.contrib.auth.models import User

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username','email','password')

    pass

class UserProfileForm(forms.Form):
    urls = forms.CharField(widget=forms.Textarea)

    pass