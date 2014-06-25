#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.contrib.auth.models import User
from bolao.models import BetRoom, Bet, Game
from itertools import izip
from django.core.cache import cache

def build_scores():
    print 'BUILDING Scores...'
    scores = []
    for bet_room in BetRoom.objects.all():
        for user in User.objects.filter(player__bet_room=bet_room):
            scores.append(Score(user))
        scores.sort(key=lambda score: score.total_score, reverse=True)

    cache.set('scores', scores)
    print 'BUILDING Scores... OK'
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

        bet_list = list(Bet.query_all_bets(self.player))
        self.bets = dict(izip([bet.game.id for bet in bet_list], bet_list))

        if self.bets:
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

        for game_id, bet in self.bets.iteritems():
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

    def get_bet(self, match_id):
        print '\n\n\n\n\n'
        print self.bets
        return self.bets[match_id]

    def get_round_of_16_bets(self):
        bets = []
        for i in range(49, 57):
            bets.append(self.bets[i])
        return bets
