#encoding:utf-8

from django import forms
from django.contrib.auth.models import User
from django.contrib.auth import authenticate

class UserForm(forms.ModelForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class' : 'validate'}))
    password = forms.CharField(widget=forms.PasswordInput())
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class' : 'validate'}))

    class Meta:
        model = User
        fields = ('username','password','email')

    pass

class UserProfileForm(forms.Form):
    urls = forms.CharField(widget=forms.Textarea(attrs={'class' : 'materialize-textarea'}))

    pass