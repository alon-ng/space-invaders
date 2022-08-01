class HealthBar:
    def __init__(self, stdscr):
        self.health = 100
        self.stdscr = stdscr

    def hit(self, damage):
        if (self.health - damage < 0):
            self.health = 0
        else:
            self.health -= damage

    def add(self, addition):
        if (self.health + addition > 100):
            self.health = 100
        else:
            self.health += addition

    def draw(self):
        h, w = self.stdscr.getmaxyx()

        self.stdscr.addstr(h - 3, 5, "HP")
        self.stdscr.addstr(h - 2, 5, "█" * (self.health // 5))
        self.stdscr.addstr(h - 2, 26, str(self.health))
