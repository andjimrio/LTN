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
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import url, include
from django.contrib.auth.views import login,logout
from django.core.urlresolvers import reverse_lazy
from django.contrib import admin

from Application import views
from Application.view import feed_view
from Application.view import item_view
import haystack.urls

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', views.home, name='home'),

    url(r'^feeds/', item_view.item_list, name='feeds'),
    url(r'^article/(?P<idItem>\w+)/', item_view.item_view, name='article'),

    url(r'^feed/(?P<idFeed>\w+)/', feed_view.feed_view, name='feed'),
    url(r'^profile/', feed_view.feed_list, name='profile'),

    url(r'^register/', views.register, name='register'),
    url(r'^login/', login, {'template_name':'login.html'}, name='login'),
    url(r'^logout/', logout, {'next_page': reverse_lazy('home')}, name='logout'),

    url(r'^search/', include('haystack.urls')),
]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
