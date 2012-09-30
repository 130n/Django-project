# Leon Hennings 880827-0154
from django.conf.urls import patterns, include, url
from django.contrib import admin
admin.autodiscover()
from app.views import logout_view, login_view, register, home, newstory, story, friends, profile

urlpatterns = patterns('',
    # url(r'^$', 'app.views.login', name='login'),
    url(r'story/(?P<storyID>\d+)/$', story),
    url(r'home/(?P<next>\d+)/$', home),
    url(r'^home/$', home),
    url(r'^logout/$', logout_view),
    url(r'^friends/$', friends),
    url(r'^profile/(?P<userID>\d+)/$', profile),
    url(r'^newstory/$', newstory),
    url(r'^register/$', 'app.views.register', name='reg'),
    url(r'^$', login_view),
    url(r'^admin/', include(admin.site.urls)),
)
