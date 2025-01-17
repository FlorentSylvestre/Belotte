from Cards import generate_32_card_deck
from Constante import WIN_SCORE
from Game_logic import *
from player import define_players
from rules import *


def main():
    end_game = False
    score_global: dict[int, int] = {0: 0, 1: 0}
    GUI = GUIBelotte()
    if not GUI.user_prompt("menu"):
        quit()

    playerstate = BelotePlayerInfos(define_players())
    deck = BeloteDeck(generate_32_card_deck())
#   deck.shuffle_deck()

    while not any(score_global[x] >= WIN_SCORE for x in score_global) and not end_game:
        board = BelotteBoardInfos()
        new_round = BelotteGame(board, playerstate, deck, GUI)
        result, deck = new_round.run_round()
        if result is not None:
            score_global = {x: (score_global[x] + result[x]) for x in result}
        end_game = GUI.user_prompt("stop_game")


if __name__ == "__main__":
    main()
