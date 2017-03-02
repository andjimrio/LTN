#encoding:utf-8
# Create your views here.
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect

from Application.rss import LINK_ABC,LINK_ELPAIS,LINK_ACEPRENSA
from Application.populate import populate_rss
from Application.queries import get_feeds_by_user,get_item
from Application.web import get_article
from Application.forms import UserForm,UserProfileForm
from Application.models import UserProfile,Feed
from Application.index_utilities import identity,keywords

def home(request):
    return render(request,'index.html',{})

def load(request):
    populate_rss(LINK_ELPAIS)
    populate_rss(LINK_ABC)
    populate_rss(LINK_ACEPRENSA)
    return HttpResponseRedirect('/')

@login_required
def feeds(request):
    feedes = get_feeds_by_user(request.user.id)
    return render(request,'feeds.html',{'feedes':feedes})

def article(request, idItem=None):
    article = get_item(idItem)
    tags = keywords(idItem)
    news = [get_item(new) for new in identity(idItem)]
    return render(request,'article.html',{'article':article,'tags':tags,'news':news})

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
