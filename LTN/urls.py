from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', 'Application.views.home'),
    url(r'^load/', 'Application.views.load'),
    url(r'^feeds/', 'Application.views.feeds'),
    url(r'^article/(?P<idItem>\w+)/', 'Application.views.article'),

    # Examples:
    # url(r'^$', 'LTN.views.home', name='home'),
    # url(r'^LTN/', include('LTN.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)
