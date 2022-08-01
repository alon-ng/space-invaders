import curses
from math import floor
from random import random
import threading
import time
from Menu import Menu, GameDifficulty
from enum import Enum
from Alien import Alien
from Player import Player
from Animation import Animation
from Levels import LEVELS_LAYOUT
from Scoreboard import Scoreboard
from HealthBar import HealthBar
from Projectile import Projectile
from FlyingLabel import FlyingLabel, LEVEL_LABELS, YOU_DIED_LABEL, YOU_WON_LABEL
from typing import List, Literal
from pynput.keyboard import Key, Listener


class GameLevel(Enum):
    LEVEL1 = 1
    LEVEL2 = 2
    LEVEL3 = 3
    LEVEL4 = 4
    LEVEL5 = 5
    LEVEL6 = 6
    LEVEL7 = 7
    LEVEL8 = 8
    LEVEL9 = 9
    LEVEL10 = 10
    FINISH = 11


class GameState(Enum):
    PLAYING = 1
    PAUSED = 2
    LOADING = 3
    DONE = 4


start_time = time.time()

DEATH_ANIMATION = ["""

, - ,
  *

""", """

_\\ ! /_
 / ! \\

""", """
.\\ , /.
\\     /
/     \\
'/ ' \\'
""", """

 * ' * 
 . , .

"""]


class GameController:
    rotation: int = 0
    level: Enum = GameLevel.LEVEL1
    state: Enum = GameState.LOADING
    keydowns: set[Literal] = set()
    aliens: List[Alien] = []
    projectiles: List[Projectile] = []
    animations: List[Animation] = []
    player: Player
    score: int = 0
    difficulty: GameDifficulty

    def __init__(self, stdscr, curses: curses, ticks_per_second, difficulty) -> None:
        self.stdscr = stdscr
        self.ticks_per_second = ticks_per_second
        self.curses = curses
        self.difficulty = difficulty
        w = self.stdscr.getmaxyx()[1]
        self.player = Player(w // 2, difficulty, stdscr)
        self.scoreboard = Scoreboard(stdscr)
        self.health_bar = HealthBar(stdscr)

        self.start_listener()

    # Draw all the entities and componenst of the game to the main screen
    def draw(self):
        self.stdscr.clear()
        [projectile.draw() for projectile in self.projectiles]
        [alien.draw() for alien in self.aliens]
        [animation.draw() for animation in self.animations]
        self.player.draw()
        self.scoreboard.draw()
        self.health_bar.draw()
        self.stdscr.refresh()

    # Starts the games (the main thread).
    def start(self) -> bool:
        self.tickThread = threading.Thread(target=self.loopTick)
        self.tickThread.start()
        self.tickThread.join()
        return self.score

    # Pausing the game and creating the pause menu
    def pause(self):
        self.state = GameState.PAUSED

        pause_menu: Menu = Menu(
            ["Resume", "Exit"], self.stdscr, self.curses)
        menu_seleceted = pause_menu.start()
        if (menu_seleceted == "Exit"):
            self.state = GameState.DONE
        if (menu_seleceted == "Resume"):
            self.state = GameState.PLAYING
            self.listener.stop()
            self.start_listener()

    # Starts and saves the listener for keystrokes using pynput
    def start_listener(self):
        def on_press(key):
            self.keydowns.add(key)

        def on_release(key):
            self.keydowns.remove(key)

        self.listener = Listener(on_press=on_press, on_release=on_release)
        self.listener.start()

    # Preforms the main logic of the game (game tick)
    def tick(self):
        # Loop over the keystrokes and calls the handler on each of them
        keydowns = self.keydowns.copy()
        [self.handle_key_press(key) for key in keydowns]

        # Filter out the projectiles which are out of the screen
        self.projectiles = list(filter(
            lambda projectile: projectile.in_bound(), self.projectiles))

        # Filter out the animations which are done
        self.animations = list(filter(
            lambda animation: not animation.is_done(), self.animations))

        # Increase the rotation number (responsible for the moving back and forth of the aliens)
        self.rotation += 1
        self.rotation = self.rotation % 100

        for alien in self.aliens:
            # The logic of the back and forth of the aliens
            if (self.rotation % 10 == 0):
                if (self.rotation < 50):
                    alien.moveX(1)
                else:
                    alien.moveX(-1)

            # The logic to when the alien try and shoot a projectile, based on the type of alien and the difficulty
            if (random() < 0.005 * (alien.type.value / 10) * (self.difficulty.value / 2)):
                new_projectile = alien.shoot()
                if new_projectile != False:
                    self.projectiles.append(new_projectile)

        # Loops over all the projectiles and checks for collision based on the 'parent' of the projectile
        for projectile in self.projectiles:
            if (type(projectile.parent).__name__ == "Alien" and projectile.is_intersecting(self.player)):
                self.projectiles.remove(projectile)
                # Decrease player's health upon being hit and shows defeat screen if the player's health is 0
                self.health_bar.hit(5 * self.difficulty.value)
                if self.health_bar.health == 0:
                    self.you_died()
            elif (type(projectile.parent).__name__ == "Player"):
                for alien in self.aliens:
                    if (projectile.is_intersecting(alien)):
                        self.projectiles.remove(projectile)
                        remaining_health = alien.hit(10)
                        # Decrease alien's health upon being hit and kills it if necessary.
                        if remaining_health <= 0:
                            self.scoreboard.add(
                                floor(alien.type.value * self.difficulty.value / 2))
                            self.aliens.remove(alien)
                            # Creates death animation of alien's death
                            death_animation = Animation(
                                self.stdscr, DEATH_ANIMATION, alien.x - 1, alien.y - 1, 3)
                            self.animations.append(death_animation)
        self.draw()

    # The main thread function, responsible for keeping the game alive and preforming the game ticks if the game isn't done
    # Responsible for presenting the levels and moving through them if the previous level had been defeated.
    def loopTick(self) -> None:
        while True and self.state != GameState.DONE:
            if (self.state == GameState.PLAYING):
                self.tick()
                if (len(self.aliens) == 0):
                    self.level = GameLevel(self.level.value + 1)
                    self.state = GameState.LOADING
            elif (self.state == GameState.LOADING):
                if (self.level.value == 11):
                    self.you_won()
                else:
                    self.state = GameState.PLAYING
                    flying_label = FlyingLabel(
                        LEVEL_LABELS[self.level.value - 1], self.stdscr)
                    flying_label.start()
                    w = self.stdscr.getmaxyx()[1]
                    self.projectiles = []

                    for alien in LEVELS_LAYOUT[self.level.value - 1]:
                        self.aliens.append(
                            Alien((w - 80) // 2 + alien['x'] - 3, alien['y'], alien['type'], self.difficulty, self.stdscr))

            time.sleep(1 / self.ticks_per_second)
        self.score = self.scoreboard.score

    # The function which handles the keystrokes
    def handle_key_press(self, key) -> None:
        # Pause if escape is pressed
        if (key == Key.esc and self.state != GameState.PAUSED):
            self.pause()
        # Moves the player on arrow keystrokes
        elif key == Key.right:
            self.player.move(1)
        elif key == Key.left:
            self.player.move(-1)
        # Shoots a projectiles on space keystroke
        elif key == Key.space:
            new_projectile = self.player.shoot()
            if new_projectile != False:
                self.projectiles.append(new_projectile)

    # Shows the you died screen and finishs the game
    def you_died(self):
        self.state = GameState.DONE
        you_died_label = FlyingLabel(
            YOU_DIED_LABEL, self.stdscr)
        you_died_label.start()

    # Shows the you won screen and finishs the game
    def you_won(self):
        self.state = GameState.DONE
        you_won_label = FlyingLabel(
            YOU_WON_LABEL, self.stdscr)
        you_won_label.start()
