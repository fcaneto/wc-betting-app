#!/usr/bin/env python
# -*- coding: utf-8 -*-

import datetime

from django.db import models
from django.contrib.auth.models import User

'''-------------------------------------------------------------------------------------------
---------- Util Models ---------------------------------------------------------------------
--------------------------------------------------------------------------------------------'''

''' Superclasses for Models that stores timestamp for all changes. '''


class TimestampedModel(models.Model):
    class Meta:
        abstract = True

    changed_timestamp = models.DateTimeField(default=datetime.datetime.now, verbose_name=u'Horário')
    deleted = models.BooleanField(verbose_name=u'Apagado', default=False)

    def save(self, update_ts=True, *args, **kwargs):
        '''So atualiza o timestamp se for na criacao do objeto'''
        if update_ts:
            self.changed_timestamp = datetime.datetime.now()
        else:
            if self.changed_timestamp == 0:
                self.changed_timestamp = datetime.datetime.now()

        super(TimestampedModel, self).save(*args, **kwargs)


'''-------------------------------------------------------------------------------------------
---------- APP Models --------------------------------------------------------------------
--------------------------------------------------------------------------------------------'''


class Group(models.Model):
    name = models.CharField(max_length=1, default="")
    #teams = models.ManyToManyField('Team', through='GroupTeamRelationship')

    def __unicode__(self):
        return self.name

#
#class GroupTeamRelationship(models.Model):
#    team = models.ForeignKey('Team')
#    group = models.ForeignKey('Group')
#    order = models.IntegerField(default=0)

class Team(models.Model):
    name = models.CharField(max_length=50, default="")
    code = models.CharField(max_length=4, default="XXX")
    group = models.ForeignKey(Group, null=True)

    def __unicode__(self):
        return self.code


class Stadium(models.Model):
    name = models.CharField(max_length=50, default="")
    city = models.CharField(max_length=20, default="")

    def __unicode__(self):
        return self.city


class Game(TimestampedModel):
    home_team = models.ForeignKey(Team, related_name='home_games',
                                  related_query_name='home_game', null=True, default=None)
    away_team = models.ForeignKey(Team, related_name='away_games',
                                  related_query_name='away_game', null=True, default=None)

    #stadium = models.ForeignKey('Stadium', null=True)
    #date_time = models.DateTimeField(null=True, blank=True)

    STATUS_NOT_STARTED = 'NS'
    STATUS_HAPPENING = 'H'
    STATUS_FINISHED = 'F'
    STATUS_CHOICES = (
        (STATUS_NOT_STARTED, 'Not Started'),
        (STATUS_HAPPENING, 'Happening'),
        (STATUS_FINISHED, 'Finished')
    )
    status = models.CharField(max_length=2, choices=STATUS_CHOICES, default=STATUS_NOT_STARTED)

    GROUP = 'G'
    ROUND_OF_16 = '16'
    QUARTER_FINALS = 'Q'
    SEMI_FINALS = 'S'
    FINALS = 'F'
    STAGE_CHOICES = (
        (GROUP, 'Grupos'),
        (ROUND_OF_16, 'Oitavas'),
        (QUARTER_FINALS, 'Quartas'),
        (SEMI_FINALS, 'Semi'),
        (FINALS, 'Final'),
    )
    stage = models.CharField(max_length=2, choices=STAGE_CHOICES, default=GROUP)

    home_goals_normal_time = models.IntegerField(default=0)
    away_goals_normal_time = models.IntegerField(default=0)

    home_goals_extra_time = models.IntegerField(null=True, default=0)
    away_goals_extra_time = models.IntegerField(null=True, default=0)
    had_extra_time = models.BooleanField(default=False)

    home_goals_penalties = models.IntegerField(null=True, default=0)
    away_goals_penalties = models.IntegerField(null=True, default=0)

    def __unicode__(self):
        return "%s X %s" % (self.home_team, self.away_team)


class Bet(TimestampedModel):
    player = models.ForeignKey(User)
    game = models.ForeignKey('Game')
    home_score = models.IntegerField(default=0)
    away_score = models.IntegerField(default=0)

    home_team = models.ForeignKey(Team, related_name='home_bets',
                                  related_query_name='home_bet', null=True, default=None)
    away_team = models.ForeignKey(Team, related_name='away_bets',
                                  related_query_name='away_bet', null=True, default=None)

    winner = models.ForeignKey(Team, null=True)

    def __str__(self):
        if self.winner:
            return '[%s] %s %s X %s %s > %s' % (self.game.id, self.home_team,
                                              self.home_score, self.away_score,
                                              self.away_team, self.winner)
        else:
            return '[%s] %s %s X %s %s' % (self.game.id, self.game.home_team,
                                           self.home_score, self.away_score,
                                           self.game.away_team)
