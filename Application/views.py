#encoding:utf-8
# Create your view here.
from django.shortcuts import render

from Application.forms import UserForm,UserProfileForm
from Application.models import UserProfile,Feed
from Application.utilities.populate_utilities import populate_rss


def home(request):
    return render(request,'index.html',{})

def register(request):
    registered = False

    if request.method == 'POST':
        user_form = UserForm(request.POST)
        profile_form = UserProfileForm(request.POST)

        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()

            profile = UserProfile()
            profile.user = user
            profile.save()
            for url in profile_form.data['urls'].split('\r\n'):
                ide = populate_rss(url)
                profile.feeds.add(Feed.objects.get(id=ide))

            registered = True

        else:
            print(user_form.errors, profile_form.errors)

    else:
        user_form = UserForm()
        profile_form = UserProfileForm()

    return render(request, 'register.html',{'user_form':user_form,'profile_form':profile_form,'registered':registered})
