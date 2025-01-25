import os
from Protocols import prompter
from Cards import BeloteDeck, Cards
from Constante import PLAYER_ORIENTATION, CARD_CHAR, SYSTEM_CLEAR, \
    CARD_CHAR_PLAYABLE, WIN_SCORE


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


def check_options(options: list[str]) -> str:
    s = ""
    while s.capitalize() not in options:
        s = input()
    return s


def pr_yes_or_no() -> bool:
    yes = ["Y", "O", "YES", "OUI"]
    no = ["N", "NO", "NON"]
    return check_options(yes + no) in yes


def pr_second_pick(options: list[str]) -> str:
    for choice, pos in enumerate(options):
        print(f"{choice}: {pos}")
    selected = check_options([str(x) for x in range(len(options))])
    return options[int(selected)]


def pr_play_card(playable: list['Cards']) -> Cards:
    pick = check_options([str(x) for x in range(len(playable))])
    return playable[int(pick)]


prompt_belote: prompter = {"menu": (f"""
BELOTTE GAME
First team to {WIN_SCORE} wins
option to print rules will be shortly implemented, i'm lazy A-F
Do you wanna play?
Y / N
""", pr_yes_or_no),
                           "first_pick": ("Do you want to play this card?\n Y/N", pr_yes_or_no),
                           "second_pick": ("Do you want to play another suit?", pr_second_pick),
                           "play_card": ("Which card do you want to play? (input Number)", pr_play_card),
                           "stop_game": ("do you to keep playing? Y/N", pr_yes_or_no)}


# TODO: separate score and GUI
# TODO: add trump and taking team infos
# TODO: ask about handling new game?
# TODO: add function about quiting anytime
# TODO: add stopping time at the right place (GUI.pause method ?)


class GUIBelotte:

    def __init__(self, coord_sys: dict[str: int], str_card: dict[str: str], offset: dict[str: tuple[int, int]]):
        self.grid = init_grid_belotte()
        self.count_option = 0
        self.coord = coord_sys
        self.card_str = str_card
        self.offset = offset

    def get_card_coord(self, c: 'Cards') -> tuple[int, int]:
        """ Fetch grid postion for a card"""

        if c.state.loc == "flipped":
            return self.coord["flipped"]

        fetch = "_".join([c.state.size, c.state.orientation,
                          c.state.loc, c.get_pos()])

        return (self.coord[fetch][0] + self.offset[c.state.orientation][0] * c.state.pos[0],
                self.coord[fetch][1] + self.offset[c.state.orientation][1] * c.state.pos[0])

    def get_card_str(self, c: 'Cards') -> str:
        return self.card_str[c.state.size + "_" + c.state.orientation]

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
        self.grid[cardpos[0] + 5][cardpos[1] + 3] = str(self.count_option)

    def update_grid(self, deck: BeloteDeck):
        self.reinitialize_grid()
        # Update each card position on the grid
        for card in deck:
            if card.get_loc() == "deck":
                continue
            # Gather card representation and grid position
            player = card.get_pos()
            orientation = PLAYER_ORIENTATION[player]
            card_string = self.get_card_str(card)
            card_coord = self.get_card_coord(card)

            # Add card layout to the grid
            self.add_card_to_grid(card_string, card_coord)

            # Played or flipped card values can be seenY
            if card.state.visible:
                self.show_value(card, card_coord, orientation)

            # Print First player legal moves and card values
            if card.get_pos() == "1" and card.get_loc() == "hand" and card.legit:
                self.print_player_option(card_coord)
                self.count_option += 1

    def reinitialize_grid(self):
        self.grid = init_grid_belotte()
        self.count_option = 0

    def print_grid(self):
        print("\n".join(["".join(x) for x in self.grid]))

    @staticmethod
    def user_prompt(name: str, *args) -> str | Cards | bool:
        print(prompt_belote[name][0])
        return prompt_belote[name][1]() if not args else prompt_belote[name][1](*args)

    @staticmethod
    def clear_screen():
        os.system(SYSTEM_CLEAR[os.name])
