#encoding:utf-8

from django import forms
from django.contrib.auth.models import User
from django.contrib.auth import authenticate

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username','email','password')

    pass

class UserProfileForm(forms.Form):
    urls = forms.CharField(widget=forms.Textarea)

    pass

class LoginForm(forms.Form):
    username = forms.CharField(max_length=255, required=True)
    password = forms.CharField(widget=forms.PasswordInput, required=True)

    def login(self, request):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        user = authenticate(username=username, password=password)
        return user