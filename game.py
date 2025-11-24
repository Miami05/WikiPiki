"""
Game Module
Handles:
- Creating quiz questions from Wikipedia using AI
- Running the gameplay loop
- Collecting user answers
- Scoring the player
"""
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

import utils
import wikipedia_client
import questions_generator
import highscores
import main

console = Console()

PLAYER_1_NAME = "[bold red]Player 1 🔴[/bold red]"
PLAYER_2_NAME = "[bold blue]Player 2 🔵[/bold blue]"
SINGLE_PLAYER_NAME = "[bold gold]Player 🟡[/bold gold]"
NUMBER_OF_CATEGORIES = 5
ALL_DIFFICULTIES = True
STREAK_START = 3
NUMBER_OF_QUESTIONS = 10

def show_categories(categories):
    """Display categories in a cool (table) game-style way."""
    utils.console.print("\n🎮 [bold magenta]Choose Your Category[/bold magenta] 🎮\n")
    table = Table(padding=(0,2),box=None)
    table.add_column("No.", justify="center", style="bold cyan")
    table.add_column("Category", justify="left", style="bold yellow")

    for i, cat in enumerate(categories, 1):
        table.add_row(str(i), cat)

    utils.console.print(table)

def summarize_article():
    """
    Asks the user to select a Wikipedia category.
    Return a summarized article.

    Returns:
        str: A summarized Wiki article
    """

    categories = wikipedia_client.get_rand_categories(NUMBER_OF_CATEGORIES)
    if not categories:
        print("❗No articles available.")
        return None

    #format categories in a cool way
    show_categories(categories)

    try:
        choice = int(input("\nEnter the number of your choice: ").strip())
        selected_category = categories[choice - 1]
    except (ValueError, IndexError):
        print("❗ Invalid choice. Try again")

    #recieved summarized article from wikipedia client
    try:
        summarized_article = wikipedia_client.get_summarized_article(selected_category)
        return summarized_article
    except Exception as e:
        print(f"❗failed to summarize article: {e}")
        return None

def generate_questions(article):
    """
    Generates quiz questions from an article.
    Shows a loading spinner while generating questions

    Args:
        article (str): A summarized Wiki article string
    Returns:
        questions list[dict]: List of questions, each with keys:
            - question (str)
            - options (dict[str, str])
            - answer (str)
            - difficulty (str)
            - question_format (str)
    """
    try:
        questions = utils.loading_spinner(
            "Generating Questions 🤓...",
            questions_generator.make_questions,article, NUMBER_OF_QUESTIONS
        )
        return questions
    except Exception as e:
        print(f"❗failed to generate questions: {e}")
        return None

# def select_num_players():
#     """Returns multiplayer if user chooses 'b' loops until the user gets it right"""
#     while True:
#         user_answer = input("\n🎮 Select Mode:\n "
#                                                 "👤  One Player (a)\ 👥  Two Players (b)\n").strip().lower()
#         if len(user_answer) == 1 and user_answer in "ab":
#             return user_answer == "b"
#         else:
#             print("Please select one of the options")

def select_num_players():
    """Return True for multiplayer (b), False for single (a)."""
    # Fancy panel prompt (optional)
    print()
    mode_table = Table.grid()
    mode_table.add_column(justify="center", style="bold")
    mode_table.add_column(justify="left")
    mode_table.add_row("👤", "[bold yellow] One Player[/bold yellow] (a)")
    mode_table.add_row("👥", "[bold yellow] Two Players[/bold yellow] (b)")
    utils.console.print(Panel.fit(mode_table, title="🎮 Select Mode 🎮", border_style="magenta"))

    while True:
        user_answer = console.input("[bold yellow]👉 Select (a/b): [/bold yellow]").strip().lower()
        if user_answer in ("a", "b"):
            return user_answer == "b"
        console.input("[red]❗ Please select one of the options (a/b).[/red]")



# def get_keys_print_question(item):
#     """from question given (item) returns answer keys and prints question nicely"""
#     keys = []
#     question = item['question']
#     print(f"{question}\n")
#     for key in item['options']:
#         print(f"{key} - {item['options'][key]}")
#         keys.append(key)
#     print("\n")
#
#     return keys

def get_valid_answer(player_name, keys):
    """validates answer to be in the given keys"""
    while True:
        utils.console.print(f"{player_name}: Please enter answer: ", end="", style="bold")
        user_answer = input().strip().lower()
        if len(user_answer) == 1 and user_answer in keys:
            return user_answer
        else:
            utils.console.print("❗ Please enter one of the letters", style="bold red")


def check_answer_and_update_score(player_answer, player_score, player_streak, correct_answer):
    """if player answers correctly, increases score and streak, if not loses streak
    returns score and streak"""
    if player_answer == correct_answer:
        player_score += 1
        player_streak += 1
        utils.print_correct(correct_answer, player_streak)
        if player_streak >= STREAK_START:
            player_score += player_streak
    else:
        utils.print_incorrect(correct_answer, player_streak)
        player_streak = 0
    return player_score, player_streak

def play_game(questions, multiplayer):
    """
    Depending on selected mode, plays single/multi user mode.
    Prints each question, and it's options.
    The user answers each question by selecting a or b or c
    If multiple questions answered in a row, increase streak, lost on wrong answer
    Prints final score and if necessary highscore function
    Args:
        questions (list[dict]): A list of questions. Each question is represented as a dictionary
    Returns:
        score (int): Final game Score
    """
    if multiplayer:
        score_a = 0
        score_b = 0
        streak_a = 0
        streak_b = 0

        for item in questions:
            keys = utils.print_question(item)
            player_one_answer = get_valid_answer(PLAYER_1_NAME, keys)
            player_two_answer = get_valid_answer(PLAYER_2_NAME, keys)

            utils.console.print(f"{PLAYER_1_NAME}:", style="bold red")
            score_a, streak_a = check_answer_and_update_score(player_one_answer, score_a, streak_a, item['answer'])

            utils.console.print(f"{PLAYER_2_NAME}:", style="bold blue")
            score_b, streak_b = check_answer_and_update_score(player_two_answer, score_b, streak_b, item['answer'])

            input("Press Enter to continue...")

        utils.console.print(f"{PLAYER_1_NAME} Score: {score_a}", style="bold")
        utils.console.print(f"{PLAYER_2_NAME} Score: {score_b}", style="bold")

        if score_a > score_b:
            utils.console.print(f"{PLAYER_1_NAME} Wins!", style="bold green")
            highscores.check_score_and_save(score_a, PLAYER_1_NAME)
        elif score_b > score_a:
            utils.console.print(f"{PLAYER_2_NAME} Wins!", style="bold green")
            highscores.check_score_and_save(score_b, PLAYER_2_NAME)
        else:
            utils.console.print("Both players had the same score!", style="bold yellow")
            highscores.check_score_and_save(score_a, PLAYER_1_NAME)
            highscores.check_score_and_save(score_b, PLAYER_2_NAME)


    else:
        score = 0
        streak = 0
        for item in questions:
            keys = utils.print_question(item)
            answer = get_valid_answer(SINGLE_PLAYER_NAME, keys)
            score, streak =  check_answer_and_update_score(answer, score, streak, item['answer'])
            input("Press Enter to continue...")
        utils.console.print(f"{SINGLE_PLAYER_NAME} score {score}", style="bold")
        highscores.check_score_and_save(score, SINGLE_PLAYER_NAME)

def start_gameplay():
    """
    Orchestrates the full game:
        Summarize article
        Generate questions
        Play quiz
        Save & display score
    """
    while True:
        multiplayer = select_num_players()
        summarized_article = summarize_article()

        if not summarized_article:
            print("❗No articles available.")
            return

        questions = generate_questions(summarized_article)
        if not questions:
            print("❗No questions available.")
            return
        else:
            utils.clear_screen()

        play_game(questions, multiplayer)


        while True:  # replay input Loop
            replay_input = input("Would you like to replay the game? (y/n)").lower()
            if replay_input.lower() == "y":
                break
            if replay_input.lower() == "n":
                print("Thanks for playing!")
                main.main() #navigates to main() menu
            else:
                print("❗Invalid input. Please try again.")

