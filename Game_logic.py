import os
import time
from random import shuffle
from typing import Optional
from Cards import Cards, BeloteDeck
from GUI import GUIBelotte
from player import Player, Winner
from rules import is_playable_belotte, is_trump
from scoring import BelotteScore
from Protocols import GameState


class BelotePlayerInfos:

    def __init__(self, players):
        self.players: Optional[list[Player]] = players
        self.dealer: Player = players[3]  # TODO randomize first dealer later, is fixed for testing
        self.reorder(self.players.index(self.dealer) + 1)

    def reorder(self, p: int | Player) -> None:
        k = p if isinstance(p, int) else self.players.index(p)
        self.players = self.players[k:] + self.players[:k]

    def shift_dealer(self) -> None:
        """ Set the player left to the last dealer as the new dealer"""
        index = self.players.index(self.dealer)
        if index == 4:  # Handle when previous dealer is last on list
            index = 0

        self.reorder(index)
        self.dealer = self.players[index]

    def get_partner(self, player) -> Player:
        for p in self.players:
            if player.team == p.team and player.name != p.name:
                return p

    def __getitem__(self, item) -> Player | list[Player]:
        return self.players[item]


class BelotteBoardInfos:
    def __init__(self):
        self.current_Fold: list[Cards] = []
        self.played_fold: list[list[Cards]] = []
        self.asked_suit: Optional[str] = None
        self.winner: Optional[Winner] = None
        self.trump: Optional[str] = None

    def add_played_card(self, card: Cards) -> None:
        self.current_Fold.append(card)

    def archive_fold(self) -> None:
        for card in self.current_Fold:
            card.reinitialize()
        self.played_fold.append(self.current_Fold)
        self.current_Fold = []

    def update_winner(self, player: Player) -> None:  # TODO This should be in the rules
        last_play = self.current_Fold[-1]
        if len(self.current_Fold) == 1:
            self.winner = Winner(player, last_play)
            return None

        is_winner_trump = is_trump(self.winner.card, self.trump)
        is_last_play_trump = is_trump(last_play, self.trump)

        if not is_winner_trump and is_last_play_trump:
            self.winner = Winner(player, last_play)
            return None

        if is_winner_trump == is_last_play_trump and (last_play.score > self.winner.card.score):
            self.winner = Winner(player, last_play)

    def get_winner_team(self) -> Optional[int]:
        if self.winner is not None:
            return self.winner.team


class BelotteDealState:

    @staticmethod
    def init_round(game: "BelotteGame", player: 'Player', suit=None):
        if suit is None:
            game.board.trump = game.deck[20].suit
        else:
            game.board.trump = suit
        game.deck[20].play_card(player)
        game.has_taken = player
        game.game_played = True

    @staticmethod
    def take_round_one(game: "BelotteGame") -> None:
        for player in game.players:
            if player.first_choice(game):
                BelotteDealState.init_round(game, player)
                return None

    @staticmethod
    def take_round_two(game):
        for player in game.players:
            suit = player.second_choice(game)
            if suit != "NO":
                BelotteDealState.init_round(game, player, suit)
            return None

    @staticmethod
    def run_game(game: "BelotteGame"):
        for player in game.players:
            game.deck.draw_cards(player, 2)
        for player in game.players:
            game.deck.draw_cards(player, 3)
        game.deck.draw_cards(None, 1)
        game.print_game()
        BelotteDealState.take_round_one(game)
        if not game.game_played:
            BelotteDealState.take_round_two(game)
        game.state = BelottePlayState()


class BelottePlayState:
    TOTAL_RUN = 8

    @staticmethod
    def run_game(game: "BelotteGame"):
        for p in game.players:
            if p == game.has_taken:
                game.deck.draw_cards(p, 2)
                continue
            game.deck.draw_cards(p, 3)

        game.deck.set_card_score(game.board.trump)

        while game.count_turn <= BelottePlayState.TOTAL_RUN:
            for player in game.players:
                play = game.player_turn(player)
                game.board.add_played_card(play)
                if len(game.board.current_Fold) == 1:
                    game.board.asked_suit = play.suit
                game.board.update_winner(player)
            game.print_game()
            os.system("pause")

            if game.board.get_winner_team() == game.has_taken.team:
                if game.count_turn == BelottePlayState.TOTAL_RUN:
                    game.score.der_de_der()
                game.score.update(game.board.current_Fold)

            game.board.archive_fold()
            game.players.reorder(game.get_winner().player)
            game.count_turn += 1
            time.sleep(5)
        game.deck.reinitialize_cards()


class BelotteGame:
    def __init__(self, boardstate, playerstate, deck, GUI):
        self.board: "BelotteBoardInfos" = boardstate
        self.players: "BelotePlayerInfos" = playerstate
        self.GUI: "GUIBelotte" = GUI
        self.score: BelotteScore = BelotteScore()
        self.state: "GameState" = BelotteDealState()
        self.deck: "BeloteDeck" = deck
        self.has_taken: Optional[Player] = None
        self.count_turn: int = 1
        self.game_played: bool = False

    def get_winner(self) -> Winner:
        return self.board.winner

    def get_hand(self, player: 'Player'):
        return [c for c in self.deck if c.get_player() == player]

    def set_playable_cards(self, player: 'Player', hand: list['Cards']) -> None:
        for card in hand:
            card.legit = is_playable_belotte(player, card, self)

    def print_game(self):
        self.GUI.update_grid(self.deck)
        self.GUI.clear_screen()
        self.GUI.print_grid()

    def reinitialize_round(self, new_deck: list[list['Cards']]) -> None:
        shuffle(new_deck)
        self.deck = BeloteDeck([j for i in new_deck for j in i])
        self.deck.reinitialize_cards()


    def player_turn(self, player: 'Player') -> 'Cards':
        hand = [x for x in self.deck if x.get_player() == player]
        self.set_playable_cards(player, hand)
        self.print_game()

        pick = player.pick_play(hand, self)
        pick.play_card(player)
        return pick

    def run_round(self) -> tuple[dict[int, int], BeloteDeck]:
        self.state.run_game(self)
        if not self.game_played:
            hands = [self.get_hand(p) for p in self.players]
            hands.append([x for x in self.deck if x.get_loc() == "flipped"])
            hands.append([x for x in self.deck if x.get_loc() == "deck"])
            self.reinitialize_round(hands)
            return self.score.round_score(self), self.deck

        self.state.run_game(self)
        self.reinitialize_round(self.board.played_fold)
        self.players.shift_dealer()
        self.GUI.reinitialize_grid()
        return self.score.round_score(self), self.deck
