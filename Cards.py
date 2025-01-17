from random import shuffle
from typing import TYPE_CHECKING, Optional
from Constante import BELOTE_VALUES, BELOTE_SUITS, BELOTE_TRUMP_SCORE, \
    BELOTE_SCORE, CARD_PLOT_COORD, CARD_PLOT_STRING, OFFSET
from Protocols import CardState

if TYPE_CHECKING:
    from player import Player


class StateDeck:
    def __init__(self):
        self.loc = "deck"
        self.player = None
        self.pos = None
        self.image = None

    @staticmethod
    def play_card(card: 'Cards', player: Optional['Player'] = None) -> None:
        if player is None:
            card.state = StateFlipped()
            return None

        player.register_card(card)
        card.state = StateHand(player, card)


class StateFlipped:
    def __init__(self):
        self.loc = "flipped"
        self.player = None
        self.pos = CARD_PLOT_COORD["flipped"]
        self.image = CARD_PLOT_STRING["real_v"]

    @staticmethod
    def play_card(card: 'Cards', player: Optional['Player'] = None) -> None:
        if player is not None:
            player.register_card(card)
            card.state = StateHand(player, card)


class StateHand:

    def __init__(self, player: 'Player', card: 'Cards'):
        self.player = player
        self.loc = "hand"
        self.string_type = "real" if (player.pos == '1') else "dummy"

        pos_fetch = "_".join([self.string_type, player.orientation, self.loc, player.pos])
        self.pos = (CARD_PLOT_COORD[pos_fetch][0] + player.hand.index(card) * OFFSET[player.orientation][0],
                    CARD_PLOT_COORD[pos_fetch][1] + player.hand.index(card) * OFFSET[player.orientation][1])

        self.image = CARD_PLOT_STRING[self.string_type + "_" + player.orientation]

    def shift_one(self):
        self.pos = (self.pos[0] - OFFSET[self.player.orientation][0],
                    self.pos[1] - OFFSET[self.player.orientation][1])

    @staticmethod
    def play_card(card: 'Cards', player: Optional['Player'] = None) -> None:
        card_pos = player.hand.index(card)
        player.remove_card(card)
        for c in player.hand[card_pos:]:
            c.state.shift_one()
        card.state = StatePlayed(player)


class StatePlayed:
    def __init__(self, player: 'Player'):
        self.player = player
        self.loc = "played"
        self.pos = CARD_PLOT_COORD[f"real_{player.orientation}_played_{player.pos}"]
        self.image = CARD_PLOT_STRING[f"real_{player.orientation}"]

    @staticmethod
    def play_card(card: 'Cards', player: Optional['Player'] = None) -> None:
        pass


class Cards:
    """Basic representation of a card
    by its suit, color, score
    and its state"""

    def __init__(self, suit: str, value: str, state: 'CardState') -> None:
        self.suit = suit.upper()
        self.value = value.upper()
        self.state = state
        self.score: int = 0
        self.legit: bool = False

    def get_pos(self) -> Optional[str]:
        if self.get_player() is not None:
            return self.get_player().pos

    def get_loc(self) -> str:
        return self.state.loc

    def get_player(self) -> Optional['Player']:
        return self.state.player

    def play_card(self, player: Optional['Player']):
        self.state.play_card(self, player)

    def reinitialize(self):
        self.state = StateDeck()

    def __eq__(self, other):
        if isinstance(other, Cards):
            return self.suit == other.suit and self.value == other.value
        return False

    # def __str__(self):
    #     return f"{self.suit, self.value}"


def generate_32_card_deck():
    """create a belote deck (32 cards, 4 color, 7 to ace"""

    deck: list[Cards] = []
    for suit in BELOTE_SUITS:
        for value in BELOTE_VALUES:
            deck.append(Cards(suit, value, StateDeck()))
    return deck


class BeloteDeck:

    def __init__(self, deck):
        self.deck: list['Cards'] = deck

    def draw_cards(self, player: Optional['Player'], n: int = 1) -> None:
        draw = [x for x in self.deck if x.get_loc() == "deck"]
        for x in draw[:n]:
            x.play_card(player)

    def shuffle_deck(self) -> None:
        shuffle(self.deck)

    def set_card_score(self, trump: str) -> None:

        for card in self.deck:
            if card.suit == trump:
                card.score = BELOTE_TRUMP_SCORE[card.value]
            else:
                card.score = BELOTE_SCORE[card.value]

    def reinitialize_cards(self) -> None:
        [c.reinitialize() for c in self.deck]

    def __str__(self) -> str:
        return (f"{len(self.deck)} cards left:\n"
                f"{chr(10).join(str(x) for x in self.deck)}\n"
                )

    def __iter__(self):
        return iter(self.deck)

    def __getitem__(self, item):
        return self.deck[item]
