import time
from enum import Enum
from typing import List
from GameManual import GameManual

MAIN_LABEL = """
              .d8888. d8888b.  .d8b.   .o88b. d88888b              
              88'  YP 88  `8D d8' `8b d8P  Y8 88'                  
              `8bo.   88oodD' 88ooo88 8P      88ooooo              
                `Y8b. 88~~~   88~~~88 8b      88~~~~~              
              db   8D 88      88   88 Y8b  d8 88.                  
              `8888Y' 88      YP   YP  `Y88P' Y88888P              
                                                                   
                                                                   
d888888b d8b   db db    db  .d8b.  d8888b. d88888b d8888b. .d8888. 
  `88'   888o  88 88    88 d8' `8b 88  `8D 88'     88  `8D 88'  YP 
   88    88V8o 88 Y8    8P 88ooo88 88   88 88ooooo 88oobY' `8bo.   
   88    88 V8o88 `8b  d8' 88~~~88 88   88 88~~~~~ 88`8b     `Y8b. 
  .88.   88  V888  `8bd8'  88   88 88  .8D 88.     88 `88. db   8D 
Y888888P VP   V8P    YP    YP   YP Y8888D' Y88888P 88   YD `8888Y' 
 """

PAUSED_LABEL = """
d8888b.  .d8b.  db    db .d8888. d88888b d8888b. 
88  `8D d8' `8b 88    88 88'  YP 88'     88  `8D 
88oodD' 88ooo88 88    88 `8bo.   88ooooo 88   88 
88~~~   88~~~88 88    88   `Y8b. 88~~~~~ 88   88 
88      88   88 88b  d88 db   8D 88.     88  .8D 
88      YP   YP ~Y8888P' `8888Y' Y88888P Y8888D' 
"""


class GameDifficulty(Enum):
    EASY = 1
    NORMAL = 2
    HARD = 3


class Menu:
    row = 0
    done = False
    difficulty = GameDifficulty.EASY

    def __init__(self, options, stdscr, curses, highscore=-1) -> None:
        self.options = options
        self.stdscr = stdscr
        self.curses = curses
        self.highscore = highscore
        curses.init_pair(1, 240, curses.COLOR_BLACK)
        curses.init_pair(2, 255, curses.COLOR_BLACK)

    def start(self) -> str:
        self.curses.curs_set(0)
        self.print_menu()
        while not self.done:
            self.print_menu()
            key = self.stdscr.getch()
            if key == self.curses.KEY_UP and self.row > 0:
                self.row -= 1
            elif key == self.curses.KEY_DOWN and self.row < len(self.options) - 1:
                self.row += 1
            elif key == self.curses.KEY_ENTER or key in [10, 13]:
                selected = self.options[self.row]
                if (selected == "Play"):
                    counter = 3
                    while (counter > 0):
                        self.print_center(
                            "Game starts in {}...".format(counter))
                        time.sleep(1)
                        counter -= 1
                    self.print_center(
                        "Have fun!")
                    time.sleep(1)
                    self.done = True
                elif (selected == "Resume"):
                    counter = 3
                    while (counter > 0):
                        self.print_center(
                            "Game resumes in {}...".format(counter))
                        time.sleep(1)
                        counter -= 1
                    self.print_center(
                        "Have fun!")
                    time.sleep(1)
                    self.done = True
                elif (selected == "Difficulty"):
                    self.difficulty = GameDifficulty(
                        1 if self.difficulty.value + 1 > 3 else self.difficulty.value + 1)
                    continue
                elif (selected == "Infromation"):
                    infromation = GameManual(self.stdscr)
                    infromation.show()
                    continue
                return selected
            time.sleep(0.01)

    def print_menu(self):
        self.stdscr.clear()

        h, w = self.stdscr.getmaxyx()
        if (self.highscore != -1):
            self.stdscr.addstr(
                h - 2, 2, "Highscore: {}".format(self.highscore))
            self._print_multi_line(
                MAIN_LABEL, w // 2 - len(MAIN_LABEL.split('\n')[2]) // 2, 5)
        else:
            self._print_multi_line(
                PAUSED_LABEL, w // 2 - len(PAUSED_LABEL.split('\n')[2]) // 2, 10)
        for i, row in enumerate(self.options):
            if (row == "Difficulty"):
                row += ": {}".format(self.difficulty.name)
            x = w // 2 - len(row) // 2
            y = h // 2 - len(self.options) // 2 + i
            if i == self.row:
                self.stdscr.attron(self.curses.color_pair(2))
                self.stdscr.addstr(y, x, row)
                self.stdscr.attroff(self.curses.color_pair(2))
            else:
                self.stdscr.attron(self.curses.color_pair(1))
                self.stdscr.addstr(y, x, row)
                self.stdscr.attroff(self.curses.color_pair(1))
        self.stdscr.refresh()

    def print_center(self, text):
        self.stdscr.clear()
        h, w = self.stdscr.getmaxyx()
        x = w // 2 - len(text) // 2
        y = h // 2
        self.stdscr.addstr(y, x, text)
        self.stdscr.refresh()

    def _print_multi_line(self, str: List[str], x, y):
        for i, line in enumerate(str.split('\n')[1:-1]):
            self.stdscr.addstr(y + i, x, line)
