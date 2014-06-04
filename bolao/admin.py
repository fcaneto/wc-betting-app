#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.contrib import admin
from bolao.models import Game, BetRoom, Team, Group, Bet, Player
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

class PlayerInline(admin.StackedInline):
    model = Player
    can_delete = False
    verbose_name_plural = 'Bolão'

# Define a new User admin
class UserAdmin(UserAdmin):
    #exclude = ('groups', 'user_permissions')
    inlines = (PlayerInline, )
    list_display = ('username', 'email', 'first_name', 'last_name', 'player')

admin.site.unregister(User)
admin.site.register(User, UserAdmin)

admin.site.register(Team)
admin.site.register(Player)
admin.site.register(Group)
admin.site.register(Game)
admin.site.register(Bet)
admin.site.register(BetRoom)

