from Cards import Generate32CardDeck
from GUI import quit_game
from Game_logic import *
from rules import *
from Constante import WIN_SCORE


def main():
    end_game = False
    score_global: dict[int, int] = {0: 0, 1: 0}
    playerstate = BelotePlayerState()
    deck = BeloteDeck(Generate32CardDeck())
    deck.shuffle_deck()

    while not any(score_global[x] >= WIN_SCORE for x in score_global) and not end_game:
        board = BelotteBoardState()
        new_round = BelotteGame(board, playerstate, deck)
        result, deck = new_round.run_round()
        if result is not None:
            score_global = {x: (score_global[x] + result[x]) for x in result}

        end_game = quit_game()


if __name__ == "__main__":
    main()

# TODO: add a waiting period at the end of a round to check board
