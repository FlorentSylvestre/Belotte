from typing import TYPE_CHECKING

from Constante import TOTAL_SCORE_ROUND

if TYPE_CHECKING:
    from Cards import Cards
    from Game_logic import BelotteGame


def is_round_won(score: int):
    return score >= (TOTAL_SCORE_ROUND / 2)


def is_capot(score: int):
    return score == 0


class BelotteScore:
    def __init__(self):
        self.score: int = 0

    def update(self, turn: list["Cards"]) -> None:
        for card in turn:
            self.score += card.score
        print(self.score)

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
            print({game.has_taken.team: self.score,
                    (1 - game.has_taken.team): TOTAL_SCORE_ROUND - self.score})
            return {game.has_taken.team: self.score,
                    (1 - game.has_taken.team): TOTAL_SCORE_ROUND - self.score}

        return {game.has_taken.team: 0,
                (1 - game.has_taken.team): TOTAL_SCORE_ROUND}
