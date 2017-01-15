#encoding:utf-8
# Create your views here.
from django.shortcuts import render_to_response
from django.template.context import RequestContext
from django.contrib.auth import authenticate,login as auth_login,logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse

from Application.rss import LINK_ABC,LINK_ELPAIS,LINK_ACEPRENSA
from Application.populate import populate_rss
from Application.queries import all_feeds,get_item
from Application.web import read_main_content
from Application.forms import UserForm,UserProfileForm
from Application.models import UserProfile,Feed

def home(request):
    return render_to_response('index.html',RequestContext(request))

def load(request):
    populate_rss(LINK_ELPAIS)
    populate_rss(LINK_ABC)
    populate_rss(LINK_ACEPRENSA)
    return render_to_response('index.html')

@login_required
def feeds(request):
    feedes = all_feeds()
    return render_to_response('feeds.html',RequestContext(request,{'feedes':feedes}))

def article(request, idItem=None):
    itemer = get_item(idItem)
    link = itemer.link
    web,image = read_main_content(link)
    return render_to_response('article.html',RequestContext(request,{'link':link,'title':itemer.title,'web':web,'image':image}))

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
            print user_form.errors, profile_form.errors

    else:
        user_form = UserForm()
        profile_form = UserProfileForm()

    return render_to_response('register.html',RequestContext(request, \
                {'user_form':user_form,'profile_form':profile_form,'registered':registered}))

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
            print "Los datos no son correctos: {0}, {1}".format(username,password)
            return HttpResponse("Los datos no son correctos")

    else:
        return render_to_response('login.html',RequestContext(request,{}))

    pass

@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect('/')