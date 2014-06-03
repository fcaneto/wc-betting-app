#!/usr/bin/env python
# -*- coding: utf-8 -*-

import random
from bolao.models import Group, Team, Game
from django.core.management.base import BaseCommand, CommandError


class Command(BaseCommand):
    help = 'Set up app db'

    def handle(self, *args, **options):
        print 'Simulating cup'

        teams = Team.objects.all()

        for i in xrange(1, 65):
            game = Game.objects.get(id=i)
            score = random.randint(0, 4)
            game.home_goals_normal_time = score
            score = random.randint(0, 4)
            game.away_goals_normal_time = score

            if game.id >= 49:
                team = random.randint(0, len(teams) - 1)
                game.home_team = teams[team]
                team = random.randint(0, len(teams) - 1)
                game.away_team = teams[team]

                if game.home_goals_normal_time == game.away_goals_normal_time:
                    team = random.randint(0,1)
                    if team:
                        game.winner = game.home_team
                    else:
                        game.winner = game.away_team

            game.save()

            print 'Game [%s] = %s x %s' % (i, game.home_goals_normal_time, game.away_goals_normal_time)

        print 'Done!'
