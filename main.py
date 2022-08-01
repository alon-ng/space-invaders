import curses
from Menu import Menu
from GameController import GameController

TICKS_PER_SECOND = 30

# Checks if the terminal size in the appropriate range and won't let the player
# play the game unless he resize the window size accordingly


def check_for_terminal_size(stdscr):
    while True:
        stdscr.clear()

        h, w = stdscr.getmaxyx()
        if (h < 50):
            print_center(stdscr, "Please increase the window height", -1)
        elif (w < 100):
            print_center(stdscr, "Please increase the window width", -1)
        elif (h > 60):
            print_center(stdscr, "Please decrease the window height", -1)
        elif (w > 140):
            print_center(stdscr, "Please decrease the window width", -1)
        else:
            break
        print_center(stdscr, "Ideal size is 100x50 - 140x60")
        print_center(stdscr, "You window size: {}x{}".format(w, h), 1)
        stdscr.refresh()


def print_center(stdscr, text, offset=0):
    h, w = stdscr.getmaxyx()
    x = w // 2 - len(text) // 2
    y = h // 2 + offset
    stdscr.addstr(y, x, text)


def main(stdscr):
    curses.curs_set(0)
    stdscr.nodelay(1)
    check_for_terminal_size(stdscr)
    highscore = 0

    while True:
        # Created the main menu of the game
        menu = Menu(["Play", "Difficulty", "Infromation", "Exit"],
                    stdscr, curses, highscore)
        state = menu.start()
        difficulty = menu.difficulty

        if (state == "Exit"):
            exit(0)
        elif (state == "Play"):
            # Starts the game
            game_controller = GameController(
                stdscr, curses, TICKS_PER_SECOND, difficulty)
            score = game_controller.start()
            highscore = max(score, highscore)


curses.wrapper(main)
