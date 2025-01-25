import dataclasses
from typing import Protocol, Optional, Callable, TYPE_CHECKING, Tuple

if TYPE_CHECKING:
    from Cards import Cards
    from Game_data import BelotteGame

type prompter = dict["str", tuple[str, Callable]]


class Player(Protocol):
    name: str  # Useless for now
    team: int  # 0 or 1, shared by team member
    pos: str  # position of the board : 1,2,3 or 4. 1 is player, clockwise rotation
    strategy: "Strategy"


class CardState(Protocol):
    loc: str
    player: Optional["Player_belotte"]
    pos = Tuple[int, int]
    visible = bool
    size = str
    orientation = "v"

    @staticmethod
    def play_card(card: 'Cards', player: Optional['Player_belotte'] = None) -> None:
        ...


class Strategy(Protocol):
    first_choice: Callable
    second_choice: Callable
    pick_play: Callable


class GameState(Protocol):
    @staticmethod
    def run_game(game: "BelotteGame") -> None:
        ...
