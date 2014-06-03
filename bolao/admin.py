#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.contrib import admin
from django.contrib.admin.filters import SimpleListFilter
from bolao.models import Game

class GameModelAdmin(admin.ModelAdmin):
    list_display = ('pk', 'home_team', 'away_team')


