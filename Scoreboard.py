class Scoreboard:
    def __init__(self, stdscr):
        self.stdscr = stdscr
        self.score = 0

    def draw(self):
        w = self.stdscr.getmaxyx()[1]
        print_string = "Score: {}".format(str(self.score))
        self.stdscr.addstr(2, w // 2 - len(print_string) // 2, print_string)

    def add(self, n):
        self.score += n
