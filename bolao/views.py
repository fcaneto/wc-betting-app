#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json

from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib.auth import login as login_at_server
from django.contrib.auth import logout as logout_at_server
from django.http import HttpResponseRedirect, HttpResponse
from django.template.context import RequestContext
from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required

from django.views.decorators.csrf import csrf_exempt

from bolao.models import Game, Bet, Team


@login_required(login_url='login')
def home(request):
    print request.user
    return render_to_response('bolao.html', {}, RequestContext(request))


def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username=username, password=password)

        if user:
            if user.is_active:
                print 'User active'
                login_at_server(request, user)
                return HttpResponseRedirect('/')
            else:
                return HttpResponse("Conta desabilitada.")
        else:
            print "Invalid login details: {0}, {1}".format(username, password)
            return HttpResponse("Login falhou.")

    else:
        return render_to_response('login.html', {}, RequestContext(request))


@login_required
def logout(request):
    logout_at_server(request)
    return HttpResponseRedirect('/')


@login_required
def ranking(request):
    scores = []
    for player in User.objects.all():
        scores.append(Score(player))

    sorted(scores, key=lambda score: score.total_score)
    return render_to_response('ranking.html',
                              {'scores': scores,
                               'me': request.user},
                              RequestContext(request))


@login_required(login_url='login')
def bet(request):
    if request.method == 'POST':

        print request.user.first_name
        bets = json.loads(request.body)

        Bet.objects.filter(player=request.user).delete()

        for bet_dict in bets:
            id = bet_dict['id']
            home_score = int(bet_dict['homeScore'])
            away_score = int(bet_dict['awayScore'])

            home_team = None
            away_team = None
            winner = None
            try:
                code = bet_dict['homeTeamCode']
                home_team = Team.objects.get(code=code)
                code = bet_dict['awayTeamCode']
                away_team = Team.objects.get(code=code)
                code = bet_dict['winnerCode']
                winner = Team.objects.get(code=code)
            except KeyError:
                print 'Not a second round match'

            game = Game.objects.get(pk=id)

            bet = Bet(
                player=request.user,
                game=game,
                home_score=home_score,
                away_score=away_score,
                home_team=home_team,
                away_team=away_team,
                winner=winner)
            bet.save()

        return HttpResponse()

    else:
        # HTTP GET
        score = Score(request.user)

        group_bets = []
        round_16_bets = []
        quarter_bets = []
        semi_bets = []
        third_place = None
        final = None

        if Bet.objects.filter(player=request.user).exists():
            group_bets = Bet.objects.all().filter(player=request.user).filter(game__stage=Game.GROUP).order_by('game__id')
            round_16_bets = Bet.objects.all().filter(player=request.user).filter(game__stage=Game.ROUND_OF_16).order_by(
                'game__id')
            quarter_bets = Bet.objects.all().filter(player=request.user).filter(game__stage=Game.QUARTER_FINALS).order_by(
                'game__id')
            semi_bets = Bet.objects.all().filter(player=request.user).filter(game__stage=Game.SEMI_FINALS).order_by(
                'game__id')
            third_place = Bet.objects.get(game__id=63)
            final = Bet.objects.get(game__id=64)

            # Adicionando estes atributo a cada bet para facilitar template
            for bet in group_bets:
                bet.player_score = score.get_bet_score(bet.game.id)
            for bet in round_16_bets:
                bet.player_score = score.get_bet_score(bet.game.id)
            for bet in quarter_bets:
                bet.player_score = score.get_bet_score(bet.game.id)
            for bet in semi_bets:
                bet.player_score = score.get_bet_score(bet.game.id)
            third_place.player_score = score.get_bet_score(third_place.game.id)
            final.player_score = score.get_bet_score(final.game.id)

        return render_to_response('player.html',
                                  {'group_bets': group_bets,
                                   'round_16_bets': round_16_bets,
                                   'quarter_bets': quarter_bets,
                                   'semi_bets': semi_bets,
                                   'third_place': third_place,
                                   'final': final,
                                   'total_score': score.total_score,
                                   'podium_scores': score.podium_scores},
                                  RequestContext(request))


class Score:
    """
    total_score = placar total do jogador
    score_by_bets = dicionário (id do jogo) -> score
    podium_scores = dicionario pontos extras do podium (posicao) -> score
    """
    def __init__(self, user):

        self.user = user
        self.score_by_bets = {}
        self.total_score = 0.0
        self.podium_scores = {}

        if  Bet.objects.filter(player=self.user).exists():
            self.score_by_bets = self._compute_all_bets()
            self.total_score = reduce(lambda x, y: x + y, self.score_by_bets.values(), 0.0)

            third_place = Bet.objects.get(game__id=63)
            final = Bet.objects.get(game__id=64)

            # pontos por acertar os quatro primeiros
            self.podium_scores = {1: 0.0, 2: 0.0, 3: 0.0, 4: 0.0}
            if third_place.get_loser() == third_place.game.get_loser():
                self.podium_scores[4] = 3
                self.total_score += 3
            if third_place.get_winner() == third_place.game.get_winner():
                self.podium_scores[3] = 4
                self.total_score += 4
            if final.get_loser() == final.game.get_loser():
                self.podium_scores[2] = 10
                self.total_score += 10
            if final.get_winner() == final.game.get_winner():
                self.podium_scores[1] = 15
                self.total_score += 15

    def get_bet_score(self, match_id):
        return self.score_by_bets.get(match_id, 0.0)

    def _compute_bet_score(self, bet):
        score = 0.0

        if bet.game.status != Game.STATUS_NOT_STARTED:
            if bet.is_a_tie() and bet.game.is_a_tie():
                # jogador apostou no empate E foi empate
                    score += 4
                    if bet.home_score == bet.game.home_goals_normal_time:
                        score += 2
            elif not bet.is_a_tie() and not bet.game.is_a_tie():
                # jogador não apostou em empateo E não foi empate
                if bet.home_score == bet.game.home_goals_normal_time:
                    score += 1.5
                if bet.away_score == bet.game.away_goals_normal_time:
                    score += 1.5
                if bet.get_winner() == bet.game.get_winner():
                    score += 3

        return score

    def _compute_all_bets(self):
        score_by_game = {}

        for bet in Bet.objects.filter(player=self.user):
            bet_score = self._compute_bet_score(bet)

            # Extra points for secound round
            if bet.game.stage == Game.ROUND_OF_16:
                if bet.home_team == bet.game.home_team:
                    bet_score += 6
                if bet.away_team == bet.game.away_team:
                    bet_score += 6

            if bet.game.stage == Game.QUARTER_FINALS:
                if bet.home_team == bet.game.home_team:
                    bet_score += 8
                if bet.away_team == bet.game.away_team:
                    bet_score += 8

            if bet.game.stage == Game.SEMI_FINALS:
                if bet.home_team == bet.game.home_team:
                    bet_score += 10
                if bet.away_team == bet.game.away_team:
                    bet_score += 10

            if bet.game.id == 63:
                # Disputa do terceiro lugar
                if bet.home_team == bet.game.home_team:
                    bet_score += 6
                if bet.away_team == bet.game.away_team:
                    bet_score += 6

            if bet.game.id == 64:
                # Disputa da final
                if bet.home_team == bet.game.home_team:
                    bet_score += 12
                if bet.away_team == bet.game.away_team:
                    bet_score += 12

            score_by_game[bet.game.id] = bet_score

        return score_by_game


