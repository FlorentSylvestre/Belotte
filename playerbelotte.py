from dataclasses import dataclass
import random
from typing import TYPE_CHECKING, List
from Constante import BELOTE_SUITS

if TYPE_CHECKING:
    from Game_data import BelotteGame
    from Cards import Cards
    from Protocols import Strategy


class RealBelotteStrategy:
    @staticmethod
    def first_choice(game: 'BelotteGame') -> bool:
        return game.GUI.user_prompt("first_pick")

    @staticmethod
    def second_choice(game: 'BelotteGame') -> str:
        flipped = [x for x in game.deck if x.get_loc() == "flipped"][0]
        choice = [x for x in BELOTE_SUITS if x != flipped.suit]
        choice.append("NO")

        return game.GUI.user_prompt("second_pick", choice)

    @staticmethod
    def pick_play(hand: list['Cards'], game: 'BelotteGame') -> 'Cards':
        playable = [x for x in hand if x.legit]
        return game.GUI.user_prompt("play_card", playable)


class RandomBelotteStrategy:
    @staticmethod
    def first_choice(game: 'BelotteGame') -> bool:
        pick = [True, False]
        random.shuffle(pick)
        return False

    @staticmethod
    def second_choice(game: 'BelotteGame') -> str:
        flipped = [x for x in game.deck if x.get_loc() == "flipped"][0]
        choice = [x for x in BELOTE_SUITS if x != flipped.suit()]
        choice.append("NO")
        random.shuffle(choice)
        return choice.pop()

    @staticmethod
    def pick_play(hand: list['Cards'], game: "BelotteGame") -> 'Cards':
        return [x for x in hand if x.legit].pop()


@dataclass
class PlayerBelotte:
    name: str  # Useless for now
    team: int  # 0 or 1, shared by team member
    pos: str  # position of the board : 1,2,3 or 4. 1 is player, clockwise rotation
    strategy: "Strategy"

    def __post_init__(self):
        self.pick_play = self.strategy.pick_play
        self.second_choice = self.strategy.second_choice
        self.first_choice = self.strategy.first_choice
        self.orientation = self.team * "h" + (1-self.team) * "v"
        self.hand: List['Cards'] = []

    def register_card(self, c: 'Cards'):
        self.hand.append(c)

    def remove_card(self, c: 'Cards'):
        self.hand.remove(c)


@dataclass
class Winner:
    player: "PlayerBelotte"
    card: "Cards"

    def __post_init__(self):
        self.team: int = self.player.team
        self.suit: str = self.card.suit
        self.score: int = self.card.score


def define_players():
    """Create a basic set of player with random bots"""
    return [PlayerBelotte(input("Enter Name "), 0, "1", RealBelotteStrategy()),
            PlayerBelotte("Bot1", 1, "2", RandomBelotteStrategy()),
            PlayerBelotte("Bot2", 0, "3", RandomBelotteStrategy()),
            PlayerBelotte("Bot3", 1, "4", RandomBelotteStrategy())]
