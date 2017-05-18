from django import forms
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _

from Application.service.feed_services import get_feeds_by_user


class UserForm(forms.ModelForm):
    username = forms.CharField(label=_("username"), widget=forms.TextInput(attrs={'class': 'validate'}))
    email = forms.EmailField(label=_("email"), widget=forms.EmailInput(attrs={'class': 'validate'}))
    password = forms.CharField(label=_("password"), widget=forms.PasswordInput())
    repassword = forms.CharField(label=_("repassword"), widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username', 'email', 'password')


class FeedForm(forms.Form):
    url = forms.URLField(label=_("link"), widget=forms.URLInput(attrs={'class': 'validate autocomplete'}))
    section = forms.CharField(label=_("section"), widget=forms.TextInput(attrs={'class': 'validate'}))


class ItemSearchForm(forms.Form):
    title = forms.CharField(label=_("title"), required=False, widget=forms.TextInput(attrs={'class': 'validate'}))
    creator = forms.CharField(label=_("creator"), required=False, widget=forms.TextInput(attrs={'class': 'validate'}))
    description = forms.CharField(label=_("description"), required=False,
                                  widget=forms.TextInput(attrs={'class': 'validate'}))
    feed = forms.ModelChoiceField(label=_("newspaper"), required=False, queryset=None)

    def __init__(self, user, *args, **kwargs):
        super(ItemSearchForm, self).__init__(*args, **kwargs)

        self.fields['feed'].queryset = get_feeds_by_user(user)
