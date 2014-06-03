#!/usr/bin/env python
# -*- coding: utf-8 -*-

from bolao.models import Group, Team, Game
from django.core.management.base import BaseCommand, CommandError


class Command(BaseCommand):
    help = 'Set up app db'

    def handle(self, *args, **options):
        print 'Deleting everybody'
        Game.objects.all().delete()
        Team.objects.all().delete()
        Group.objects.all().delete()

        print 'Adding stuff again'
        group = Group(name="A")
        group.save()
        team0 = Team(name='Brasil', code='bra')
        team0.save()
        team1 = Team(name='Croácia', code='cro')
        team1.save()
        team2 = Team(name='México', code='mex')
        team2.save()
        team3 = Team(name='Camarões', code='cam')
        team3.save()

        Game(id=1, home_team=team0, away_team=team1).save()
        Game(id=2, home_team=team2, away_team=team3).save()
        Game(id=17, home_team=team0, away_team=team2).save()
        Game(id=18, home_team=team3, away_team=team1).save()
        Game(id=33, home_team=team3, away_team=team0).save()
        Game(id=34, home_team=team1, away_team=team2).save()

        group = Group(name="B")
        group.save()
        team0 = Team(group=group,  name='Espanha', code='esp')
        team0.save()
        team1 = Team(group=group,  name='Holanda', code='hol')
        team1.save()
        team2 = Team(group=group,  name='Chile', code='chi')
        team2.save()
        team3 = Team(group=group,  name='Austrália', code='aus')
        team3.save()

        Game(id=3, home_team=team0, away_team=team1).save()
        Game(id=4, home_team=team2, away_team=team3).save()
        Game(id=19, home_team=team0, away_team=team2).save()
        Game(id=20, home_team=team3, away_team=team1).save()
        Game(id=35, home_team=team3, away_team=team0).save()
        Game(id=36, home_team=team1, away_team=team2).save()


        group = Group(name="C")
        group.save()
        team0 = Team(group=group,  name='Colômbia', code='col')
        team0.save()
        team1 = Team(group=group,  name='Grécia', code='gre')
        team1.save()
        team2 = Team(group=group,  name='Costa do Marfim', code='cdm')
        team2.save()
        team3 = Team(group=group,  name='Japão', code='jap')
        team3.save()

        Game(id=5, home_team=team0, away_team=team1).save()
        Game(id=6, home_team=team2, away_team=team3).save()
        Game(id=21, home_team=team0, away_team=team2).save()
        Game(id=22, home_team=team3, away_team=team1).save()
        Game(id=37, home_team=team3, away_team=team0).save()
        Game(id=38, home_team=team1, away_team=team2).save()


        group = Group(name="D")
        group.save()
        team0 = Team(group=group,  name='Uruguai', code='uru')
        team0.save()
        team1 = Team(group=group,  name='Costa Rica', code='cos')
        team1.save()
        team2 = Team(group=group,  name='Inglaterra', code='ing')
        team2.save()
        team3 = Team(group=group,  name='Itália', code='ita')
        team3.save()

        Game(id=7, home_team=team0, away_team=team1).save()
        Game(id=8, home_team=team2, away_team=team3).save()
        Game(id=23, home_team=team0, away_team=team2).save()
        Game(id=24, home_team=team3, away_team=team1).save()
        Game(id=39, home_team=team3, away_team=team0).save()
        Game(id=40, home_team=team1, away_team=team2).save()


        group = Group(name="E")
        group.save()
        team0 = Team(group=group,  name='Suíça', code='sui')
        team0.save()
        team1 = Team(group=group,  name='Equador', code='equ')
        team1.save()
        team2 = Team(group=group,  name='França', code='fra')
        team2.save()
        team3 = Team(group=group,  name='Honduras', code='hon')
        team3.save()

        Game(id=9, home_team=team0, away_team=team1).save()
        Game(id=10, home_team=team2, away_team=team3).save()
        Game(id=25, home_team=team0, away_team=team2).save()
        Game(id=26, home_team=team3, away_team=team1).save()
        Game(id=41, home_team=team3, away_team=team0).save()
        Game(id=42, home_team=team1, away_team=team2).save()


        group = Group(name="F")
        group.save()
        team0 = Team(group=group,  name='Argentina', code='arg')
        team0.save()
        team1 = Team(group=group,  name='Bósnia', code='bos')
        team1.save()
        team2 = Team(group=group,  name='Irã', code='ira')
        team2.save()
        team3 = Team(group=group,  name='Nigéria', code='nga')
        team3.save()

        Game(id=11, home_team=team0, away_team=team1).save()
        Game(id=12, home_team=team2, away_team=team3).save()
        Game(id=27, home_team=team0, away_team=team2).save()
        Game(id=28, home_team=team3, away_team=team1).save()
        Game(id=43, home_team=team3, away_team=team0).save()
        Game(id=44, home_team=team1, away_team=team2).save()


        group = Group(name="G")
        group.save()
        team0 = Team(group=group,  name='Alemanha', code='ale')
        team0.save()
        team1 = Team(group=group,  name='Portugal', code='por')
        team1.save()
        team2 = Team(group=group,  name='Gana', code='gan')
        team2.save()
        team3 = Team(group=group,  name='EUA', code='eua')
        team3.save()

        Game(id=13, home_team=team0, away_team=team1).save()
        Game(id=14, home_team=team2, away_team=team3).save()
        Game(id=29, home_team=team0, away_team=team2).save()
        Game(id=30, home_team=team3, away_team=team1).save()
        Game(id=45, home_team=team3, away_team=team0).save()
        Game(id=46, home_team=team1, away_team=team2).save()


        group = Group(name="H")
        group.save()
        team0 = Team(group=group,  name='Bélgica', code='bel')
        team0.save()
        team1 = Team(group=group,  name='Argélia', code='agl')
        team1.save()
        team2 = Team(group=group,  name='Rússia', code='rus')
        team2.save()
        team3 = Team(group=group,  name='Coréia do Sul', code='cor')
        team3.save()

        Game(id=15, home_team=team0, away_team=team1).save()
        Game(id=16, home_team=team2, away_team=team3).save()
        Game(id=31, home_team=team0, away_team=team2).save()
        Game(id=32, home_team=team3, away_team=team1).save()
        Game(id=47, home_team=team3, away_team=team0).save()
        Game(id=48, home_team=team1, away_team=team2).save()

        Game(id=49, stage=Game.ROUND_OF_16).save()
        Game(id=50, stage=Game.ROUND_OF_16).save()
        Game(id=51, stage=Game.ROUND_OF_16).save()
        Game(id=52, stage=Game.ROUND_OF_16).save()
        Game(id=53, stage=Game.ROUND_OF_16).save()
        Game(id=54, stage=Game.ROUND_OF_16).save()
        Game(id=55, stage=Game.ROUND_OF_16).save()
        Game(id=56, stage=Game.ROUND_OF_16).save()
        Game(id=57, stage=Game.QUARTER_FINALS).save()
        Game(id=58, stage=Game.QUARTER_FINALS).save()
        Game(id=59, stage=Game.QUARTER_FINALS).save()
        Game(id=60, stage=Game.QUARTER_FINALS).save()
        Game(id=61, stage=Game.SEMI_FINALS).save()
        Game(id=62, stage=Game.SEMI_FINALS).save()
        Game(id=63, stage=Game.FINALS).save()
        Game(id=64, stage=Game.FINALS).save()

        print 'Done!'
