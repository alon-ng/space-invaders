

from time import sleep, time
from typing import List


class GameManual:
    MANUAL_HEADER = ["""
   _____                        _____                     _
  / ____|                      |_   _|                   | |
 | (___  _ __   __ _  ___ ___    | |  _ ____   ____ _  __| | ___ _ __ ___
  \\___ \\| '_ \\ / _` |/ __/ _ \\   | | | '_ \\ \\ / / _` |/ _` |/ _ \\ '__/ __|
  ____) | |_) | (_| | (_|  __/  _| |_| | | \\ V / (_| | (_| |  __/ |  \\__ \\
 |_____/| .__/ \\__,_|\\___\\___| |_____|_| |_|\\_/ \\__,_|\\__,_|\\___|_|  |___/
        | |
        |_|
    """,
                     """
   _____        __                           _   _             
 |_   _|      / _|                         | | (_)            
   | |  _ __ | |_ _ __ ___  _ __ ___   __ _| |_ _  ___  _ __  
   | | | '_ \|  _| '__/ _ \| '_ ` _ \ / _` | __| |/ _ \| '_ \ 
  _| |_| | | | | | | | (_) | | | | | | (_| | |_| | (_) | | | |
 |_____|_| |_|_| |_|  \___/|_| |_| |_|\__,_|\__|_|\___/|_| |_|
    """
                     ]

    MANUAL_TEXT = [
        """
    _   _ _
   /_\ | (_)___ _ _  ___
  / _ \| | / -_) ' \(_-<
 /_/ \_\_|_\___|_||_/__/


          /-1-\\
           | |

       Name: Squid
      Health: 10 HP
    Reward: 10 Points


          /&_&\\
           /2\\

       Name: Crab
      Health: 20 HP
    Reward: 20 Points


          (+!+)
          /(3)\\

      Name: Octopus
      Health: 30 HP
    Reward: 30 Points
        """,
        """
   ___         _           _
  / __|___ _ _| |_ _ _ ___| |___
 | (__/ _ \ ' \  _| '_/ _ \ (_-<
  \___\___/_||_\__|_| \___/_/__/


     Move Right: Arrow Right
      Move Left: Arrow Left
         Shoot: Spacebar
           Pause: ESC
         Select:  Enter
        """,
        """
  _                _
 | |   _____ _____| |___
 | |__/ -_) V / -_) (_-<
 |____\___|\_/\___|_/__/


         Level 1
        30 Squids
         0 Crabs
        0 Octopus


         Level 2
        16 Squids
        10 Crabs
        4 Octopus
        

         Level 3
        10 Squids
        12 Crabs
        8 Octopus


      Levels 4 - 10
   Randomly generated
      levels in an
  increasing difficulty
        """, """
    _   _              _   
   /_\ | |__  ___ _  _| |_ 
  / _ \| '_ \/ _ \ || |  _|
 /_/ \_\_.__/\___/\_,_|\__|


    This game is based on
  the game 'Space Invaders'

    Made by Alon Ner-Gaon
  @(alon.nergaon@gmail.com)

     
        """
    ]

    def __init__(self, stdscr):
        self.stdscr = stdscr
        self.keydowns = set()

    # Present the information page upon being called
    def show(self):
        while True:
            if self.stdscr.getch() == 27:  # ESC
                return

            h, w = self.stdscr.getmaxyx()

            self.stdscr.clear()
            self._print_multi_line(
                self.MANUAL_HEADER[0], w // 2 - len(self.MANUAL_HEADER[0].split('\n')[3]) // 2, 2)
            self._print_multi_line(
                self.MANUAL_HEADER[1], w // 2 - len(self.MANUAL_HEADER[1].split('\n')[1]) // 2, 8)
            self._print_multi_line(
                self.MANUAL_TEXT[0], 6, 18)
            self._print_multi_line(
                self.MANUAL_TEXT[1], w // 2 - len(self.MANUAL_TEXT[1].split('\n')[1]) // 2, 18)
            self._print_multi_line(
                self.MANUAL_TEXT[2], w - 10 - len(self.MANUAL_TEXT[2].split('\n')[1]), 18)
            self._print_multi_line(
                self.MANUAL_TEXT[3], 1 + w // 2 - len(self.MANUAL_TEXT[3].split('\n')[1]) // 2, 32)

            if time() % 2 > 1:  # Makes blinking effect
                text = "Press esc to go back..."
                self.stdscr.addstr(h - 4, w // 2 - len(text) // 2 + 3, text)

            self.stdscr.refresh()
            sleep(0.05)

    # A function which handles a multiple line string print
    def _print_multi_line(self, str: List[str], x, y):
        for i, line in enumerate(str.split('\n')[1:-1]):
            self.stdscr.addstr(y + i, x, line)
