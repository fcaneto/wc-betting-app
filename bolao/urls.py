from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf import settings

admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'bolao.views.home', name='home'),
    url(r'^login/$', 'bolao.views.login', name='login'),
    url(r'^password/$', 'bolao.views.change_password', name='change_password'),
    url(r'^logout/$', 'bolao.views.logout', name='logout'),
    url(r'^bet/$', 'bolao.views.bet', name='bet'),
    url(r'^bet/user/(?P<user_id>[0-9]+)/$', 'bolao.views.bet_from_user', name='bet_from_user'),
    url(r'^sim/$', 'bolao.views.simulator', name='sim'),
    url(r'^rules/$', 'bolao.views.rules', name='rules'),
    url(r'^player/$', 'bolao.views.player', name='player'),
    url(r'^games/$', 'bolao.views.games', name='games'),
    url(r'^ranking/$', 'bolao.views.ranking', name='ranking'),
    url(r'^rivals/$', 'bolao.views.rivals', name='rivals'),
    url(r'^admin/', include(admin.site.urls)),
)

#if settings.DEBUG:
#    import debug_toolbar
#    urlpatterns += patterns('',
#        url(r'^__debug__/', include(debug_toolbar.urls)),
#    )


