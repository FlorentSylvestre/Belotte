import os
from typing import Optional

from Cards import BeloteDeck, Cards
from Constante import CARD_PLOT_STRING, OFFSET, PLAYER_ORIENTATION, CARD_PLOT_COORD, CARD_CHAR, SYSTEM_CLEAR, \
    CARD_CHAR_PLAYABLE, WIN_SCORE, INIT_OFFSET


def init_grid_belotte() -> list[list[str]]:
    layout = []
    for x in range(40):
        layout.append([" "] * 95)
    layout[0] = ["_"] * 95
    layout[5] = ["_"] * 95
    layout[32] = ["_"] * 95
    layout[39] = ["_"] * 95
    for i in range(1, len(layout)):
        layout[i][0] = "|"
        layout[i][7] = "|"
        layout[i][87] = "|"
        layout[i][94] = "|"
    return layout


# TODO: separate score and GUI
# TODO: add trump and taking team infos
# TODO: ask about handling new game?
# TODO: add function about quiting anytime
# TODO: add stopping time at the right place (GUI.pause method ?)
# TODO: separate GUI in menu / game / prompt?

class GUIBelotte:

    def __init__(self):
        self.offset = INIT_OFFSET.copy()
        self.shift_offset(1, "v")
        self.grid = init_grid_belotte()
        self.count_player1 = -1

    @staticmethod
    def get_card_coord(card: 'Cards') -> tuple[int, int]:
        """ Fetch grid postion for a card
        or the starting point of the player's hand in not in play"""

        where = card.get_loc()
        if where not in ["deck", "flipped"]:
            who = card.get_pos()
            orientation = PLAYER_ORIENTATION[who]
            string_type = "real" if (who == '1' or where == "played") else "dummy"
            return CARD_PLOT_COORD["_".join([string_type, orientation, where, str(who)])]

        return CARD_PLOT_COORD[where]

    def select_offset(self, card: Cards):
        if card.get_loc() == "hand":
            return self.offset[card.get_pos()]

        return self.offset[card.get_loc()]

    def compute_card_pos(self, card: 'Cards'):
        offset = self.select_offset(card)
        cardpos = self.get_card_coord(card)
        return offset[0] + cardpos[0], offset[1] + cardpos[1]

    @staticmethod
    def get_card_str(card: 'Cards', orientation: str) -> str:
        """" Determines which reference string is need to represent a card
        based on its position on the board"""

        string_type = "real" if (card.get_pos() == "1" or card.get_loc() in ["played", "flipped"]) else "dummy"
        return CARD_PLOT_STRING[string_type + "_" + orientation]

    def add_card_to_grid(self, cardstring: str, cardpos: tuple[int, int]) -> None:
        cardstr = cardstring.split(".")
        for x, y, symbol in [cardstr[i:i + 3] for i in range(0, len(cardstr), 3)]:
            self.grid[int(x) + cardpos[0]][int(y) + cardpos[1]] = symbol

    def show_value(self, card: 'Cards', cardpos: tuple[int, int], orientation: str) -> None:
        """We need to display card values instead of blank card for played cards, flipped cards and player's hand
        This method adds card value and suit to the grid"""

        # Need to know if value in one or 2 char long
        value = card.value

        # Card width / length depends on its orientation (vertical or horizontal)
        width, length = (2, 3) if orientation == "v" else (1, 4)

        # This loop add all card value chars to the grid
        for i in range(len(value)):
            # Adjust printing when card value is more than one character
            self.grid[cardpos[0] + width][cardpos[1] + length - len(value) + i] = value[i:i + 1]

        if card.legit:
            self.grid[cardpos[0] + width][cardpos[1] + length + 1] = CARD_CHAR_PLAYABLE[card.suit]
        else:
            self.grid[cardpos[0] + width][cardpos[1] + length + 1] = CARD_CHAR[card.suit]

    def print_player_option(self, cardpos: tuple[int, int]) -> None:
        """Print the playable options for human player"""
        self.grid[cardpos[0] + 5][cardpos[1] + 3] = str(self.count_player1)

    def shift_offset(self, pos: Optional[int], orientation: str) -> None:
        if pos is None:
            return None
        self.offset[str(pos)] = [self.offset[str(pos)][0] + OFFSET[orientation][0],
                                 self.offset[str(pos)][1] + OFFSET[orientation][1]]

    def update_grid(self, deck: BeloteDeck):

        # Reinitialize the grid caracteristic
        self.reinitialize_grid()

        # Update each card position on the grid
        for card in deck:
            if card.get_loc() == "deck":
                continue

            # Gather card representation and grid position
            player = card.get_pos()
            orientation = PLAYER_ORIENTATION[player]
            card_string = self.get_card_str(card, orientation)
            card_coord = self.compute_card_pos(card)

            # print("Updating:")
            # print(player)
            # print(card)
            # print(orientation)
            # print(self.select_offset(card))
            # print(card_coord)
            # print("")

            # Add card layout to the grid
            self.add_card_to_grid(card_string, card_coord)

            # Played or flipped card values can be seenY
            if card.get_loc() == "flipped" or card.get_loc() == "played" or player == "1":
                self.show_value(card, card_coord, orientation)

            # Print First player legal moves and card values
            if card.get_pos() == "1" and card.legit:
                self.count_player1 += 1
                self.print_player_option(card_coord)

            # Updates offset for correct card alignement in hand

            if card.get_loc() == "hand":
                self.shift_offset(player, orientation)

    def reinitialize_grid(self):
        self.grid = init_grid_belotte()
        self.offset = INIT_OFFSET.copy()
        self.count_player1 = -1
        print(self.offset)
        print(INIT_OFFSET)

    def print_grid(self):
        print("\n".join(["".join(x) for x in self.grid]))

    @staticmethod
    def prompt_first_pick() -> str:
        print("Do you want to play this card? Y/N\n")
        return input()

    @staticmethod
    def prompt_second_pick(choice: list[str]) -> str:
        print("Do you want to play another suit? \n")
        for suit, pos in enumerate(choice):
            print(f"{suit}: {pos}")
        return input()

    @staticmethod
    def prompt_play_card() -> str:
        print("Which card do you want to play? (input Number)")
        return input()

    @staticmethod
    def clear_screen():
        os.system(SYSTEM_CLEAR[os.name])

    @staticmethod
    def quit_game() -> bool:
        os.system("cls")
        stop_game = ""
        while stop_game.capitalize() not in ["Y", "N"]:
            stop_game: str = input(f"do you to keep playing? Y/N ")
        return False if stop_game.capitalize() == "N" else True

    @staticmethod
    def print_menu():
        print("BELOTTE GAME")
        print(f"First team to {WIN_SCORE} wins")
        print("option to print rules will be shortly implemented, i'm lazy A-F")
        print("Bisous bisous")
        print("Do you wanna play? Y/N ")
        play = ""
        while play not in ["Y", "N"]:
            play = input().capitalize()
        return play
