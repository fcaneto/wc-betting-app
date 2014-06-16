#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json

from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib.auth import login as login_at_server
from django.contrib.auth import logout as logout_at_server
from django.http import HttpResponseRedirect, HttpResponse, HttpResponseForbidden
from django.template.context import RequestContext
from django.shortcuts import render_to_response
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required

from django.views.decorators.csrf import csrf_exempt

from bolao.models import Game, Bet, Team, BetRoom, Group


@login_required(login_url='login')
def change_password(request):
    if request.method == 'GET':
        return render_to_response('change_password.html', {'bet_room': request.user.player.bet_room}, RequestContext(request))
    else:
        password = request.POST.get('newPassword')
        password_check = request.POST.get('passwordCheck')

        if password != password_check or password is None:
            return render_to_response('change_password.html',
                                      {'bet_room': request.user.player.bet_room,
                                       'error': 'Senha não bateu, digite de novo.'},
                                      RequestContext(request))
        else:
            request.user.set_password(password)
            request.user.save()
            return render_to_response('change_password_ok.html', {'bet_room': request.user.player.bet_room},
                                      RequestContext(request))


@login_required(login_url='login')
def home(request):
    if request.user.player.bet_room.is_open_to_betting:
        url = reverse('sim')
    else:
        url = reverse('ranking')

    return HttpResponseRedirect(url)


@login_required(login_url='login')
def simulator(request):
    if not request.user.player.bet_room.is_open_to_betting:
        return HttpResponse("Hacker safado, tentando entrar direto com a URL. O bolão já foi fechado para edição.")
    else:
        return render_to_response('sim.html', {'bet_room': request.user.player.bet_room}, RequestContext(request))


@login_required(login_url='login')
def games(request):
    if request.user.player.bet_room.is_open_to_betting:
        return HttpResponse("Hacker safado, tentando entrar direto com a URL. O bolão ainda está aberto para edição.")
    else:
        users = User.objects.filter(player__bet_room=request.user.player.bet_room).exclude(id=request.user.id)
        return render_to_response('games.html',
                                  {'me': request.user,
                                   'users': users},
                                  RequestContext(request))


def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)

        if user:
            if user.is_active:
                login_at_server(request, user)
                return HttpResponseRedirect('/')
            else:
                return render_to_response('login.html', {'errorMsg': 'Conta desabilitada.'}, RequestContext(request))
        else:
            return render_to_response('login.html', {'errorMsg': 'Usuário / senha inválidos.'}, RequestContext(request))

    else:
        return render_to_response('login.html', {}, RequestContext(request))


@login_required(login_url='login')
def rules(request):
    return render_to_response('rules.html', {'bet_room': request.user.player.bet_room}, RequestContext(request))


@login_required(login_url='login')
def logout(request):
    logout_at_server(request)
    return HttpResponseRedirect('/')


@login_required(login_url='login')
def ranking(request):
    scores = []
    for user in User.objects.filter(player__bet_room=request.user.player.bet_room).order_by('first_name'):
        scores.append(Score(user))

    scores.sort(key=lambda score: score.total_score, reverse=True)
    # TODO: grouped scores

    current_game = Game.get_current_game()
    next_game_bets = []

    ranking = 1
    previous_score = None
    for score in scores:
        """
        adding ranking to each score
        """
        if previous_score is not None:
            if previous_score.total_score != score.total_score:
                ranking += 1
                score.ranking = ranking
            else:
                score.ranking = None
        else:
            score.ranking = ranking
        previous_score = score



        next_bet_query = Bet.objects.all().filter(game=current_game).filter(player=score.player)
        if score.player == request.user.player:
            my_bet = next_bet_query[0]
        else:
            if len(next_bet_query) > 0:
                next_game_bets.append(next_bet_query[0])

    return render_to_response('ranking.html',
                              {'bet_room': request.user.player.bet_room,
                               'scores': scores,
                               'my_bet': my_bet,
                               'next_game': current_game,
                               'next_game_bets': next_game_bets,
                               'me': request.user,
                               'game_ids': range(1,38),
                               'max_game_id': 38},
                              RequestContext(request))

@login_required(login_url='login')
def rivals(request):
    if request.user.player.bet_room.is_open_to_betting:
        return HttpResponse("Hacker safado, tentando entrar direto com a URL. O bolão ainda está aberto para edição.")
    else:
        users = User.objects.filter(player__bet_room=request.user.player.bet_room).exclude(id=request.user.id).order_by('first_name')
        return render_to_response('rivals.html',
                                  {'me': request.user,
                                   'others': users},
                                  RequestContext(request))

@login_required(login_url='login')
def player(request):
    score = Score(request.user)

    group_bets = []
    round_16_bets = []
    quarter_bets = []
    semi_bets = []
    third_place = None
    final = None

    player = request.user.player

    if Bet.query_all_bets(player).exists():
        group_bets = Bet.query_all_bets(player).filter(game__stage=Game.GROUP).order_by('game__id')
        round_16_bets = Bet.query_all_bets(player).filter(game__stage=Game.ROUND_OF_16).order_by(
            'game__id')
        quarter_bets = Bet.query_all_bets(player).filter(game__stage=Game.QUARTER_FINALS).order_by(
            'game__id')
        semi_bets = Bet.query_all_bets(player).filter(game__stage=Game.SEMI_FINALS).order_by(
            'game__id')

        third_place = Bet.get_by_match_id(player, 63)
        final = Bet.get_by_match_id(player, 64)

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
                              {'bet_room': request.user.player.bet_room,
                               'group_bets': group_bets,
                               'round_16_bets': round_16_bets,
                               'quarter_bets': quarter_bets,
                               'semi_bets': semi_bets,
                               'third_place': third_place,
                               'final': final,
                               'total_score': score.total_score,
                               'podium_scores': score.podium_scores},
                              RequestContext(request))


####################
# Bet Ajax API
####################
@login_required(login_url='login')
def bet_from_user(request, user_id):
    if request.method == 'GET':
        user = User.objects.get(pk=user_id)
        return render_bets(user)


@login_required(login_url='login')
def bet(request):
    if request.method == 'POST':

        if not request.user.player.bet_room.is_open_to_betting:
            return HttpResponseForbidden()

        bets = json.loads(request.body)

        games = {}
        for game in Game.objects.all():
            games[game.id] = game

        Bet.query_all_bets(request.user.player).delete()

        bets_to_be_saved = []
        for bet_dict in bets:
            id = bet_dict['id']
            home_score = int(bet_dict['homeScore'])
            away_score = int(bet_dict['awayScore'])

            teams = {}
            winner = None
            try:
                code = bet_dict['homeTeamCode']
                if code not in teams:
                    teams[code] = Team.objects.get(code=code)
                home_team = teams[code]

                code = bet_dict['awayTeamCode']
                if code not in teams:
                    teams[code] = Team.objects.get(code=code)
                away_team = teams[code]

                code = bet_dict['winnerCode']
                if code not in teams:
                    teams[code] = Team.objects.get(code=code)
                winner = teams[code]

            except KeyError:
                print 'Not a second round match'

            game = games[id]

            bets_to_be_saved.append(Bet(
                player=request.user.player,
                game=game,
                home_score=home_score,
                away_score=away_score,
                home_team=home_team,
                away_team=away_team,
                winner=winner))

        Bet.objects.bulk_create(bets_to_be_saved)

        return HttpResponse()

    elif request.method == 'GET':
        return render_bets(request.user)

    else:
        return HttpResponse(code=401)


def render_bets(user):
    response_data = {
        'groups': {'A': {},
                   'B': {},
                   'C': {},
                   'D': {},
                   'E': {},
                   'F': {},
                   'G': {},
                   'H': {}},
        'roundOf16': {},
        'quarterFinals': {},
        'semiFinals': {},
        'finals': {}
    }

    for bet in Bet.query_all_bets(user.player).filter(game__stage=Game.GROUP):
        match_data = {'homeScore': bet.home_score,
                      'awayScore': bet.away_score}
        group = bet.game.home_team.group.name
        response_data['groups'][group][bet.game.id] = match_data

    for bet in Bet.query_all_bets(user.player).filter(game__stage=Game.ROUND_OF_16):
        match_data = {'id': bet.game.id,
                      'homeScore': bet.home_score,
                      'awayScore': bet.away_score,
                      'winnerCode': bet.get_winner().code}
        response_data['roundOf16'][bet.game.id] = match_data

    for bet in Bet.query_all_bets(user.player).filter(game__stage=Game.QUARTER_FINALS):
        match_data = {'id': bet.game.id,
                      'homeScore': bet.home_score,
                      'awayScore': bet.away_score,
                      'winnerCode': bet.get_winner().code}
        response_data['quarterFinals'][bet.game.id] = match_data

    for bet in Bet.query_all_bets(user.player).filter(game__stage=Game.SEMI_FINALS):
        match_data = {'id': bet.game.id,
                      'homeScore': bet.home_score,
                      'awayScore': bet.away_score,
                      'winnerCode': bet.get_winner().code}
        response_data['semiFinals'][bet.game.id] = match_data

    for bet in Bet.query_all_bets(user.player).filter(game__stage=Game.FINALS):
        match_data = {'id': bet.game.id,
                      'homeScore': bet.home_score,
                      'awayScore': bet.away_score,
                      'winnerCode': bet.get_winner().code}
        response_data['finals'][bet.game.id] = match_data

    return HttpResponse(json.dumps(response_data), content_type="application/json")


class Score:
    """
    total_score = placar total do jogador
    score_by_bets = dicionário (id do jogo) -> score
    podium_scores = dicionario pontos extras do podium (posicao) -> score
    """
    def __init__(self, user):

        self.player = user.player
        self.score_by_bets = {}
        self.total_score = 0.0
        self.podium_scores = {}
        self.variation_game_id = 0

        self.all_player_bets = list(Bet.query_all_bets(self.player))
        if self.all_player_bets:
            self.has_bet = True
            self.score_by_bets = self._compute_all_bets()
            self.total_score = reduce(lambda x, y: x + y, self.score_by_bets.values(), 0.0)

            third_place = Bet.get_by_match_id(self.player, 63)
            final = Bet.get_by_match_id(self.player, 64)

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

    def set_game_for_variation(self, game):
        self.variation_game_id = game.id

    def variation(self):
        return self.score_by_bets[self.variation_game_id]

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
                # jogador não apostou em empate E não foi empate
                if bet.get_winner() == bet.game.get_winner():
                    score += 3
                    if bet.home_score == bet.game.home_goals_normal_time:
                        score += 1.5
                    if bet.away_score == bet.game.away_goals_normal_time:
                        score += 1.5


        return score

    def _compute_all_bets(self):
        score_by_game = {}

        for bet in Bet.query_all_bets(self.player):
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

    def get_bet_scores_as_list(self):
        bet_scores = []
        for i in range(1, 49):
            bet_scores.append(self.score_by_bets[i])
        return bet_scores

    def get_bets_as_list(self):
        return Bet.query_all_bets(self.player)


