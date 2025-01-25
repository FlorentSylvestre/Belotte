from typing import Optional
from Cards import Cards
from playerbelotte import PlayerBelotte, Winner
from rules import is_winner_belotte


class BelotePlayerInfos:

    def __init__(self, players):
        self.players: Optional[list[PlayerBelotte]] = players
        self.dealer: PlayerBelotte = players[3]  # TODO randomize first dealer later, is fixed for testing
        self.reorder(self.players.index(self.dealer) + 1)

    def reorder(self, p: int | PlayerBelotte) -> None:
        k = p if isinstance(p, int) else self.players.index(p)
        self.players = self.players[k:] + self.players[:k]

    def shift_dealer(self) -> None:
        """ Set the player left to the last dealer as the new dealer"""
        index = self.players.index(self.dealer)
        if index == 4:  # Handle when previous dealer is last on list
            index = 0

        self.reorder(index)
        self.dealer = self.players[index]

    def get_partner(self, player) -> PlayerBelotte:
        for p in self.players:
            if player.team == p.team and player.name != p.name:
                return p

    def __getitem__(self, item) -> PlayerBelotte | list[PlayerBelotte]:
        return self.players[item]


class BelotteBoardInfos:
    def __init__(self):
        self.current_Fold: list[Cards] = []
        self.played_fold: list[list[Cards]] = []
        self.asked_suit: Optional[str] = None
        self.winner: Optional[Winner] = None
        self.trump: Optional[str] = None

    def add_played_card(self, card: Cards) -> None:
        self.current_Fold.append(card)

    def archive_fold(self) -> None:
        for card in self.current_Fold:
            card.reinitialize()
        self.played_fold.append(self.current_Fold)
        self.current_Fold = []

    def update_winner(self, player: PlayerBelotte) -> None:
        if is_winner_belotte(self):
            self.winner = Winner(player, self.current_Fold[-1])

    def get_winner_team(self) -> Optional[int]:
        if self.winner is not None:
            return self.winner.team


