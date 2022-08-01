from typing import List


class Animation:
    def __init__(self, stdscr, frames, x, y, repeat):
        self.stdscr = stdscr
        self.frames = []
        for frame in frames:
            for i in range(repeat):
                self.frames.append(frame)
        self.x = x
        self.y = y
        self.stage = 0

    def draw(self):
        self._print_multi_line(self.frames[self.stage])
        self.stage += 1

    def _print_multi_line(self, str: List[str]):
        for i, line in enumerate(str.split('\n')[1:-1]):
            self.stdscr.addstr(self.y + i, self.x, line)

    def is_done(self):
        return self.stage > len(self.frames) - 1
