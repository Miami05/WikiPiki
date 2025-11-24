import json
import utils

MAX_HIGHSCORES = 10  # called to as HS all over

with open('highscores.json') as json_data:
    HIGHSCORES = json.load(json_data)


def get_valid_name() -> str:
    """
    Validates that: name is 3 letters (no numbers).
    Returns a valid winner_name
    """
    utils.console.print("✨✨ You've got a high score! ✨✨", style="bold magenta")
    while True:
        utils.console.print("📝 Enter your 3 initials (e.g. JHN or ANN): ", end="", style="bold cyan")
        winner_name = input().upper()
        if winner_name.isalpha() and len(winner_name) == 3:
            break
        else:
            utils.console.print("❗ Error! Please enter three letters! ❗", style="bold red")
    return winner_name


def is_in_highscores(score) -> bool:
    """
    Check if the number of scores is less than the maximum, if so add score
    otherwise, check if score is higher than the lower value.
    """
    if len(HIGHSCORES[0]) < MAX_HIGHSCORES:  # set your HS in the constant
        return True
    return score > min(HIGHSCORES[0].values())  # check if score is lower than the lowest score in HS


def print_all_scores() -> None:
    """
    From highscores.json prints every score in order of appearance.
    Returns nothing, used to print all HS in a formatted fashion.
    """
    print()
    utils.console.print("🥇 Highscores:", style="bold yellow")
    for player, score in HIGHSCORES[0].items():
        utils.console.print(f"\t- {player} - {score}", style="bold")

    print()


def save_scores(winner_name, player_score: int) -> None:
    """
    Receives name and score, saves scores:
    clips dictionary if longer than 10.
    """
    new_scores = {
        winner_name: player_score
    }
    with open('highscores.json', 'w') as score_data:
        HIGHSCORES[0].update(new_scores)
        sorted_scores = sorted(HIGHSCORES[0].items(),
                               key=lambda item: item[1], reverse=True)  # sorts scores in order
        HIGHSCORES[0] = dict(sorted_scores[:MAX_HIGHSCORES])
        json.dump(HIGHSCORES, score_data, indent=4)


def check_score_and_save(score, temp_name) -> None:
    """
    If score is to be saved, get valid name, save score, print updated scores.
    """
    if is_in_highscores(score):
        utils.console.print(f"{temp_name}, save your high score!", style="bold magenta")
        name = get_valid_name()
        save_scores(name, score)
        print_all_scores()
