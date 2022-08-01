class Projectile:

    def __init__(self, x, y, speed, parent, stdscr) -> None:
        self.x = x
        self.y = y
        self.speed = speed
        self.parent = parent
        self.stdscr = stdscr
        self.symbol = "¿" if (type(self.parent).__name__ == "Player") else "¥"

    def draw(self):
        self.y += self.speed
        self.stdscr.addstr(self.y, self.x, self.symbol)

    def in_bound(self):
        h, w = self.stdscr.getmaxyx()
        return self.x < w and self.x > 0 and self.y < h - 4 and self.y > 0

    def is_intersecting(self, entity):
        return self.x >= entity.x and self.x < entity.x + 5 and self.y >= entity.y and self.y < entity.y + 2
