from Protocols import prompter


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


def user_prompt(name: str, *args) -> str | Cards | bool:
    print(prompt_belote[name][0])
    return prompt_belote[name][1]() if not args else prompt_belote[name][1](*args)