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
from django.template.loader import render_to_string
from django.core.cache import cache

from score import Score, build_scores, get_scores

from django.views.decorators.csrf import csrf_exempt

from bolao.models import Game, Bet, Team


@login_required(login_url='login')
def change_password(request):
    if request.method == 'GET':
        return render_to_response('change_password.html', {'bet_room': request.user.player.bet_room},
                                  RequestContext(request))
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


def build_ranking_data(request):

    scores = get_scores(request.user.player.bet_room)

    current_games = Game.get_current_games()
    current_games_bets = []
    my_current_games_bets = []
    ranking = 1
    previous_score = None
    for score in scores:
        """
        adding ranking to each score
        """
        if previous_score is not None:
            if previous_score.total_score != score.total_score:
                score.ranking = ranking
            else:
                score.ranking = None
        else:
            score.ranking = ranking
        ranking += 1
        previous_score = score
        score.set_games_for_variation(current_games)

        game_bets = []
        for game in current_games:
            next_bet = score.get_bet(game.id)
            if score.player == request.user.player:
                my_current_games_bets.append(next_bet)
            else:
                game_bets.append(next_bet)

        if score.player != request.user.player:
            current_games_bets.append({'first_name': score.player.user.first_name,
                                       'last_name': score.player.user.last_name,
                                       'bets': game_bets})

    return current_games, current_games_bets, my_current_games_bets, scores

import time

@login_required(login_url='login')
def ranking(request):

    start_time = time.time()
    current_games, current_games_bets, my_current_games_bets, scores = build_ranking_data(request)

    elapsed_time = time.time() - start_time
    print '[1]: %.3f' % (elapsed_time)
    start_time = time.time()

    round_of_16_matches = Game.get_round_of_16_games()
    quarter_finals_matches = Game.get_quarter_finals_games()

    rendered_template = render_to_string('ranking.html',
                                         {'bet_room': request.user.player.bet_room,
                                          'scores': scores,
                                          'my_current_games_bets': my_current_games_bets,
                                          'current_games': current_games,
                                          'current_games_ids': map(lambda x: x.id, current_games),
                                          'current_games_bets': current_games_bets,
                                          'me': request.user,
                                          'round_of_16_matches': round_of_16_matches,
                                          'quarter_finals_matches': quarter_finals_matches},
                                         RequestContext(request))
    elapsed_time = time.time() - start_time
    print '[2]: %.3f' % (elapsed_time)

    return HttpResponse(rendered_template, content_type="text/html")


@login_required(login_url='login')
def rivals(request):
    if request.user.player.bet_room.is_open_to_betting:
        return HttpResponse("Hacker safado, tentando entrar direto com a URL. O bolão ainda está aberto para edição.")
    else:
        users = User.objects.filter(player__bet_room=request.user.player.bet_room).exclude(id=request.user.id).order_by(
            'first_name')
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



