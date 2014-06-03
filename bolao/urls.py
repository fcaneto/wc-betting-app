from django.conf.urls import patterns, include, url

from django.contrib import admin

from bolao.models import Team, Group, Game, Stadium, Bet
from bolao.admin import GameModelAdmin

admin.autodiscover()
admin.site.register(Team)
admin.site.register(Group)
admin.site.register(Game)
admin.site.register(Stadium)
admin.site.register(Bet)

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'bolao.views.home', name='home'),
    url(r'^login/$', 'bolao.views.login', name='login'),
    url(r'^logout/$', 'bolao.views.logout', name='logout'),
    url(r'^bet/$', 'bolao.views.bet', name='bet'),
    url(r'^ranking/$', 'bolao.views.ranking', name='ranking'),
    url(r'^admin/', include(admin.site.urls)),
)
