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
from django.conf.urls import url, include, handler400, handler403, handler404, handler500
from django.contrib.auth.views import login, logout
from django.core.urlresolvers import reverse_lazy
from django.contrib import admin

from Application import views
from Application.view import feed_views, item_views, profile_views, section_views

handler400 = 'Application.views.bad_request'
handler403 = 'Application.views.permission_denied'
handler404 = 'Application.views.page_not_found'
handler500 = 'Application.views.server_error'

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^i18n/', include('django.conf.urls.i18n')),
    url(r'^$', views.home, name='home'),

    # Profile
    url(r'^profile/view/', profile_views.profile_view, name='profile_view'),
    url(r'^profile/edit/', profile_views.profile_edit, name='profile_edit'),

    # Section
    url(r'^section/view/(?P<section_id>\d+)/', section_views.section_view, name='section_view'),
    url(r'^section/edit/(?P<section_id>\d+)/', section_views.section_edit, name='section_edit'),
    url(r'^section/delete/(?P<section_id>\d+)/', section_views.section_delete, name='section_delete'),

    # Feed
    url(r'^feed/view/(?P<feed_id>\d+)/', feed_views.feed_view, name='feed_view'),
    url(r'^feed/list/', feed_views.feed_list, name='feed_list'),
    url(r'^feed/create/', feed_views.feed_create, name='feed_create'),
    url(r'^feed/delete/(?P<section_id>\d+)/(?P<feed_id>\d+)/', feed_views.feed_delete, name='feed_delete'),

    # Item
    url(r'^item/list/', item_views.item_list, name='item_list'),
    url(r'^item/view/(?P<item_id>\d+)/', item_views.item_view, name='item_view'),
    url(r'^item/query/(?P<query>.+)/', item_views.item_query, name='item_query'),
    url(r'^item/recommend/', item_views.item_recommend, name='item_recommend'),
    url(r'^item/summary/', item_views.item_summary, name='item_summary'),
    url(r'^item/search/', item_views.item_search, name='item_search'),
    url(r'^item/saved/', item_views.item_saved, name='item_saved'),

    # User
    url(r'^register/', views.register, name='register'),
    url(r'^login/', login, {'template_name': 'login.html'}, name='login'),
    url(r'^logout/', logout, {'next_page': reverse_lazy('home')}, name='logout'),

    # Otras
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
