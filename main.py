"""
This module starts the Wiki Piki application.
Provides instruction to the user, and then they can start the game!
"""

import utils

def main() -> None:
    """
    Starts game on user command.
    Plays game.
    When game is done:
        If 'y', it launches the quiz gameplay.
        If 'n', it exits the program.
        If invalid input re-run main
    """

    utils.show_banner()

    # print("""Answer questions! Score points,
    # And if you're among the most clever, join the legendary...
    #     ┓ ┏┓┏┓┳┓┏┓┳┓┳┓┏┓┏┓┳┓┳┓╻
    #     ┃ ┣ ┣┫┃┃┣ ┣┫┣┫┃┃┣┫┣┫┃┃┃
    #     ┗┛┗┛┛┗┻┛┗┛┛┗┻┛┗┛┛┗┛┗┻┛•""")

    utils.print_all_commands()
    while True:
        try:
            command = input("Choose a command: ").lower()
            if command not in utils.DISPATCH.keys():
                raise KeyError
            utils.DISPATCH[command]()
        except KeyError:
            print("❗ Error - invalid command ❗")


if __name__ == "__main__":
    main()
