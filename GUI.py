import os

from Cards import BeloteDeck, Cards
from Constante import CARD_PLOT_STRING, OFFSET, PLAYER_ORIENTATION, CARD_PLOT_COORD, CARD_CHAR, SYSTEM_CLEAR, \
    CARD_CHAR_PLAYABLE


def quit_game() -> bool:
    os.system("cls")
    stop_game = ""
    while stop_game.capitalize() not in ["Y", "N"]:
        stop_game: str = input(f"do you to keep playing? Y/N ")
    return True if stop_game.capitalize() == "N" else False


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


class GUI:
    def __init__(self, grid=init_grid_belotte()):
        self.grid = grid

    def get_grid(self):
        return self.grid

    @staticmethod
    def get_card_coord(card: 'Cards') -> tuple[int, int]:
        where = card.get_loc()
        if where == "deck":
            return CARD_PLOT_COORD["deck"]
        if where == "flipped":
            return CARD_PLOT_COORD["flipped"]

        who = card.get_pos()
        orientation = PLAYER_ORIENTATION[who]
        explicit = "dummy"
        if who == '1' or where == "played":
            explicit = "real"
        return CARD_PLOT_COORD["_".join([explicit, orientation, where, str(who)])]

    @staticmethod
    def get_card_str(card: 'Cards') -> str:
        explicit = "dummy"
        orientation = PLAYER_ORIENTATION[card.get_pos()]
        if card.get_pos() == "1" or card.get_loc() in ["played", "flipped"]:
            explicit = "real"

        return CARD_PLOT_STRING[explicit + "_" + orientation]

    def print_grid(self):
        print("\n".join(["".join(x) for x in self.grid]))

    def reinitialize_grid(self):
        self.grid = init_grid_belotte()

    def parse_string(self, cardstring: str, cardpos: tuple[int, int],
                     offset: list[int, int] = (0, 0)) -> None:

        offset = (offset[0] + cardpos[0], offset[1] + cardpos[1])
        cardstr = cardstring.split(".")

        for x, y, symbol in [cardstr[i:i + 3] for i in range(0, len(cardstr), 3)]:
            self.grid[int(x) + offset[0]][int(y) + offset[1]] = symbol

    def show_value(self, card: 'Cards', count: int, cardpos: tuple[int, int],
                   offset: list[int, int] = [0, 0]) -> None:

        offset = [offset[0] + cardpos[0], offset[1] + cardpos[1]]
        orientation = PLAYER_ORIENTATION[card.get_pos()]

        value = card.get_value()
        x, y = (2, 3) if orientation == "v" else (1, 4)

        for i in range(len(value)):
            self.grid[offset[0] + x][offset[1] + y - len(value) + i] = value[i:i + 1]

        if card.get_legit():
            if card.get_pos() == "1" and card.get_loc() == "hand":
                self.grid[offset[0] + 5][offset[1] + 3] = str(count)
            self.grid[offset[0] + x][offset[1] + y + 1] = CARD_CHAR_PLAYABLE[card.get_suit()]
        else:
            self.grid[offset[0] + x][offset[1] + y + 1] = CARD_CHAR[card.get_suit()]

    def update_grid(self, deck: BeloteDeck):
        offset = {'1': [0, 0], '2': [0, 0], '3': [0, 0], '4': [0, 0]}
        self.reinitialize_grid()
        count_player1 = -1
        for card in deck:
            if card.get_loc() == "deck":
                continue

            card_string = self.get_card_str(card)
            card_coord = self.get_card_coord(card)

            if card.get_loc() == "flipped":
                self.parse_string(card_string, card_coord)
                self.show_value(card, count_player1, card_coord)
                continue

            if card.get_loc() == "played":
                self.parse_string(card_string, card_coord)
                self.show_value(card, count_player1, card_coord)
                continue

            self.parse_string(card_string, card_coord, offset[str(card.get_pos())])

            if card.get_pos() == "1":
                if card.get_legit():
                    count_player1 += 1
                self.show_value(card, count_player1, card_coord, offset[str(card.get_pos())])

            if card.get_pos() in ["1", "3"]:
                offset[str(card.get_pos())][0] += OFFSET["v"][0]
                offset[str(card.get_pos())][1] += OFFSET["v"][1]

            if card.get_pos() in ["2", "4"]:
                offset[str(card.get_pos())][0] += OFFSET["h"][0]
                offset[str(card.get_pos())][1] += OFFSET["h"][1]

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
