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


from .grid import Grid 
from .ui import Screen
import curses
import time
from .block import blocks
from multiprocessing import Process
from pathlib import Path
from .utils import parse_args
import copy
import random

report = ''
score_file = f"{Path.home()}/.pytris_highscore"
name = 'nobody'
highscore = 0
block = "curses."
block_list = []
p_audio = ''

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
    def __init__(self, *args, gridsize = (20, 10), **kwargs):
        """ 
        Initialize game state

        """
        # Move arguments to attributes
        self.gridsize = gridsize
        self.debug = False
        if "debug" in kwargs.keys():
            self.debug = True

        # Start audio
        try:
            if kwargs['audio']:
                self.p_audio = start_audio()
        except KeyError:
            pass

        # Initialize screen
        self.screen = Screen(self, **kwargs)

        # Initialze grid
        self.grid = Grid(gridsize)

        # Initialize block queue
        self.queue = Queue(self)

        # Initialize first block
        self.block = self.queue.pop()



        # Initialize some values
        self.gameover = False
        self.score = 0
        self.speed = 1.0
        self.factor = 0.6
        self.level = 1
        self.t = 0

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
        The main game loop
        """
        try:
            while not self.gameover:

                if not self.block.mobile:
                    # Pop a new block from queue
                    self.block = self.queue.pop()

                # Keep track of game ticks
                # speed basically determines the time a tick takes
                while True:
                    # Move the block down every "tick"
                    if self.tick():
                        if not self.block.down():
                            # Means a collision has occurred
                            break

                    # Try to get a command every cycle
                    try:
                        self.screen.command()
                    except (curses.error, KeyError):
                        # Ignore curses errors
                        pass

                    # Limit CPU cycles, IMPORTANT
                    time.sleep(0.01)

                # After every collision:
                # Check if there is a full row in the grid
                self.grid.full_row()

                # At every 20 points, increment level and speed
                self.check_score()


        except KeyboardInterrupt as e:
            if p_audio:
                p_audio.terminate()
            raise e

        self.screen.endgame()
        #refresh()
        #stdscr.nodelay(False)
        #report("Game Over!")
        #write_highscore()

        #if stdscr:
        #    stdscr.getch()
        try:
            p_audio.terminate()
        except:
            pass

    def check_score(self):
        """
        Check if the level and speed should be incremented
        :return: Bool
        """
        if self.score // self.level >= 20:
            self.level += 1
            self.speed *= self.factor
            self.screen.data()
            return True
        else:
            return False

def start_audio(self):
    try:
        from . import audio
        p_audio = Process(target=audio.start)
        p_audio.start()
        return p_audio
    except ImportError:
        # simpleaudio is not installed
        pass
    pass


class Queue(list):
    """
    The queue contains 1 copy of each block
    When the bag is depleted, it is again filled with blocks in random order
    Blocks are "popped" from the queue
    """
    def __init__(self, game, *args, **kwargs):
        self.game = game
        self.fill()
    def __str__(self):
        tmp = ""
        for b in self:
            tmp += b.__class__.__name__ + ","
        return tmp
    def fill(self):
        tmp = copy.deepcopy(blocks)
        random.shuffle(tmp)
        for b in tmp:
            self.append(b(game = self.game))
    def pop(self, i = 0):
        """
        Pop a block from the stack
        Automatically draw new block to screen
        :return: Block
        """
        if len(self) <= 2:
            self.fill()
        n = super().pop(i)
        self.game.screen.next(n)
        return n


def start(init_stdscr=None, **kwargs):
    """
    Starts the main game loop
    Initializes a block
    Moves the block until there is a collision
    Loop until game over
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('--audio','-a',action='store_true', default=False)
    args = parser.parse_args()
    if args.audio:
        global p_audio
        try:
            from . import audio
            p_audio = Process(target=audio.start)
            p_audio.start()
        except ImportError:
            # simpleaudio is not installed
            pass


    global grid
    global gridsize
    grid = Grid(gridsize)

    global report
    if init_stdscr:
        global stdscr
        stdscr = init_stdscr
        refresh = refresh_curses
        report = report_curses
        border()
        curses.curs_set(0)
        stdscr.nodelay(True)
        curses.use_default_colors()
        for i in range(0, curses.COLORS):
            curses.init_pair(i, -1, i);
        
    else:
        refresh = refresh_debug
        report = print
        breakpoint()

    global block_list
    block_list = [
            Block(block_type='random', insert_point=insert_point)
            for _ in range(2)
            ]

    global score
    report_score()
    read_highscore()

    global speed
    global level

    try:
        while not grid.game_over:
            grid.spawn(get_next_block())
            show_next_block()
            t0 = time.time()
            while True:
                if time.time() - t0 > speed:
                    t0 = time.time()
                    grid.block.move('down')
                try:
                    pick_move(get_move())
                except (curses.error, KeyError):
                    pass
                if grid.collision():
                    break
                refresh()
                time.sleep(0.01)

            grid.put()
            score += grid.full_row()
            if score // level >= 20:
                level += 1
                speed *= factor
            report_score()
    except KeyboardInterrupt as e:
        if p_audio:
            p_audio.terminate()
        raise e

    refresh()
    stdscr.nodelay(False)
    report("Game Over!")
    write_highscore()
    if stdscr:
        stdscr.getch()
    try:
        p_audio.terminate()
    except:
        pass

def show_next_block():
    for y in range(1,6):
        y += 8
        stdscr.addstr(y, 12+x_off, ' '*8)
    global block_list
    stdscr.addstr(8, 12+x_off, "Next:")
    next_b = block_list[0]
    y_ori = 9
    x_ori = 10
    for y, x in next_b:
        m = next_b.mark
        stdscr.addstr(y+y_ori, x+x_ori, ' ', curses.color_pair(m))


def get_next_block():
    global block_list
    block_list.append(Block(block_type='random', insert_point=insert_point))
    return block_list.pop(0)

def pick_move(move):
    if move == 'fw':
        grid.block.rotate(move)
    else:
        grid.block.move(move)

movelookup = {
        'KEY_DOWN': 'down',
        'KEY_LEFT': 'left',
        'KEY_RIGHT': 'right',
        'KEY_UP': 'fw'
        }
def get_move():
    return movelookup[stdscr.getkey()]

def clear_curses():
    grid_y, grid_x = gridsize
    for y in range(10):
        stdscr.addstr(y+y_off, 0+x_off, " "*grid_x)

def refresh_curses():
    clear_curses()
    for y, line in enumerate(grid[4:]):
        for x, ch in enumerate(line):
            if ch == 0:
                ch = ' '
                stdscr.addstr(y+y_off, x+x_off, ch)
            else:
                stdscr.addstr(y+y_off, x+x_off, " ", curses.color_pair(ch))
                
    refresh_block()
    stdscr.refresh()

def refresh_block():
    for y, x in grid.block.position():
        if y > 3:
            Y = y+y_off-buff
            X = x+x_off
            ch = grid.block.mark
            stdscr.addstr(Y, X, " ", curses.color_pair(grid.block.mark))

def refresh_debug():
    print(grid)

def report_score():
    global score
    global level
    stdscr.addstr(1, 12+x_off, "SCORE: "+str(score))
    stdscr.addstr(2, 12+x_off, "LEVEL: "+str(level))
    stdscr.refresh()

def read_highscore():
    global name
    global highscore
    try :
        with open(score_file, 'r') as f: 
            name = f.readline().strip()
            highscore = f.readline().strip()
    except:
        pass
    stdscr.addstr(4, 12+x_off, "HIGHSCORE:")
    stdscr.addstr(5, 12+x_off, str(name))
    stdscr.addstr(6, 12+x_off, str(highscore))

def write_highscore():
    if score > int(highscore):
        import getpass
        name = getpass.getuser()
        with open(score_file, 'w') as f:
            f.write(f"{name}\n")
            f.write(f"{score}\n")


