from random import shuffle
from typing import Protocol, TYPE_CHECKING, Optional

from Constante import BELOTE_VALUES, BELOTE_SUITS, BELOTE_TRUMP_SCORE, \
    BELOTE_SCORE

if TYPE_CHECKING:
    from player import Player


class State(Protocol):
    def get_player(self) -> Optional['Player']:
        ...

    def get_loc(self) -> str:
        ...

    @staticmethod
    def set_state_deck(card):
        ...

    @staticmethod
    def play_card(card: 'Cards', player: Optional['Player'] = None) -> None:
        ...


class StateDeck:
    def __init__(self):
        self.loc = "deck"
        self.player = None

    def get_player(self) -> Optional['Player']:
        return self.player

    def get_loc(self) -> str:
        return self.loc

    @staticmethod
    def set_state_deck(card):
        card.state = StateDeck()

    @staticmethod
    def play_card(card: 'Cards', player: Optional['Player'] = None) -> None:
        if player is None:
            card.state = StateFlipped()
            return None
        card.state = StateHand(player)


class StateFlipped:
    def __init__(self):
        self.loc = "flipped"
        self.player = None

    def get_player(self) -> Optional['Player']:
        return self.player

    def get_loc(self) -> str:
        return self.loc

    @staticmethod
    def set_state_deck(card):
        card.state = StateDeck()

    @staticmethod
    def play_card(card: 'Cards', player: Optional['Player'] = None) -> None:
        if player is not None:
            card.state = StateHand(player)


class StateHand:

    def __init__(self, player: 'Player'):
        self.player = player
        self.loc = "hand"

    def get_player(self) -> Optional['Player']:
        return self.player

    def get_loc(self) -> str:
        return self.loc

    @staticmethod
    def set_state_deck(card):
        card.state = StateDeck()

    @staticmethod
    def play_card(card: 'Cards', player: Optional['Player'] = None) -> None:
        if player is not None:
            card.state = StatePlayed(player)


class StatePlayed:
    def __init__(self, player: 'Player'):
        self.player = player
        self.loc = "played"

    def get_player(self) -> Optional['Player']:
        return self.player

    def get_loc(self) -> str:
        return self.loc

    @staticmethod
    def set_state_deck(card):
        card.state = StateDeck()

    @staticmethod
    def play_card(card: 'Cards', player: Optional['Player'] = None) -> None:
        pass


class Cards:
    """Basic representation of a card
    by its suit, color, score
    and its state"""

    def __init__(self, suit: str, value: str, state: State) -> None:
        self._suit = suit.upper()
        self._value = value.upper()
        self.state = state()
        self._score: int = 0
        self._legit: bool = False

    def get_pos(self) -> Optional[str]:
        if self.get_player() is not None:
            return self.get_player().get_pos()
        return None

    def get_loc(self) -> str:
        return self.state.get_loc()

    def get_player(self) -> Optional['Player']:
        return self.state.get_player()

    def set_score(self, n: int):
        self._score = n

    def get_score(self):
        return self._score

    def set_legit(self, legit: bool):
        self._legit = legit

    def get_legit(self):
        return self._legit

    def get_suit(self) -> str:
        return self._suit

    def get_value(self) -> str:
        return self._value

    def play_card(self, player: Optional['Player']):
        self.state.play_card(self, player)

    def reinitialize(self):
        self.state.set_state_deck(self)

    def __eq__(self, other):
        if isinstance(other, Cards):
            return self._suit == other._suit and self._value == self._value
        return False


def Generate32CardDeck():
    """create a belote deck (32 cards, 4 color, 7 to ace"""

    deck: list[Cards] = []
    for suit in BELOTE_SUITS:
        for value in BELOTE_VALUES:
            deck.append(Cards(suit, value, StateDeck))
    return deck


class BeloteDeck:

    def __init__(self, deck: list['Cards']):
        self.deck = deck

    def get_deck(self):
        return self.deck

    def draw_cards(self, player: 'Player', n: int = 1) -> None:
        draw = [x for x in self.deck if x.get_loc() == "deck"]
        for x in draw[:n]:
            x.play_card(player)

    def shuffle_deck(self) -> None:
        shuffle(self.deck)

    def set_card_score(self, trump: str) -> None:

        for card in self.deck:
            if card.get_suit() == trump:
                card.set_score(BELOTE_TRUMP_SCORE[card.get_value()])
            else:
                card.set_score(BELOTE_SCORE[card.get_value()])

    def reinitialize_cards(self) -> None:
        [c.reinitialize() for c in self.deck]

    def __str__(self) -> str:
        return (f"{len(self.deck)} cards left:\n"
                f"{chr(10).join(str(x) for x in self.deck)}\n"
                )

    def __iter__(self):
        for x in self.deck:
            yield x

    def __getitem__(self, item):
        return self.deck[item]
