from django.conf.urls import patterns, include, url
from django.contrib import admin
from bolao.admin import UserAdmin
from django.contrib.auth.models import User

admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'bolao.views.home', name='home'),
    url(r'^login/$', 'bolao.views.login', name='login'),
    url(r'^signup/$', 'bolao.views.signup', name='signup'),
    url(r'^logout/$', 'bolao.views.logout', name='logout'),
    url(r'^bet/$', 'bolao.views.bet', name='bet'),
    url(r'^sim/$', 'bolao.views.simulator', name='sim'),
    url(r'^rules/$', 'bolao.views.rules', name='rules'),
    url(r'^player/$', 'bolao.views.player', name='player'),
    url(r'^ranking/$', 'bolao.views.ranking', name='ranking'),
    url(r'^admin/', include(admin.site.urls)),
)


