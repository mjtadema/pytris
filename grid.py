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


import numpy as np
import block
import utils as ut
import copy
import time
from functools import partial
import curses
from pytris import gridsize

buff = 4
grid_y, grid_x = gridsize
insert_point           = (3, grid_x//2)

class Grid():

    def __init__(self, gridsize):
        """
        Main object for keeping track of the game

        Provides the following methods:
            start()         : Initializes the game and starts the main loop
            end()           : End the game and close it
            collision()     : Checks if there is a collision
            full_row()      : Deals with full rows

        Contains the following properties:
            grid_main       : numpy array, size (grid_y, grid_x), contains main grid of non-moving squares
            grid_moving     : numpy array, size (grid_y, grid_x), contains grid of moving squares
            block           : current moving Block object

        """
        # Initialize game
        grid_buffer                 = grid_y+buff, grid_x
        self.grid                   = np.zeros((gridsize), dtype=np.int64)
        self.game_over              = False
        self.block                  = ''

    # Some methods to take advantage of numpy arrays
    def __str__(self):
        #if self.block:
        #    grid_copy = copy.deepcopy(self.grid)
        #    return str(copy_to_grid(grid_copy, self.block))
        #else:
        return str(self.grid)
    __repr__ = __str__
    def __getitem__(self, index):
        return self.grid[index]
    def __iter__(self):
        return iter(self.grid)
    def __len__(self):
        return len(self.grid)

    def spawn(self, next_block):
        self.block = next_block

    def at_edge(self):
        for y, x in self.block.position():
            if x == grid_x or x < 0:
                self.block.revert()
                return True
        return False

    def at_bottom(self):
        for y, x in self.block.position():
            if y == grid_y:
                self.block.revert()
                return True
        return False

    def at_block(self):
        for y, x in self.block.position():
            if self.grid[y][x] != 0:
                if self.block.prev_move == 'down':
                    self.block.revert()
                    return True
                else:
                    self.block.revert()
                    return False
        return False

    def at_top(self):
        for y, x in self.block:
            if y <= 3:
                return True
        return False

    def collision(self):
        """
        Returns true if collision is "fatal"
        Else deals with it and returns false
        """
        if self.at_bottom():
            return True 
        elif self.at_edge():
            return False
        elif self.at_block():
            if self.at_top():
                self.game_over = True
            return True
        return False

    def full_row(self):
        row_full = 0
        # Handle full row
        for y, row in enumerate(self.grid):
            if row.all() != 0:
                row_full += 1
                # Delete the full row, insert a blank row up top
                self.grid = np.delete(self.grid, y, axis=0)
                self.grid = np.insert(self.grid, 0, np.zeros((1,grid_x)), axis=0)
        return row_full

    def put(self):
        for y, x in self.block:
            self.grid[y][x] = self.block.mark
