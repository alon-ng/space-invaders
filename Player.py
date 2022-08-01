from math import floor
import time
from Projectile import Projectile


class Player:
    prev_shoot_time: float

    def __init__(self, x, difficulty, stdscr) -> None:
        self.x = x
        self.y = stdscr.getmaxyx()[0] - 7
        self.stdscr = stdscr
        self.prev_shoot_time = time.time()
        self.PLAYER_SPEED = (4 - difficulty.value) / 2
        self.FIRE_RATE_DELAY = difficulty.value / 10

    def move(self, dir):
        w = self.stdscr.getmaxyx()[1]
        dx = self.PLAYER_SPEED if dir > 0 else -self.PLAYER_SPEED
        if (self.x + dx < w - 7 and self.x + dx >= 3):
            self.x += dx

    def draw(self):
        self.stdscr.addstr(self.y, floor(self.x + 1), "/~\\")
        self.stdscr.addstr(self.y + 1, floor(self.x), "/___\\")
        self.stdscr.addstr(self.y + 2, floor(self.x + 1), "$ $")

    def shoot(self):
        if (self.prev_shoot_time < time.time() - self.FIRE_RATE_DELAY):
            self.prev_shoot_time = time.time()
            return Projectile(floor(self.x) + 2, self.y - 1, -1, self, self.stdscr)
        return False
