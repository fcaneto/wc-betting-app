#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json

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
        group_bets = Bet.objects.all().filter(player=request.user).filter(game__stage=Game.GROUP).order_by('game__id')
        round_16_bets = Bet.objects.all().filter(player=request.user).filter(game__stage=Game.ROUND_OF_16).order_by(
            'game__id')
        quarter_bets = Bet.objects.all().filter(player=request.user).filter(game__stage=Game.QUARTER_FINALS).order_by(
            'game__id')
        semi_bets = Bet.objects.all().filter(player=request.user).filter(game__stage=Game.SEMI_FINALS).order_by(
            'game__id')
        third_place = Bet.objects.get(game__id=63)
        final = Bet.objects.get(game__id=64)

        return render_to_response('player.html',
                                  {'group_bets': group_bets,
                                   'round_16_bets': round_16_bets,
                                   'quarter_bets': quarter_bets,
                                   'semi_bets': semi_bets,
                                   'third_place': third_place,
                                   'final': final},
                                  RequestContext(request))



