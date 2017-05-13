from django import forms
from django.contrib.auth.models import User

from Application.utilities.queries_utilities import get_feeds_by_user


class UserForm(forms.ModelForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'validate'}))
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username', 'password', 'email')

    pass


class FeedForm(forms.Form):
    url = forms.URLField(widget=forms.URLInput(attrs={'class': 'validate autocomplete'}))
    section = forms.CharField(widget=forms.TextInput(attrs={'class': 'validate'}))

    pass


class ItemSearchForm(forms.Form):
    title = forms.CharField(label="Título", required=False, widget=forms.TextInput(attrs={'class': 'validate'}))
    creator = forms.CharField(label="Autor", required=False, widget=forms.TextInput(attrs={'class': 'validate'}))
    description = forms.CharField(label="Descripción", required=False, widget=forms.TextInput(attrs={'class': 'validate'}))
    feed = forms.ModelChoiceField(label="Periódico", required=False, queryset=None)

    def __init__(self, user, *args, **kwargs):
        super(ItemSearchForm, self).__init__(*args, **kwargs)

        self.fields['feed'].queryset = get_feeds_by_user(user)

    pass
