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

class BetRoom(models.Model):
    name = models.CharField(max_length=30, default="")

    def __unicode__(self):
        return self.name


class Player(models.Model):
    user = models.OneToOneField(User)
    bet_room = models.ForeignKey(BetRoom)

    def __unicode__(self):
        return '%s' % self.bet_room


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

    winner = models.ForeignKey(Team, null=True, blank=True)

    def __unicode__(self):
        return "[%s] %s X %s" % (self.id, self.home_team, self.away_team)

    def is_a_tie(self):
        return self.home_goals_normal_time == self.away_goals_normal_time

    def get_winner(self):
        if self.is_a_tie():
            return self.winner
        else:
            return self.home_team if self.home_goals_normal_time > self.away_goals_normal_time else self.away_team

    def get_loser(self):
        return self.home_team if self.get_winner() == self.away_team else self.away_team

    def has_started(self):
        return self.status != Game.STATUS_NOT_STARTED

class Bet(TimestampedModel):
    betRoom = models.ForeignKey(BetRoom, null=True)
    player = models.ForeignKey(Player)
    game = models.ForeignKey(Game)
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

    def is_a_tie(self):
        return self.home_score == self.away_score

    def get_winner(self):
        if self.is_a_tie():
            return self.winner
        else:
            return self.home_team if self.home_score > self.away_score else self.away_team

    def get_loser(self):
        return self.home_team if self.get_winner() == self.away_team else self.away_team

    @staticmethod
    def query_all_bets(player):
        return Bet.objects.filter(player=player)

    @staticmethod
    def get_by_match_id(player, match_id):
        return Bet.objects.get(player=player, game__id=match_id)
