from enum import Enum
from math import floor
from Projectile import Projectile
import time


class AlienType(Enum):
    Squid = 10
    Crab = 20
    Octopus = 30


class Alien:
    def __init__(self, x, y, type, difficulty, stdscr) -> None:
        self.x = x
        self.y = y
        self.type = type
        self.stdscr = stdscr
        self.health = type.value
        # Sets the fire rate of the alien based on the difficulty.
        self.FIRE_RATE_DELAY = 0.5 if difficulty.value == 1 else 0.35 if difficulty.value == 2 else 0.2
        self.prev_shoot_time = time.time()

    def moveX(self, dir):
        self.x += dir

    # Draws the alien to the screen based on the types
    def draw(self):
        if (self.type == AlienType.Squid):
            self.stdscr.addstr(self.y, self.x, "/-1-\\")
            self.stdscr.addstr(self.y + 1, self.x + 1, "| |")
        if (self.type == AlienType.Crab):
            self.stdscr.addstr(self.y, self.x, "/&_&\\")
            self.stdscr.addstr(self.y + 1, self.x + 1, "/2\\")
        if (self.type == AlienType.Octopus):
            self.stdscr.addstr(self.y, self.x, "(+!+)")
            self.stdscr.addstr(self.y + 1, self.x, "/(3)\\")

    def hit(self, damage):
        self.health -= damage
        return self.health

    def shoot(self):
        if (self.prev_shoot_time < time.time() - self.FIRE_RATE_DELAY):
            self.prev_shoot_time = time.time()
            return Projectile(floor(self.x) + 2, self.y + 2, 1, self, self.stdscr)
        return False
