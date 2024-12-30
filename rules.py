from typing import TYPE_CHECKING
from Constante import TOTAL_SCORE_ROUND
if TYPE_CHECKING:
    from Cards import Cards
    from Game_logic import BelotePlayerInfos, BelotteBoardInfos, BelotteGame
    from player import Player, Winner


def is_asked_trump(board: 'BelotteBoardInfos') -> bool:
    return board.asked_suit == board.trump


def is_trump_asked(board: 'BelotteBoardInfos') -> bool:
    return board.asked_suit == board.trump


def is_first_to_play(player: 'Player', first_player: 'Player') -> bool:
    return player.name == first_player.name


def has_trump(hand: list['Cards'], board: 'BelotteBoardInfos') -> bool:
    return any(card.suit == board.trump for card in hand)


def is_color_asked(card: 'Cards', board: 'BelotteBoardInfos') -> bool:
    return board.asked_suit == card.suit


def has_color_asked(hand: list['Cards'], board: 'BelotteBoardInfos') -> bool:
    return board.asked_suit in [card.suit for card in hand]


def is_trump(card: 'Cards', trump: str) -> bool:
    return trump == card.suit


def beat_asked_trump(card: 'Cards', wining_trump: 'Winner') -> bool:
    return card.score > wining_trump.score


def other_beat_asked_trump(hand: list['Cards'], w_trump: 'Winner') -> bool:
    return any([card.score > w_trump.score for card in hand if card.suit == w_trump.suit])


def is_mate_master(player: 'Player', playersstate: 'BelotePlayerInfos', master: 'Winner'):
    return master.player == playersstate.get_partner(player)


def is_playable_belotte(player: 'Player', card: 'Cards', game: 'BelotteGame') -> bool:
    hand = [x for x in game.deck if x.get_player() == player]

    if is_first_to_play(player, game.players[0]):
        return True

    if not has_color_asked(hand, game.board) and not has_trump(hand, game.board):
        return True

    if is_color_asked(card, game.board):
        if is_trump(card, game.board.trump):
            return (beat_asked_trump(card, game.get_winner()) or
                    not other_beat_asked_trump(hand, game.get_winner()))
        return True

    if has_color_asked(hand, game.board):
        if is_trump_asked(game.board):
            return is_mate_master(player, game.players, game.get_winner())
        return False

    if not is_trump(card, game.board.trump):
        return False

    if is_trump(game.get_winner().card, game.board.trump):
        return (beat_asked_trump(card, game.get_winner()) or
                not other_beat_asked_trump(hand, game.get_winner()))
    return True


def is_round_won(score: int):
    return score >= (TOTAL_SCORE_ROUND / 2)


def is_capot(score: int):
    return score == 0


class BelotteScore:
    def __init__(self):
        self.score: int = 0

    def update(self, turn: list["Cards"]) -> None:
        score = 0
        for card in turn:
            score += card.score
        self.score += score

    def der_de_der(self) -> None:
        self.score += 10

    def round_score(self, game: "BelotteGame") -> dict[int, int]:
        if not game.game_played:
            return {0: 0,
                    1: 0}

        if is_capot(self.score):
            return {game.has_taken.team: 0,
                    (1 - game.has_taken.team): 2 * TOTAL_SCORE_ROUND}

        if is_capot(TOTAL_SCORE_ROUND - self.score):
            return {game.has_taken.team: 2 * TOTAL_SCORE_ROUND,
                    (1 - game.has_taken.team): 0}

        if is_round_won(self.score):
            return {game.has_taken.team: self.score,
                    (1 - game.has_taken.team): TOTAL_SCORE_ROUND - self.score}

        return {game.has_taken.team: 0,
                (1 - game.has_taken.team): TOTAL_SCORE_ROUND}
