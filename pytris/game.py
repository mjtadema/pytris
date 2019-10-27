#MIT License
#
#Copyright (c) 2019 Matthijs Tadema
#
#Permission is hereby granted, free of charge, to any person obtaining a copy
#of this software and associated documentation files (the "Software"), to deal
#in the Software without restriction, including without limitation the rights
#to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#copies of the Software, and to permit persons to whom the Software is
#furnished to do so, subject to the following conditions:
#
#The above copyright notice and this permission notice shall be included in all
#copies or substantial portions of the Software.
#
#THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
#OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
#SOFTWARE.

# Relative imports
from .grid import Grid 
from .screen import Screen
from .queue import Queue

# Stdlib
import time
from pathlib import Path
import getpass

class Game():
    """
    Game instance holds the state of the game
    It initializes the screen, audio,

    Contains:
        grid    : grid of immobile blocks
        block   : mobile block object
        p_audio : audio process
        queue   : queue of next blocks
        screen  : abstraction to curses
    """
    def __init__(self, debug = False, screen = None):
        """ 
        Initialize game state

        """
        # Move arguments to attributes
        self.debug = debug

        # Initialize screen
        self.screen = Screen(self, screen)

        # Initialize grid
        self.grid = Grid(self)

        # Initialize block queue
        self.queue = Queue(self)

        # Pop the first block
        self.block = self.queue.pop()

        # Initialize some values
        self.gameover = False
        self.score = 0
        if self.debug:
            # When debugging just put maximum speed
            self.speed = 0.0
        else:
            self.speed = 0.8

        self.factor = 0.6
        self.level = 1
        self.t = 0
        self.paused = False

        self.read_highscore()
        self.screen.data()

    def read_highscore(self):
        try:
            with open(f"{Path.home()}/.pytris_highscore") as f_high:
                self.username = str(f_high.readline().strip())
                self.highscore = int(f_high.readline().strip())
        except:
            self.username = "Nobody"
            self.highscore = 0

    def write_highscore(self):
        if self.score > self.highscore:
            self.username = getpass.getuser()
            try:
                with open(f"{Path.home()}/.pytris_highscore", 'w') as f_high:
                    f_high.write(str(self.username + "\n"))
                    f_high.write(str(self.score))
            except:
                pass # Else just fuck it

    def pause(self):
        """
        Toggle pause the game
        """
        self.block.mobile = not self.block.mobile
        if not self.paused:
            self.paused = True
            # Also print paused message
            self.screen.print("PAUSED")
        else:
            self.paused = False
            self.screen.print("")
        # Also reset tick time
        self.t = time.time()

    def add_score(self, score_to_add):
        """
        Adds the score to the current score in game
        """
        self.score += score_to_add
        if self.score // self.level >= 20:
            self.level += 1
            self.speed *= self.factor
            self.screen.print("Speed is now: " + str(self.speed))
            self.screen.data()
        # Refresh the data on screen
        self.screen.data()

    def tick(self):
        """
        Check if a tick has passed
        :return: Bool
        """
        if time.time() - self.t > self.speed:
            self.t = time.time()
            return True
        else:
            return False

    def start(self):
        """
        The main game loop.
        During a tick, allow the block to be moved by the user
        After each tick, the block is moved downward forcefully.
        If the bottom is hit, a new block is popped from the queue
        """
        while not self.gameover:

            # Pop a new block from queue
            self.block = self.queue.pop()

            while self.block.mobile:
                # Try to get commands turing a tick
                while not self.tick():
                    self.screen.command()
                    # Limit CPU cycles, IMPORTANT
                    # When debugging or testing, DON'T sleep but go asap
                    if not self.debug:
                        time.sleep(0.01)
                    else:
                        self.block.random_move()

                # While paused, the block is not mobile so move commands are ignored
                while self.paused:
                    self.screen.command()
                    continue # So that the block isn't immediately moved down

                # After a tick passes, move the block down forcefully
                self.block.down()

            # After every collision:
            # Check if there is a full row in the grid
            self.grid.row_is_full()

        # Game is now over
        self.screen.print("Game over!")
        self.write_highscore()
        time.sleep(3)

        # There is not yet an endgame screen
        self.screen.endgame()


