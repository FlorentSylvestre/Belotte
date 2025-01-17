from typing import Protocol, Optional, Callable, TYPE_CHECKING, Tuple

if TYPE_CHECKING:
    from player import Player
    from Cards import Cards
    from Game_logic import BelotteGame


class CardState(Protocol):
    loc: str
    player: Optional["Player"]
    pos: Optional[Tuple[int, int]]
    image: Optional[str]

    @staticmethod
    def play_card(card: 'Cards', player: Optional['Player'] = None) -> None:
        ...


class Strategy(Protocol):
    first_choice: Callable
    second_choice: Callable
    pick_play: Callable


class GameState(Protocol):
    @staticmethod
    def run_game(game: "BelotteGame") -> None:
        ...
