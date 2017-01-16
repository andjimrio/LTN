#encoding:utf-8
# Create your views here.
from django.shortcuts import render
from django.contrib.auth import authenticate,login as auth_login,logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse

from Application.rss import LINK_ABC,LINK_ELPAIS,LINK_ACEPRENSA
from Application.populate import populate_rss
from Application.queries import get_feeds_by_user,get_item
from Application.web import get_article
from Application.forms import UserForm,UserProfileForm
from Application.models import UserProfile,Feed

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
    link = get_item(idItem).link
    article = get_article(link)
    return render(request,'article.html',{'article':article})

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
            for url in profile_form.data['urls'].split('\n'):
                ide = populate_rss(url)
                profile.feeds.add(Feed.objects.get(id=ide))

            registered = True

        else:
            print(user_form.errors, profile_form.errors)

    else:
        user_form = UserForm()
        profile_form = UserProfileForm()

    return render(request, 'register.html',{'user_form':user_form,'profile_form':profile_form,'registered':registered})

def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)

        if user:
            if user.is_active:
                auth_login(request, user)
                return HttpResponseRedirect('/feeds/')

            else:
                return HttpResponse("Tu cuenta no está activa")

        else:
            print("Los datos no son correctos: {0}, {1}".format(username,password))
            return HttpResponse("Los datos no son correctos")

    else:
        return render(request,'login.html',{})

    pass

@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect('/')