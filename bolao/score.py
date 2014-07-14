#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.contrib.auth.models import User
from bolao.models import BetRoom, Bet, Game
from itertools import izip
from django.core.cache import cache
import time

def build_scores(bet_room=None):
    print 'BUILDING Scores...'
    scores = []

    if bet_room is not None:
        for user in User.objects.filter(player__bet_room=bet_room):
            scores.append(Score(user))
        scores.sort(key=lambda score: score.total_score, reverse=True)
        return scores

    for bet_room in BetRoom.objects.all():
        for user in User.objects.filter(player__bet_room=bet_room):
            scores.append(Score(user))
        scores.sort(key=lambda score: score.total_score, reverse=True)
        #cache.set('scores_%s' % bet_room.id, scores)
    print 'BUILDING Scores... OK'


def get_scores(bet_room):
    #scores = cache.get('scores_%s' % bet_room.id)
    #if not scores:
    scores = build_scores(bet_room)
    #scores = cache.get('scores_%s' % bet_room.id)
    return scores


class Score:
    """
    total_score = placar total do jogador
    score_by_bets = dicionário (id do jogo) -> score
    podium_scores = dicionario pontos extras do podium (posicao) -> score
    bets = dicionario (id do jogo) -> bet
    """

    def __init__(self, user):

        self.player = user.player

        self.score_by_bets = {}
        self.total_score = 0.0
        self.podium_scores = {}
        self.variation_game_ids = 0

        self.first_round_first_half_score = 0.0
        self.first_round_second_half_score = 0.0
        self.round_of_16_qualified_score = 0.0
        self.quarter_finals_qualified_score = 0.0
        self.finals_qualified_score = 0.0

        start_time = time.time()

        bet_list = Bet.query_all_bets(self.player)
        self.bets = dict(izip([bet.game_id for bet in bet_list], bet_list))

        elapsed_time = time.time() - start_time
        print '[Score.1]: %.3f' % (elapsed_time)
        start_time = time.time()

        if self.bets:
            self.has_bet = True

            self.score_by_bets = self._compute_all_bets()

            elapsed_time = time.time() - start_time
            print '[Score.2]: %.3f' % (elapsed_time)
            start_time = time.time()

            self.third_place_bet = Bet.get_by_match_id(self.player, 63)
            self.final_bet = Bet.get_by_match_id(self.player, 64)
            
            # TODO: otimizar acesso aos games aqui
            # pontos por acertar os quatro primeiros
            self.podium_scores = {1: 0.0, 2: 0.0, 3: 0.0, 4: 0.0}
            if self.third_place_bet.get_loser() == self.third_place_bet.game.get_loser():
                self.podium_scores[4] = 3
                self.finals_qualified_score += 3
            if self.third_place_bet.get_winner() == self.third_place_bet.game.get_winner():
                self.podium_scores[3] = 4
                self.finals_qualified_score += 4
            if self.final_bet.get_loser() == self.final_bet.game.get_loser():
                self.podium_scores[2] = 10
                self.finals_qualified_score += 10
            if self.final_bet.get_winner() == self.final_bet.game.get_winner():
                self.podium_scores[1] = 15
                self.finals_qualified_score += 15

            self.total_score = reduce(lambda x, y: x + y, self.score_by_bets.values(), 0.0)
            self.total_score += self.round_of_16_qualified_score
            self.total_score += self.quarter_finals_qualified_score
            self.total_score += self.finals_qualified_score

            elapsed_time = time.time() - start_time
            print '[Score.3]: %.3f' % (elapsed_time)

    def set_games_for_variation(self, games):
        self.variation_game_ids = []
        for game in games:
            self.variation_game_ids.append(game.id)

    def variation(self):
        variation = 0
        for game_id in self.variation_game_ids:
            variation += self.score_by_bets[game_id]
        return variation

    def get_bet_score(self, match_id):
        return self.score_by_bets.get(match_id, 0.0)

    def _compute_bet_score(self, bet, game):
        score = 0.0

        if game.status != Game.STATUS_NOT_STARTED:
            if bet.is_a_tie() and game.is_a_tie():
            # jogador apostou no empate E foi empate
                score += 4
                if bet.home_score == game.home_goals_normal_time:
                    score += 2
            elif not bet.is_a_tie() and not game.is_a_tie():
                # jogador não apostou em empate E não foi empate
                if (bet.is_home_team_winner() and game.is_home_team_winner()) \
                    or (bet.is_away_team_winner() and game.is_away_team_winner()):
                    score += 3
                    if bet.home_score == game.home_goals_normal_time:
                        score += 1.5
                    if bet.away_score == game.away_goals_normal_time:
                        score += 1.5

        return score

    def _compute_all_bets(self):
        score_by_game = {}

        for game_id, bet in self.bets.iteritems():

            game = bet.game

            key = 'score_%s' % (bet.id)
            bet_score = cache.get(key)
            if not bet_score:
                bet_score = self._compute_bet_score(bet, game)
                cache.set(key, bet_score)

            # Extra points for secound round
            if game.stage == Game.ROUND_OF_16:
                self.round_of_16_qualified_score += 6 * bet.teams_got_right()

            if game.stage == Game.QUARTER_FINALS:
                self.quarter_finals_qualified_score += 8 * bet.teams_got_right()

            if game.stage == Game.SEMI_FINALS:
                self.finals_qualified_score += 10 * bet.teams_got_right()

            if bet.game_id == 63:
                # Disputa do terceiro lugar
                self.finals_qualified_score += 6 * bet.teams_got_right()

            if bet.game_id == 64:
                # Disputa da final
                self.finals_qualified_score += 12 * bet.teams_got_right()

            score_by_game[bet.game_id] = bet_score
            if bet.game_id < 25:
                self.first_round_first_half_score += bet_score
            elif bet.game_id < 49:
                self.first_round_second_half_score += bet_score

        return score_by_game

    def get_bet_scores_as_list(self):
        bet_scores = []
        for i in range(1, 49):
            bet_scores.append(self.score_by_bets[i])
        return bet_scores

    def get_bet(self, match_id):
        return self.bets[match_id]

    def get_round_of_16_bets(self):
        bets = []
        for i in range(49, 57):
            bets.append(self.bets[i])
        return bets

    def get_quarter_finals_bets(self):
        bets = []
        for i in range(57, 61):
            bets.append(self.bets[i])
        return bets

    def get_finals_bets(self):
        bets = []
        for i in range(61, 65):
            bets.append(self.bets[i])
        return bets

    def get_round_of_16_results_score(self):
        sum = 0.0
        for i in range(49, 57):
            sum += self.score_by_bets[i]
        return sum

    def get_quarter_finals_result_score(self):
        sum = 0.0
        for i in range(57, 61):
            sum += self.score_by_bets[i]
        return sum

    def get_finals_result_score(self):
        sum = 0.0
        for i in range(61, 65):
            sum += self.score_by_bets[i]
        return sum