from django.conf.urls import patterns, include, url
# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

from app.views import logout_view, login_view, register, home, newsnip, newstory


urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'app.views.login', name='login'),
    url(r'^home/$', home),
    url(r'^logout/$', logout_view),
    url(r'^newsnip/$', newsnip),
    url(r'^newstory/$', newstory),
    url(r'^register/$', 'app.views.register', name='reg'),
    url(r'^$', login_view),
    # url(r'^inlupp/', include('inlupp.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)
