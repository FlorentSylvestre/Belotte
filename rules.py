from typing import TYPE_CHECKING
from Constante import TOTAL_SCORE_ROUND
if TYPE_CHECKING:
    from Cards import Cards
    from Game_logic import BelotePlayerState, BelotteBoardState, BelotteGame
    from player import Player, Winner


def is_asked_trump(game: 'BelotteBoardState') -> bool:
    return game.get_asked_suit() == game.get_trump()


def is_trump_asked(game: 'BelotteBoardState') -> bool:
    return game.get_asked_suit() == game.get_trump()


def is_first_to_play(player: 'Player', first_player: 'Player') -> bool:
    return player.get_name() == first_player.get_name()


def has_trump(hand: list['Cards'], board: 'BelotteBoardState') -> bool:
    return any(card.get_suit() == board.get_trump() for card in hand)


def is_color_asked(card: 'Cards', board: 'BelotteBoardState') -> bool:
    return board.get_asked_suit() == card.get_suit()


def has_color_asked(hand: list['Cards'], board: 'BelotteBoardState') -> bool:
    return board.get_asked_suit() in [card.get_suit() for card in hand]


def is_trump(card: 'Cards', trump: str) -> bool:
    return trump == card.get_suit()


def beat_asked_trump(card: 'Cards', wining_trump: 'Winner') -> bool:
    return card.get_score() > wining_trump.get_card().get_score()


def other_beat_asked_trump(hand: list['Cards'], w_trump: 'Winner') -> bool:
    return any([card.get_score() > w_trump.get_score() for card in hand if card.get_suit() == w_trump.get_suit()])


def is_mate_master(player: 'Player', playersstate: 'BelotePlayerState', master: 'Winner'):
    return master.get_player() == playersstate.get_partner(player)


def IsPlayableBelotte(player: 'Player', card: 'Cards', game: 'BelotteGame') -> bool:

    hand = [x for x in game.get_deck() if x.get_player() == player]

    if is_first_to_play(player, game.get_first_player()):
        return True

    if not has_color_asked(hand, game.get_board()) and not has_trump(hand, game.get_board()):
        return True

    if is_color_asked(card, game.get_board()):
        if is_trump(card, game.get_board().get_trump()):
            return (beat_asked_trump(card, game.get_winner()) or
                    not other_beat_asked_trump(hand, game.get_winner()))
        return True

    if has_color_asked(hand, game.get_board()):
        if is_trump_asked(game.get_board()):
            return is_mate_master(player, game.get_players_state(), game.get_winner())
        return False

    if not is_trump(card, game.get_board().get_trump()):
        return False

    if is_trump(game.get_winner().get_card(), game.get_board().get_trump()):
        return (beat_asked_trump(card, game.get_board().get_winner()) or
                not other_beat_asked_trump(hand, game.get_board().get_winner()))
    return True


def is_round_won(score: int):
    return score >= (TOTAL_SCORE_ROUND / 2)


def is_capot(score: int):
    return score == 0
