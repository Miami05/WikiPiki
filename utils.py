import os
import sys
import game
import highscores
import time
import ascii_art
from rich.panel import Panel
from rich.console import Console
from rich.align import Align
from rich.table import Table
from rich.rule import  Rule
from rich.text import Text


os.environ.setdefault("TERM", "xterm-256color")
console = Console()


def quit_cli() -> None:
    """Quits the CLI."""
    print("Thanks for playing, goodbye!")
    sys.exit(0)


def print_all_commands() -> None:
    """Prints all commands in dispatch with colors."""
    console.print("[bold magenta]Main Menu:[/bold magenta]")
    for key in DISPATCH:
        console.print(f"\t→ [bold yellow]{key}[/bold yellow]")
    console.print()


DISPATCH = {
    "start": game.start_gameplay,
    "leaderboard": highscores.print_all_scores,
    "quit": quit_cli
}


def loading_spinner(task, function, *args, **kwargs):
    """Shows a loading spinner for the function(*args, **kwargs) """
    with console.status(f"[bold green]{task}", spinner="bouncingBall"):
        result = function(*args, **kwargs)
    console.print(f"✅ {task} done!", style="bold green")
    return result


def clear_screen():
    """ clears the console for better game view """
    os.system('cls' if os.name == 'nt' else 'clear')


def show_banner():
    """Shows WIKI PIKI banner when starting the app"""
    BANNER = ascii_art.banner
    banner_panel = Panel(
        Align.center(BANNER.strip(), vertical="middle"),
        border_style="magenta",
        padding=(1, 6),
        title="W I K I   P I K I",
        title_align="center",
    )
    console.clear()
    console.print(banner_panel)
    console.print(ascii_art.GAME_INTRO, justify="left")

def print_correct(answer, streak=0):
    """Formatting for the correct answer"""
    console.print(
        Panel.fit(f"✅ Correct! The answer is [bold green]{answer}[/bold green]",
                  border_style="green"
                  )
    )
    if streak >= 3:
        console.print(
            Panel.fit(f"🔥 You're on fire! Streak: {streak}! 🔥",
                      border_style="red"
                      )
        )
    time.sleep(1)


def print_incorrect(answer, streak=0):
    """Formatting for the incorrect answer"""
    console.print(
        Panel.fit(f"❌ Wrong! The correct answer was [bold red]{answer}[/bold red]",
                  border_style="red"
                  )
    )
    if streak >= 3:
        console.print(
            Panel.fit(f"🥶 You lost your streak of {streak}! 🥶",
                      border_style="blue"
                      )
        )
    time.sleep(1)


def print_question(item):
    """format and print a question with options."""
    question_text = Text(item["question"], style="bold cyan")
    question_panel = Panel.fit(question_text, title="Question", border_style="magenta")
    console.print()
    console.print(question_panel, justify="center")
    console.print()

    options_table = Table(show_header=False, box=None, padding=(0, 2))
    options_table.add_column("Key", justify="center", style="bold yellow")
    options_table.add_column("Option", style="white")

    keys = []
    for key, value in item["options"].items():
        options_table.add_row(key, value)
        keys.append(key)

    console.print(options_table, justify="center")
    console.print()
    return keys
