#!/usr/bin/env python
# -*- coding: utf-8 -*-

from bolao.models import Group, Team, Game, Bet
from django.core.management.base import BaseCommand, CommandError


class Command(BaseCommand):
    help = 'Set up app db'

    def handle(self, *args, **options):
        print 'Deleting everybody'
        Game.objects.all().delete()
        Team.objects.all().delete()
        Group.objects.all().delete()
        Bet.objects.all().delete()

        print 'Done!'
