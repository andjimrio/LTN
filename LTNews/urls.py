"""LTNews URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from Application.views import home,feeds,feed,article,register,profile
from django.contrib.auth.views import login,logout
from django.core.urlresolvers import reverse_lazy
from django.conf import settings
from django.conf.urls.static import static
import haystack.urls

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', home, name='home'),

    url(r'^feeds/', feeds, name='feeds'),
    url(r'^feed/(?P<idFeed>\w+)/', feed, name='feed'),
    url(r'^article/(?P<idItem>\w+)/', article, name='article'),

    url(r'^register/', register, name='register'),
    url(r'^profile/', profile, name='profile'),
    url(r'^login/', login, {'template_name':'login.html'}, name='login'),
    url(r'^logout/', logout, {'next_page': reverse_lazy('home')}, name='logout'),

    url(r'^search/', include('haystack.urls')),
]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
