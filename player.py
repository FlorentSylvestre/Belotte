from dataclasses import dataclass
import random
from typing import TYPE_CHECKING
from Constante import BELOTE_SUITS

if TYPE_CHECKING:
    from Game_logic import BelotteGame
    from Cards import Cards
    from Protocols import Strategy


class RealBelotteStrategy:
    @staticmethod
    def first_choice(game: 'BelotteGame') -> bool:
        pick = ""
        while pick.upper() not in ["Y", "YES", "OUI", "N", "NO", "NON"]:
            pick = game.GUI.prompt_first_pick()
        return pick.upper() in ["Y", "YES", "OUI"]

    @staticmethod
    def second_choice(game: 'BelotteGame') -> str:
        pick = None
        flipped = [x for x in game.deck if x.get_loc() == "flipped"][0]
        choice = [x for x in BELOTE_SUITS if x != flipped.suit]
        choice.append("NO")
        while pick not in [str(x) for x in range(len(choice))]:
            pick = game.GUI.prompt_second_pick(choice)
        return choice[int(pick)]

    @staticmethod
    def pick_play(hand: list['Cards'], game: 'BelotteGame') -> 'Cards':
        pick = None
        playable = [x for x in hand if x.legit]
        while pick not in [str(x) for x in range(len(playable))]:
            pick = game.GUI.prompt_play_card()
        return playable[int(pick)]


class RandomBelotteStrategy:
    @staticmethod
    def first_choice(game: 'BelotteGame') -> bool:
        pick = [True, False]
        random.shuffle(pick)
        return False

    @staticmethod
    def second_choice(game: 'BelotteGame') -> str:
        flipped = [x for x in game.deck if x.get_loc() == "flipped"][0]
        choice = [x for x in BELOTE_SUITS if x != flipped.get_suit()]
        choice.append("NO")
        random.shuffle(choice)
        return choice.pop()

    @staticmethod
    def pick_play(hand: list['Cards'], game: "BelotteGame") -> 'Cards':
        return [x for x in hand if x.legit].pop()


@dataclass
class Player:
    name: str  # Useless for now
    team: int  # 0 or 1, shared by team member
    pos: str  # position of the board : 1,2,3 or 4. 1 is player, clockwise rotation
    strategy: "Strategy"

    def __post_init__(self):
        self.pick_play = self.strategy.pick_play
        self.second_choice = self.strategy.second_choice
        self.first_choice = self.strategy.first_choice


@dataclass
class Winner:
    player: "Player"
    card: "Cards"

    def __post_init__(self):
        self.team: int = self.player.team
        self.suit: str = self.card.suit
        self.score: int = self.card.score


def define_players():
    """Create a basic set of player with random bots"""
    return [Player(input("Enter Name "), 0, "1", RealBelotteStrategy()),
            Player("Bot1", 1, "2", RandomBelotteStrategy()),
            Player("Bot2", 0, "3", RandomBelotteStrategy()),
            Player("Bot3", 1, "4", RandomBelotteStrategy())]
