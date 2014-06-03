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
        print bets

        Bet.objects.filter(player=request.user).delete()

        for bet in bets:
            id = bet['id']
            home_score = int(bet['homeScore'])
            away_score = int(bet['awayScore'])

            winner = None
            try:
                code = bet['winnerCode']
                print code
                winner = Team.objects.get(code=code)
                print winner
            except:
                print 'No winner'

            game = Game.objects.get(pk=id)
            Bet(player=request.user,
                game=game,
                home_score=home_score,
                away_score=away_score,
                winner=winner).save()

        return HttpResponse()

    else:
        group_bets = Bet.objects.all().filter(player=request.user).filter(game__stage=Game.GROUP).order_by('game__id')
        round_16_bets = Bet.objects.all().filter(player=request.user).filter(game__stage=Game.ROUND_OF_16).order_by('game__id')
        quarter_bets = Bet.objects.all().filter(player=request.user).filter(game__stage=Game.QUARTER_FINALS).order_by('game__id')
        semi_bets = Bet.objects.all().filter(player=request.user).filter(game__stage=Game.SEMI_FINALS).order_by('game__id')
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



