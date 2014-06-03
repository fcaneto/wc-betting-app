##!/usr/bin/env python
## -*- coding: utf-8 -*-
#import datetime
#from bolao.models import Team, Group, GroupTeamRelationship, Game
#
#Game.objects.all().delete()
#GroupTeamRelationship.objects.all().delete()
#Group.objects.all().delete()
#Team.objects.all().delete()
#
#
#with open('cup.txt') as f:
#    line = f.readline()
#    group_id = 'A'
#    team_1 = Team.objects.create(name='Brasil', code='BRA')
#    team_2 = Team.objects.create(name=u'Croácia', code='CRO')
#    team_3 = Team.objects.create(name=u'México', code='MEX')
#    team_4 = Team.objects.create(name=u'Camarões', code='CAM')
#    teams = [team_1, team_2, team_3, team_4]
#    group = Group.objects.create(name=group_id)
#    for i, team_name in enumerate(teams):
#        team = Team.objects.create(name=team_name)
#        GroupTeamRelationship.objects.create(group=group, team=team, order=i)
#
#
#
#    (1) Thu Jun/12 17:00 Brazil - Croatia @ Arena de São Paulo, São Paulo (UTC-3)
#(2) Fri Jun/13 13:00 Mexico - Cameroon @ Estádio das Dunas, Natal (UTC-3)
#
#(17) Tue Jun/17 16:00 Brazil - Mexico @ Estádio Castelão, Fortaleza (UTC-3)
#(18) Wed Jun/18 18:00 Cameroon - Croatia @ Arena Amazônia, Manaus (UTC-4)
#
#(33) Mon Jun/23 17:00 Cameroon - Brazil @ Brasília (UTC-3)
#(34) Mon Jun/23 17:00 Croatia - Mexico @ Recife (UTC-3)
#
#    'Spain', 'Netherlands', 'Chile', 'Australia'
#
#    #_, _, _, team1, team2, team3, team4 = line.split()
#    ## group B
#    #Team(name=team1).save()
#    #Team(name=team2).save()
#    #Team(name=team3).save()
#    #Team(name=team4).save()
#    #
#    #_, _, _, team1, team2, team3, team4 = line.split()
#    ## group C
#    #Team(name=team1).save()
#    #Team(name=team2).save()
#    #Team(name=team3).save()
#    #Team(name=team4).save()
#    #
#    #_, _, _, team1, team2, team3, team4 = line.split()
#    ## group D
#    #Team(name=team1).save()
#    #Team(name=team2).save()
#    #Team(name=team3).save()
#    #Team(name=team4).save()
#    #
#    #_, _, _, team1, team2, team3, team4 = line.split()
#    ## group E
#    #Team(name=team1).save()
#    #Team(name=team2).save()
#    #Team(name=team3).save()
#    #Team(name=team4).save()
#    #
#    #_, _, _, team1, team2, team3, team4 = line.split()
#    ## group F
#    #Team(name=team1).save()
#    #Team(name=team2).save()
#    #Team(name=team3).save()
#    #Team(name=team4).save()
#    #
#    #_, _, _, team1, team2, team3, team4 = line.split()
#    ## group G
#    #Team(name=team1).save()
#    #Team(name=team2).save()
#    #Team(name=team3).save()
#    #Team(name=team4).save()
#    #
#    #_, _, _, team1, team2, team3, team4 = line.split()
#    ## group H
#    #Team(name=team1).save()
#    #Team(name=team2).save()
#    #Team(name=team3).save()
#    #Team(name=team4).save()
#
#
