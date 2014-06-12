#!/usr/bin/env python
# -*- coding: utf-8 -*-

from bolao.models import Group, Team, Game, Bet, BetRoom
from django.core.management.base import BaseCommand, CommandError


class Command(BaseCommand):
    help = 'Correlate players'

    def handle(self, *args, **options):

        max_score = 6 * 64 + 16*6 + 8*8 + 4*10 + 12 + 24
        print 'MAX is %s' % max_score

        for bet_room in BetRoom.objects.all():
            print 'Processing ' + bet_room.name

            player_list = list(bet_room.player_set.all())
            print '> %s players' % str(len(player_list))

            all_bets = {}
            for player in player_list:
                bets_dict = {}
                for bet in Bet.objects.filter(player=player):
                    bets_dict[bet.game.id] = bet
                all_bets[player.id] = bets_dict
            print 'Got all bets'

            round_of_16 = []
            quarter = []
            semi = []

            error = ""
            for i, player in enumerate(player_list):
                if len(all_bets[player.id]) > 0:
                    for game_id in range(49, 57):
                        home = all_bets[player.id][game_id].home_team
                        away = all_bets[player.id][game_id].away_team
                        round_of_16.append(home)
                        round_of_16.append(away)
                    for game_id in range(57, 61):
                        home = all_bets[player.id][game_id].home_team
                        away = all_bets[player.id][game_id].away_team
                        if home not in round_of_16 or away not in round_of_16:
                            error = 'Erro nas quartas - %s x %s' % (home.name, away.name)
                            break
                        quarter.append(home)
                        quarter.append(away)
                    if not error:
                        for game_id in [61, 62]:
                            home = all_bets[player.id][game_id].home_team
                            away = all_bets[player.id][game_id].away_team
                            if home not in quarter or away not in quarter:
                                error = 'Erro nas semis'
                                break
                            semi.append(home)
                            semi.append(away)
                    if not error:
                        for game_id in [63, 64]:
                            home = all_bets[player.id][game_id].home_team
                            away = all_bets[player.id][game_id].away_team
                            if home not in quarter or away not in quarter:
                                error = 'Erro nas finais'
                                break
                if error:
                    print 'Player %s: %s' % (player.user.first_name, error)


        print 'Done!'
