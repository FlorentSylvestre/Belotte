import random
import time
from random import shuffle
from typing import Optional

from Cards import Cards, BeloteDeck
from Constante import TOTAL_SCORE_ROUND
from GUI import GUI
from player import Player, Winner, define_players
from rules import IsPlayableBelotte, is_round_won, is_capot, is_trump


class BelotePlayerState:

    def __init__(self):
        self.players: Optional[list[Player]] = None
        self.set_players(define_players())
        self.dealer: Player = self.players[3]
        self.reorder(self.players.index(self.dealer) + 1)

    def set_dealer(self, player: int) -> None:
        self.dealer = self.players[player]

    def get_dealer(self) -> Player:
        return self.dealer

    def set_players(self, players: list[Player]) -> None:
        self.players = players

    def get_players(self) -> list[Player]:
        return self.players

    def reorder(self, k: int) -> None:
        self.players = self.players[k:] + self.players[:k]

    def get_partner(self, player):
        return [p for p in self.get_players() if player.get_team() == p.get_team()
                and player.get_name() != p.get_name()]

    def shift_dealer(self) -> None:
        self.reorder(self.get_players().index(self.get_dealer()))
        self.set_dealer(1)
        self.reorder(self.get_players().index(self.get_dealer()) + 1)

    def __str__(self):
        return "This is a belotte card game."


class BelotteBoardState:

    def __init__(self):
        self.current_Fold: list[Cards] = []
        self.played_fold: list[list[Cards]] = []
        self.asked_suit: Optional[str] = None
        self.winner: Optional[Winner] = None
        self.trump: Optional[str] = None

    def get_winner(self) -> Optional[Winner]:
        return self.winner

    def get_winner_team(self) -> Optional[int]:
        if self.winner is not None:
            return self.winner.get_team()

    def get_winner_player(self) -> Optional[Player]:
        if self.winner is not None:
            return self.winner.get_player()

    def get_trump(self) -> str:
        return self.trump

    def set_trump(self, trump: str) -> None:
        self.trump = trump

    def get_asked_suit(self) -> str:
        return self.asked_suit

    def set_asked_suit(self, suit: str) -> None:
        self.asked_suit = suit

    def get_played(self) -> list[list[Cards]]:
        return self.played_fold

    def get_current(self) -> list[Cards]:
        return self.current_Fold

    def add_played_card(self, card: Cards) -> None:
        self.current_Fold.append(card)

    def archive_fold(self) -> None:
        for card in self.current_Fold:
            card.reinitialize()
        self.played_fold.append(self.current_Fold)
        self.current_Fold = []

    def update_winner(self, player: Player) -> None:
        last_play = self.get_current()[-1]
        is_winner_trump = is_trump(self.winner.get_card(), self.trump)
        is_last_play_trump = is_trump(last_play, self.trump)
        if not is_winner_trump and is_last_play_trump:
            self.winner = Winner(player, last_play)

        if is_winner_trump == is_last_play_trump and (last_play.get_score() > self.winner.get_card().get_score()):
            self.winner = Winner(player, last_play)


class BelotteGame:
    def __init__(self, boardstate: BelotteBoardState, playerstate: BelotePlayerState, deck: BeloteDeck):
        self.board = boardstate
        self.players = playerstate
        self.GUI = GUI()
        self.deck = deck
        self.has_taken: Optional[Player] = None
        self.count_turn: int = 1
        self.game_played: bool = False
        self.score: dict[int, int] = {0: 0, 1: 0}

    def get_winner(self) -> Winner:
        return self.board.get_winner()

    def get_winner_player(self) -> Optional['Player']:
        return self.board.get_winner_player()

    def get_winner_team(self) -> Optional['int']:
        return self.board.get_winner_team()

    def set_winner(self, winner: 'Winner'):
        self.board.winner = winner

    def get_players(self) -> list[Player]:
        return self.players.get_players()

    def get_deck(self) -> 'BeloteDeck':
        return self.deck

    def get_first_player(self):
        return self.get_players()[0]

    def get_board(self):
        return self.board

    def get_players_state(self):
        return self.players

    def deal(self, player: Optional['Player'], n: int) -> None:
        self.deck.draw_cards(player, n)

    def init_round(self, player: 'Player', suit=None):
        if suit is None:
            self.board.set_trump(self.deck[20].get_suit())
        else:
            self.board.set_trump(suit)
        self.deck[20].play_card(player)
        self.has_taken = player
        self.score = {0: 0, 1: 0}
        self.game_played = True

    def take_round_one(self) -> None:
        for player in self.get_players():
            if player.first_choice(self):
                self.init_round(player)
                return None

    def take_round_two(self):
        for player in self.get_players():
            suit = player.second_choice(self)
            if suit != "NO":
                self.init_round(player, suit)
            return None

    def print_grid(self):
        self.GUI.reinitialize_grid()
        self.GUI.update_grid(self.deck)
        self.GUI.clear_screen()
        self.GUI.print_grid()

    def start_phase(self) -> None:
        for player in self.get_players():
            self.deal(player, 2)
        for player in self.get_players():
            self.deal(player, 3)
        self.deal(None, 1)
        self.print_grid()
        self.take_round_one()
        if not self.game_played:
            self.take_round_two()

    def reinitialize_round(self, new_deck: list[list['Cards']]) -> None:
        shuffle(new_deck)
        self.deck = BeloteDeck([j for i in new_deck for j in i])
        self.deck.reinitialize_cards()

    def get_hand(self, player: 'Player'):
        return [c for c in self.deck if c.get_player() == player]

    def set_playable_cards(self, player: 'Player', hand: list['Cards']) -> None:
        for card in hand:
            card.set_legit(IsPlayableBelotte(player, card, self))

    def player_turn(self, player: 'Player') -> 'Cards':
        hand = [x for x in self.deck if x.get_player() == player]
        self.set_playable_cards(player, hand)
        self.print_grid()
        pick = player.pick_play(hand, self)
        pick.play_card(player)
        return pick

    def update_score(self) -> None:
        score = 0
        for card in self.board.get_current():
            score += card.get_score()
        if self.count_turn == 8:
            score += 10
        self.score[self.has_taken.team] += score

    def parse_score_round(self) -> dict[int, int]:
        if not self.game_played:
            return {0: 0,
                    1: 0}

        if is_capot(self.score[self.has_taken.team]):
            return {self.has_taken.get_team(): 0,
                    (1 - self.has_taken.get_team()): 2 * TOTAL_SCORE_ROUND}

        if is_capot(TOTAL_SCORE_ROUND - self.score[self.has_taken.team]):
            return {self.has_taken.get_team(): 2 * TOTAL_SCORE_ROUND,
                    (1 - self.has_taken.get_team()): 0}

        if is_round_won(self.score[self.has_taken.team]):
            return {self.has_taken.team: self.score[self.has_taken.get_team()],
                    (1 - self.has_taken.team): TOTAL_SCORE_ROUND - self.score[self.has_taken.get_team()]}

        return {self.has_taken.team: 0,
                (1 - self.has_taken.team): TOTAL_SCORE_ROUND}

    def reinitialize_score(self) -> None:
        [c.set_legit(False) for c in self.deck]

    def run_round(self) -> (int, int):
        self.start_phase()
        if not self.game_played:
            hands = [self.get_hand(p) for p in self.get_players()]
            hands.append([x for x in self.deck if x.get_loc() == "flipped"])
            hands.append([x for x in self.deck if x.get_loc() == "deck"])
            self.reinitialize_round(hands)
            return [self.parse_score_round(), self.deck]

        for p in self.get_players():
            if p == self.has_taken:
                self.deal(p, 2)
                continue
            self.deal(p, 3)

        self.deck.set_card_score(self.board.get_trump())

        while self.count_turn <= 8:
            for player in self.get_players():
                play = self.player_turn(player)
                self.board.add_played_card(play)
                self.print_grid()
                if len(self.board.get_current()) == 1:
                    self.board.set_asked_suit(play.get_suit())
                    self.set_winner(Winner(player, play))
                    continue
                self.board.update_winner(player)
            self.reinitialize_score()

            if self.get_winner_team() == self.has_taken.team:
                self.update_score()

            self.board.archive_fold()
            self.players.reorder(self.players.get_players().index(self.get_winner_player()))
            self.count_turn += 1
            time.sleep(5)
            self.print_grid()

        self.reinitialize_round(self.board.get_played())
        self.players.shift_dealer()
        self.GUI.reinitialize_grid()
        return [self.parse_score_round(), self.deck]
