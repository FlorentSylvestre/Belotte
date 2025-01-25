from random import shuffle
from typing import Optional
from Cards import Cards, BeloteDeck
from GUI import GUIBelotte
from playerbelotte import PlayerBelotte, Winner
from rules import is_playable_belotte
from scoring import BelotteScore
from Protocols import GameState

class BelotteDealState:

    @staticmethod
    def init_round(game: "BelotteGame", player: 'PlayerBelotte', suit=None):
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

            if game.board.get_winner_team() == game.has_taken.team:
                if game.count_turn == BelottePlayState.TOTAL_RUN:
                    game.score.der_de_der()
                game.score.update(game.board.current_Fold)

            game.board.archive_fold()
            game.players.reorder(game.get_winner().player)
            game.count_turn += 1
        game.deck.reinitialize_cards()


class BelotteGame:
    def __init__(self, boardstate, playerstate, deck, GUI):
        self.board: "BelotteBoardInfos" = boardstate
        self.players: "BelotePlayerInfos" = playerstate
        self.GUI: "GUIBelotte" = GUI
        self.score: BelotteScore = BelotteScore()
        self.state: "GameState" = BelotteDealState()
        self.deck: "BeloteDeck" = deck
        self.has_taken: Optional[PlayerBelotte] = None
        self.count_turn: int = 1
        self.game_played: bool = False

    def get_winner(self) -> Winner:
        return self.board.winner

    def get_hand(self, player: 'PlayerBelotte'):
        return [c for c in self.deck if c.get_player() == player]

    def set_playable_cards(self, player: 'PlayerBelotte', hand: list['Cards']) -> None:
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

    def player_turn(self, player: 'PlayerBelotte') -> 'Cards':
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
