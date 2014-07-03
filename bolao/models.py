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

    changed_timestamp = models.DateTimeField(default=datetime.datetime.now, verbose_name=u'Última modificação')
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
    is_open_to_betting = models.BooleanField(default=True, verbose_name="Apostas abertas?")

    def __unicode__(self):
        return self.name


class Player(models.Model):
    user = models.OneToOneField(User)
    bet_room = models.ForeignKey(BetRoom)

    rival = models.ForeignKey('Player', null=True)
    rival_correlation = models.CharField(max_length=10, null=True)

    def __unicode__(self):
        return '%s @ %s' % (self.user.first_name, self.bet_room)


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
                                  related_query_name='home_game', null=True, blank=True, default=None)
    away_team = models.ForeignKey(Team, related_name='away_games',
                                  related_query_name='away_game', null=True, blank=True, default=None)

    #stadium = models.ForeignKey('Stadium', null=True)
    start_date_time = models.DateTimeField(null=True, blank=True, verbose_name=u'Data e hora de início')

    def get_start_date_time(self):
        date_time = self.start_date_time
        if date_time:
            return "%s/%s às %s:%s" % (date_time.day, date_time.month, date_time.hour, date_time.minute)
        else:
            return 'None'

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

    home_goals_normal_time = models.IntegerField(default=0, verbose_name=u'Placar mandante (tempo normal)')
    away_goals_normal_time = models.IntegerField(default=0, verbose_name=u'Placar visitante (tempo normal)')

    home_goals_extra_time = models.IntegerField(null=True, default=0)
    away_goals_extra_time = models.IntegerField(null=True, default=0)
    had_extra_time = models.BooleanField(default=False)

    home_goals_penalties = models.IntegerField(null=True, default=0)
    away_goals_penalties = models.IntegerField(null=True, default=0)

    winner = models.ForeignKey(Team, null=True, blank=True, verbose_name=u'Vencedor (empate em tempo normal)')

    def __unicode__(self):
        return "[%s] %s X %s - %s - %s" % (self.id, self.home_team, self.away_team, self.status, self.start_date_time)

    def is_a_tie(self):
        return self.home_goals_normal_time == self.away_goals_normal_time

    def get_winner(self):
        if self.is_a_tie():
            return self.winner
        else:
            return self.home_team if self.home_goals_normal_time > self.away_goals_normal_time else self.away_team

    def get_loser(self):
        return self.home_team if self.get_winner() == self.away_team else self.away_team

    def is_home_team_winner(self):
        return self.home_team == self.get_winner()

    def is_away_team_winner(self):
        return self.away_team == self.get_winner()

    def has_started(self):
        return self.status != Game.STATUS_NOT_STARTED

    def save(self, update_ts=True, *args, **kwargs):
        from django.core.cache import cache
        for bet in self.bet_set:
            cache.delete('score_%s' % bet.id)

        super(Game, self).save(*args, **kwargs)

    @staticmethod
    def get_current_games():
        happening = Game.objects.filter(status=Game.STATUS_HAPPENING).order_by('start_date_time')
        if happening:
            return happening
        not_started_games = Game.objects.filter(status=Game.STATUS_NOT_STARTED).exclude(start_date_time__isnull=True).order_by('start_date_time')
        next_games = []
        next_date_time = None
        for game in not_started_games:
            if next_date_time is None:
                next_date_time = game.start_date_time
            if game.start_date_time == next_date_time:
                next_games.append(game)
            else:
                break
        return next_games

    @staticmethod
    def get_round_of_16_games():
        return Game.objects.filter(id__range=(49, 56)).order_by('id')

    @staticmethod
    def get_quarter_finals_games():
        return Game.objects.filter(id__range=(57, 60)).order_by('id')

    @staticmethod
    def get_semi_finals_games():
        return Game.objects.filter(id__range=(61, 62)).order_by('id')

    @staticmethod
    def get_finals_games():
        return Game.objects.filter(id__range=(63, 64)).order_by('id')

    #@staticmethod
    #def get_last_game():
    #    """
    #    Current match being played or the last that finished
    #    """
    #    last_games = Game.objects.filter(status=Game.STATUS_NOT_STARTED).order_by('start_date_time')
    #    if last_games:
    #        return not_started_games[0]
    #    else:
    #        return None


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
            return '[%s] %s %s X %s %s > %s' % (self.game_id, self.home_team,
                                              self.home_score, self.away_score,
                                              self.away_team, self.winner)
        else:
            return '[%s] %s %s X %s %s' % (self.game_id, self.game.home_team,
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

    def is_home_team_winner(self):
        return self.home_team == self.get_winner()

    def is_away_team_winner(self):
        return self.away_team == self.get_winner()

    def teams_got_right(self):
        teams = 0
        if self.home_team_id == self.game.home_team_id or self.home_team_id == self.game.away_team_id:
            teams += 1
        if self.away_team_id == self.game.away_team_id or self.away_team_id == self.game.home_team_id:
            teams += 1
        return teams

    @staticmethod
    def query_all_bets(player):
        return Bet.objects.filter(player=player).select_related('game')

    @staticmethod
    def get_by_match_id(player, match_id):
        return Bet.objects.get(player=player, game__id=match_id)
