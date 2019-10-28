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

class Grid(list):
    """
    Grid now keeps track of the underlying grid of immobile blocks
    """

    def __init__(self, game):
        # Initialize grid
        self.game = game
        self.gridsize = (10, 40)
        self.top_buffer = 20 # Following tetris guidlines
        self.width, self.height = self.gridsize
        # Doing it in this way so that the grid is accessed as grid[x][y]
        for col in range(self.width):
            self.append([0 for row in range(self.height)])

    def row_is_full(self):
        """
        Checks if a row is full (doesn't contain a 0 anymore)
        If so, pop the row and insert a new row at the bottom of the list
        Also redraw the grid to the screen
        :return: None

                  columns x
                  0 1 2 3 4 5 ...
         rows y 0 [ [ [ [ [ [
                1
                2         a
                3
                4
                5 [ [ [ [ [ [
                ...

            a = grid[4][2]
            for i in width:
                grid[i].pop(2)
                grid[i].insert(0, 0)

        """
        full = 0
        # Grid is defined as x by y
        # Iterate over rows
        for i in range(self.height):
            row = [self[j][i] for j in range(self.width)]
            if 0 not in row:
                full = True
                for j in range(self.width):
                    # Pop the full row
                    self[j].pop(i)
                    # Insert a new row at the top
                    self[j].insert(0, 0)
        if full > 0:
            self.game.add_score(full)
            # Refresh the grid on the screen
            self.game.screen.grid()

    def set(self, value, iterable):
        """
        Set a value to a list of grid coordinates
        """
        for x, y in iterable:
            self[x][y] = value
