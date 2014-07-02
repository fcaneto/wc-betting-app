#!/usr/bin/env python
# -*- coding: utf-8 -*-

from bolao.models import Group, Team, Game, Bet, BetRoom
from django.core.management.base import BaseCommand, CommandError


class Command(BaseCommand):
    help = 'Validate players bets'

    def handle(self, *args, **options):

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
            finals = []

            round_of_16_winners = []
            quarter_winners = []
            semi_winners = []

            error = ""
            for i, player in enumerate(player_list):
                if len(all_bets[player.id]) > 0:
                    for game_id in range(49, 57):
                        bet = all_bets[player.id][game_id]
                        home = bet.home_team
                        away = bet.away_team
                        round_of_16.append(home)
                        round_of_16.append(away)
                        round_of_16_winners.append(bet.get_winner())
                    for game_id in range(57, 61):
                        bet = all_bets[player.id][game_id]
                        home = bet.home_team
                        away = bet.away_team
                        if home not in round_of_16 or away not in round_of_16:
                            error = 'Erro nas quartas - %s x %s' % (home.name, away.name)
                            break
                        quarter.append(home)
                        quarter.append(away)
                        quarter_winners.append(bet.get_winner())
                    if not error:
                        for game_id in [61, 62]:
                            bet = all_bets[player.id][game_id]
                            home = bet.home_team
                            away = bet.away_team
                            if home not in quarter or away not in quarter:
                                error = 'Erro nas semis'
                                break
                            semi.append(home)
                            semi.append(away)
                            semi_winners.append(bet.get_winner())
                    if not error:
                        for game_id in [63, 64]:
                            bet = all_bets[player.id][game_id]
                            home = bet.home_team
                            away = bet.away_team
                            finals.append(home)
                            finals.append(away)
                            if home not in quarter or away not in quarter:
                                error = 'Erro nas finais'
                                break

                for w in round_of_16_winners:
                    if w not in quarter:
                        error = u'Oitavas - Vencedor não passou!'
                        break

                if not error:
                    for w in quarter_winners:
                        if w not in semi:
                            error = u'Quartas - Vencedor não passou!'

                if not error:
                    for w in semi_winners:
                        if w not in finals:
                            error = u'Semi - Vencedor não passou!'

                if error:
                    print 'Player %s: %s' % (player.user.first_name, error)
                else:
                    print 'Player %s: OK' % (player.user.first_name)


        print 'Done!'
