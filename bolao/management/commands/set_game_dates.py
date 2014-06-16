#!/usr/bin/env python
# -*- coding: utf-8 -*-

from bolao.models import Group, Team, Game, Bet
from django.core.management.base import BaseCommand, CommandError
from datetime import datetime

class Command(BaseCommand):
    help = 'Set up app db'

    def handle(self, *args, **options):

        game = Game.objects.get(id=1)
        game.start_date_time = datetime(year=2014, month=6, day=12, hour=17)
        game.save()
        game = Game.objects.get(id=2)
        game.start_date_time = datetime(year=2014, month=6, day=13, hour=13)
        game.save()
        game = Game.objects.get(id=17)
        game.start_date_time = datetime(year=2014, month=6, day=17, hour=16)
        game.save()
        game = Game.objects.get(id=18)
        game.start_date_time = datetime(year=2014, month=6, day=18, hour=19)
        game.save()
        game = Game.objects.get(id=33)
        game = Game.objects.get(id=34)

#        group = Group(name="B")

        game = Game.objects.get(id=3)
        game.start_date_time = datetime(year=2014, month=6, day=13, hour=16)
        game.save()
        game = Game.objects.get(id=4)
        game.start_date_time = datetime(year=2014, month=6, day=13, hour=19)
        game.save()
        game = Game.objects.get(id=19)
        game = Game.objects.get(id=20)
        game = Game.objects.get(id=35)
        game = Game.objects.get(id=36)


        #group = Group(name="C")

        game = Game.objects.get(id=5)
        game.start_date_time = datetime(year=2014, month=6, day=14, hour=13)
        game.save()
        game = Game.objects.get(id=6)
        game.start_date_time = datetime(year=2014, month=6, day=14, hour=22)
        game.save()
        game = Game.objects.get(id=21)
        game = Game.objects.get(id=22)
        game = Game.objects.get(id=37)
        game = Game.objects.get(id=38)


        #group = Group(name="D")

        game = Game.objects.get(id=7)
        game.start_date_time = datetime(year=2014, month=6, day=14, hour=16)
        game.save()
        game = Game.objects.get(id=8)
        game.start_date_time = datetime(year=2014, month=6, day=14, hour=19)
        game.save()
        game = Game.objects.get(id=23)
        game = Game.objects.get(id=24)
        game = Game.objects.get(id=39)
        game = Game.objects.get(id=40)


        #group = Group(name="E")
        game = Game.objects.get(id=9)
        game.start_date_time = datetime(year=2014, month=6, day=15, hour=13)
        game.save()
        game = Game.objects.get(id=10)
        game.start_date_time = datetime(year=2014, month=6, day=15, hour=16)
        game.save()
        game = Game.objects.get(id=25)
        game = Game.objects.get(id=26)
        game = Game.objects.get(id=41)
        game.start_date_time = datetime(year=2014, month=6, day=25, hour=17)
        game.save()
        game = Game.objects.get(id=42)


        #group = Group(name="F")
        game = Game.objects.get(id=11)
        game.start_date_time = datetime(year=2014, month=6, day=15, hour=19)
        game.save()
        game = Game.objects.get(id=12)
        game.start_date_time = datetime(year=2014, month=6, day=16, hour=16)
        game.save()
        game = Game.objects.get(id=27)
        game = Game.objects.get(id=28)
        game = Game.objects.get(id=43)
        game = Game.objects.get(id=44)


        #group = Group(name="G")
        game = Game.objects.get(id=13)
        game.start_date_time = datetime(year=2014, month=6, day=16, hour=13)
        game.save()
        game = Game.objects.get(id=14)
        game.start_date_time = datetime(year=2014, month=6, day=16, hour=19)
        game.save()
        game = Game.objects.get(id=29)
        game = Game.objects.get(id=30)
        game.start_date_time = datetime(year=2014, month=6, day=22, hour=19)
        game.save()
        game = Game.objects.get(id=45)
        game = Game.objects.get(id=46)


        #group = Group(name="H")
        game = Game.objects.get(id=15)
        game.start_date_time = datetime(year=2014, month=6, day=17, hour=13)
        game.save()
        game = Game.objects.get(id=16)
        game.start_date_time = datetime(year=2014, month=6, day=17, hour=19)
        game.save()
        game = Game.objects.get(id=31)
        game = Game.objects.get(id=32)
        game = Game.objects.get(id=47)
        game = Game.objects.get(id=48)

        game = Game.objects.get(id=49)
        game = Game.objects.get(id=50)
        game = Game.objects.get(id=51)
        game = Game.objects.get(id=52)
        game = Game.objects.get(id=53)
        game = Game.objects.get(id=54)
        game = Game.objects.get(id=55)
        game = Game.objects.get(id=56)
        game = Game.objects.get(id=57, stage=Game.QUARTER_FINALS).save()
        game = Game.objects.get(id=58, stage=Game.QUARTER_FINALS).save()
        game = Game.objects.get(id=59, stage=Game.QUARTER_FINALS).save()
        game = Game.objects.get(id=60, stage=Game.QUARTER_FINALS).save()
        game = Game.objects.get(id=61, stage=Game.SEMI_FINALS).save()
        game = Game.objects.get(id=62, stage=Game.SEMI_FINALS).save()
        game = Game.objects.get(id=63, stage=Game.FINALS).save()
        game = Game.objects.get(id=64, stage=Game.FINALS).save()

        print 'Done!'
