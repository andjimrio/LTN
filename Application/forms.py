#encoding:utf-8

from django import forms

class UserForm(forms.Form):
    idUsuario = forms.IntegerField(label="ID del usuario")