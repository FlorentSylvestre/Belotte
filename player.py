import random
from typing import TYPE_CHECKING, Protocol

from Constante import BELOTE_SUITS

if TYPE_CHECKING:
    from Game_logic import BelotteGame
    from Cards import Cards


class Strategy(Protocol):
    @staticmethod
    def first_choice(game: 'BelotteGame') -> bool:
        ...

    @staticmethod
    def second_choice(game: 'BelotteGame') -> str:
        ...

    @staticmethod
    def pick_play(hand: list['Cards'], game: 'BelotteGame') -> 'Cards':
        ...


class RealBelotteStrategy:
    @staticmethod
    def first_choice(game: 'BelotteGame') -> bool:
        pick = ""
        while pick.upper() not in ["Y", "YES", "OUI", "N", "NO", "NON"]:
            game.GUI.clear_screen()
            game.GUI.print_grid()
            pick = game.GUI.prompt_first_pick()
        return pick.upper() in ["Y", "YES", "OUI"]

    @staticmethod
    def second_choice(game: 'BelotteGame') -> str:
        pick = None
        flipped = [x for x in game.get_deck() if x.get_loc() == "flipped"][0]
        choice = [x for x in BELOTE_SUITS if x != flipped.get_suit()]
        choice.append("NO")
        while pick not in [str(x) for x in range(len(choice))]:
            game.GUI.clear_screen()
            game.GUI.print_grid()
            pick = game.GUI.prompt_second_pick(choice)
        return choice[int(pick)]

    @staticmethod
    def pick_play(hand: list['Cards'], game: 'BelotteGame') -> 'Cards':
        pick = None
        playable = [x for x in hand if x.get_legit()]
        while pick not in [str(x) for x in range(len(playable))]:
            game.GUI.clear_screen()
            game.GUI.print_grid()
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
        flipped = [x for x in game.get_deck() if x.get_loc() == "flipped"][0]
        choice = [x for x in BELOTE_SUITS if x != flipped.get_suit()]
        choice.append("NO")
        random.shuffle(choice)
        return "NO"

    @staticmethod
    def pick_play(hand: list['Cards'], game: 'BelotteGame') -> 'Cards':
        return [x for x in hand if x.get_legit()].pop()


class Player:

    def __init__(self, name: str, team: int, pos: str, strategy: 'Strategy') -> None:
        self.name = name
        self.team = team
        self.pos = str(pos)
        self.is_reel = None
        self.strategy = strategy()

    def get_pos(self):
        return self.pos

    def get_name(self) -> str:
        return self.name

    def get_team(self) -> int:
        return self.team

    def pick_play(self, hand: list['Cards'], game: 'BelotteGame') -> 'Cards':
        return self.strategy.pick_play(hand, game)

    def first_choice(self, game) -> bool:
        return self.strategy.first_choice(game)

    def second_choice(self, game) -> str:
        return self.strategy.second_choice(game)


class Winner:
    def __init__(self, player: 'Player', card: 'Cards'):
        self.player = player
        self.card = card
        self.suit = self.card.get_suit()
        self.team = self.player.get_team()

    def get_team(self) -> int:
        return self.team

    def get_player(self) -> 'Player':
        return self.player

    def get_card(self) -> 'Cards':
        return self.card

    def get_suit(self) -> str:
        return self.get_card().get_suit()

    def get_score(self) -> str:
        return self.get_card().get_score()


def define_players():
    return [Player(input("Enter Name "), 0, "1", RealBelotteStrategy),
            Player("Bot1", 1, "2", RandomBelotteStrategy),
            Player("Bot2", 0, "3", RandomBelotteStrategy),
            Player("Bot3", 1, "4", RandomBelotteStrategy)]
