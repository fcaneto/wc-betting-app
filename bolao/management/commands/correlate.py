#!/usr/bin/env python
# -*- coding: utf-8 -*-

from bolao.models import Group, Team, Game, Bet, BetRoom
from django.core.management.base import BaseCommand, CommandError


class Command(BaseCommand):
    help = 'Correlate players'

    def handle(self, *args, **options):

        max_score = 6 * 64 + 16 * 6 + 8 * 8 + 4 * 10 + 12 + 24

        for bet_room in BetRoom.objects.all():
            print 'Processing ' + bet_room.name

            player_list = list(bet_room.player_set.all())
            print '> %s players' % str(len(player_list))
            correlation_matrix = []
            for i in range(0, len(player_list)):
                column = []
                for j in range(0, len(player_list)):
                    column.append(0.0)
                correlation_matrix.append(column)

            all_bets = {}
            for player in player_list:
                bets_dict = {}
                for bet in Bet.objects.filter(player=player):
                    bets_dict[bet.game.id] = bet
                all_bets[player.id] = bets_dict
            print 'Got all bets'

            for i, player in enumerate(player_list):
                for j, other_player in enumerate(player_list):
                    total_score = 0.0
                    if i < j and len(all_bets[player.id]) > 0 and len(all_bets[other_player.id]) > 0:
                        for game_id in range(1, 65):
                            bet = all_bets[player.id][game_id]
                            other_bet = all_bets[other_player.id][game_id]

                            score = calculate_score(bet, other_bet)
                            total_score += score

                        correlation_matrix[i][j] = total_score/max_score
                    elif i > j:
                        correlation_matrix[i][j] = correlation_matrix[j][i]

            for i, player in enumerate(player_list):
                rival = None
                rival_correlation = 0.0
                for j, other_player in enumerate(player_list):
                    if correlation_matrix[i][j] > rival_correlation:
                        rival_correlation = correlation_matrix[i][j]
                        rival = other_player
                if rival:
                    print u'Rival de %s é %s (%s)' % (player.user.first_name, rival.user.first_name, rival_correlation)
                    player.rival = rival
                    player.rival_correlation = "{:.2%}".format(rival_correlation)
                    player.save()

        print 'Done!'


def calculate_score(bet, other_bet):
    score = 0.0
    if bet.is_a_tie() and other_bet.is_a_tie():
        # jogador apostou no empate E foi empate
        score += 4.0
        if bet.home_score == other_bet.home_score:
            score += 2.0
    elif not bet.is_a_tie() and not other_bet.is_a_tie():
        # jogador não apostou em empate E não foi empate
        if bet.get_winner() == other_bet.get_winner():
            score += 3.0
            if bet.home_score == other_bet.home_score:
                score += 1.5
            if bet.away_score == other_bet.away_score:
                score += 1.5

    if bet.game.stage == Game.ROUND_OF_16:
        if bet.home_team == other_bet.home_team:
            score += 6.0
        if bet.away_team == other_bet.away_team:
            score += 6.0

    if bet.game.stage == Game.QUARTER_FINALS:
        if bet.home_team == other_bet.home_team:
            score += 8.0
        if bet.away_team == other_bet.away_team:
            score += 8.0

    if bet.game.stage == Game.SEMI_FINALS:
        if bet.home_team == other_bet.home_team:
            score += 10.0
        if bet.away_team == other_bet.away_team:
            score += 10.0

    if bet.game.id == 63:
        # Disputa do terceiro lugar
        if bet.home_team == other_bet.home_team:
            score += 6.0
        if bet.away_team == other_bet.away_team:
            score += 6.0

    if bet.game.id == 64:
        # Disputa da final
        if bet.home_team == other_bet.home_team:
            score += 12.0
        if bet.away_team == other_bet.away_team:
            score += 12.0

    return float(score)