from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from Cards import Cards
    from Game_data import BelotePlayerInfos, BelotteBoardInfos, BelotteGame
    from playerbelotte import PlayerBelotte, Winner


def is_asked_trump(board: 'BelotteBoardInfos') -> bool:
    return board.asked_suit == board.trump


def is_trump_asked(board: 'BelotteBoardInfos') -> bool:
    return board.asked_suit == board.trump


def is_first_to_play(player: 'PlayerBelotte', first_player: 'PlayerBelotte') -> bool:
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


def is_mate_master(player: 'PlayerBelotte', playersstate: 'BelotePlayerInfos', master: 'Winner') -> bool:
    return master.player == playersstate.get_partner(player)


def is_playable_belotte(player: 'PlayerBelotte', card: 'Cards', game: 'BelotteGame') -> bool:
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

    if is_mate_master(player, game.players, game.get_winner()):
        return True

    if not is_trump(card, game.board.trump):
        return False

    if is_trump(game.get_winner().card, game.board.trump):
        return (beat_asked_trump(card, game.get_winner()) or
                not other_beat_asked_trump(hand, game.get_winner()))
    return True


def is_winner_belotte(board: 'BelotteBoardInfos') -> bool:
    last_play = board.current_Fold[-1]

    if len(board.current_Fold) == 1:
        return True

    is_winner_trump = is_trump(board.winner.card, board.trump)
    is_last_play_trump = is_trump(last_play, board.trump)
    if not is_winner_trump and is_last_play_trump:
        return True

    if is_winner_trump == is_last_play_trump and (last_play.score > self.winner.card.score):
        return True

    return False
