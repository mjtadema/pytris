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
import curses
import time
from .block import Block
from multiprocessing import Process
from pathlib import Path

gridsize = (20, 10)
grid_y, grid_x = gridsize
buff = 4
insert_point = (3, grid_x//2)
stdscr = ''
grid = ''
y_off, x_off = (1,1)
report = ''
score = 0
speed = 1.0
factor = 0.6
level = 1
score_file = f"{Path.home()}/.pytris_highscore"
name = 'nobody'
highscore = 0
block = "curses."
block_list = []
p_audio = ''

def start(init_stdscr=None, **kwargs):
    """
    Starts the main game loop
    Initializes a block
    Moves the block until there is a collision
    Loop until game over
    """
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

    global p_audio
    try:
        from . import audio
        p_audio = Process(target=audio.start)
        p_audio.start()
    except ImportError:
        # simpleaudio is not installed
        pass

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

def report_curses(*message):
    stdscr.addstr(4, 12+x_off, " ".join(message))
    stdscr.refresh()

def border():
    top = "+----------+"
    bottom = "+----------+"
    side = "|          |"
    stdscr.addstr(0, 0, top)
    grid_y, grid_x = gridsize
    for y in range(grid_y-buff):
        Y = y+1
        stdscr.addstr(Y, 0, side)
    stdscr.addstr(grid_y-buff+1, 0, bottom)

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


