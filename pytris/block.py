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

class Block():
    """
    Base block class, is inherited from to form individual blocks
    Collisions are checked upon movement
    """
    def __init__(self, game, *args, **kwargs):
        """
        Base block object
            init()                  : Spawns new block

        Exposes following methods:
            clockwise()             : Rotate the block clockwise
            countercw()             : Rotate the block counterclockwise
            up()                    : Move up
            down()                  : Move down
            left()                  : Move left
            right()                 : Move right
            position()              : Current coordinates of all squares

        And properties:
            anchor                  : tuple( y, x ) to define anchor point
            color                   : character to draw on the grid
            states                  : list of rotational states
            rotation                : Current relative rotation to anchor

        """

        self.game = game
        grid_y, grid_x = self.game.gridsize
        insert_point = (3, grid_x // 2)
        self.mobile = True

        # Initialize block definition
        self.anchor = [insert_point]
        self.rotation = [0]

    def __str__(self):
        return self.__class__.__name__

    def position(self):
        """
        returns: an array of coordinates
        """
        return np.add(self.anchor[-1], self.states[self.rotation[-1]])

    def move(move_func):
        """
        Decorator for movement functions
        Checks for collision, first check if bottom is hit.
        If block collided with the bottom of the grid or the
        top of a block, move the block to grid
        If block collided with a wall (sideways),
        revert the move by popping the last item
        Finally automatically draw the block to the screen
        :param move_func: A function that moves the block
        :return: Boolean signifying collision
        """
        def wrapper(self):
            if not self.mobile:
                raise Exception("Block is not mobile but trying to move block")
            move_func(self)
            # First check if a collision has occurred
            if self.collision():
                # If it has, revert the move
                self.anchor.pop(-1)
                self.rotation.pop(-1)
                # Check if the last move was downward
                if move_func.__name__ == "down":
                    # If it was, it's a bottom collision
                    self.to_grid()
                    self.mobile = False
                    return False
            # Finally abstract away screen drawing
            self.game.screen.block()
        return wrapper

    def collision(self):
        """
        Check if any block position intersects with a block on
        the grid or a wall
        :return: Boolean
        """
        for x, y in self.position():
            if not 0 <= x < self.game.grid.grid_x:
                return True
            if not 0 <= y < self.game.grid.grid_y:
                return True
            if self.game.grid[x][y] != 0:
                return True
        return False

    @move
    def down(self):
        now = self.anchor[-1]
        next = tuple(np.add(now, (0, 1)))
        self.anchor.append(next)
        self.rotation.append(self.rotation[-1])

    @move
    def up(self):
        now = self.anchor[-1]
        next = tuple(np.subtract(now, (0, 1)))
        self.anchor.append(next)
        self.rotation.append(self.rotation[-1])

    @move
    def left(self):
        now = self.anchor[-1]
        next = tuple(np.subtract(now, (1, 0)))
        self.anchor.append(next)
        self.rotation.append(self.rotation[-1])

    @move
    def right(self):
        now = self.anchor[-1]
        next = tuple(np.add(now, (1, 0)))
        self.anchor.append(next)
        self.rotation.append(self.rotation[-1])

    @move
    def clockwise(self):
        tmp = 0
        if len(self.states) > 1:
            tmp = self.rotation[-1] + 1
            tmp %= len(self.states) - 1
        self.rotation.append(tmp)
        self.anchor.append(self.anchor[-1])

    @move
    def countercw(self):
        tmp = 0
        if len(self.states) > 1:
            tmp = self.rotation[-1] - 1
            if tmp < 0:
                tmp = len(self.states) - 1
        self.rotation.append(tmp)
        self.anchor.append(self.anchor[-1])

"""
0: black
1: red
2: green
3: yellow
4: blue
5: magenta
6: cyan
7: white
"""

class I(Block):
    def __init__(self, *args, **kwargs):
        self.states = [
            [
                                (0, 2),
                                (0, 1),
                                (0, 0),
                                (0,-1)
            ],
            [
                        (-1,0),(0,0),(1,0),(2,0)
            ],
            [
                                (0,1),
                                (0,0),
                                (0,-1),
                                (0,-2)
            ],
            [
                (-2,0),(-1,0),(0,0),(1,0)
            ]
        ]
        self.color = 1
        super().__init__(*args, **kwargs)

class T(Block):
    def __init__(self, *args, **kwargs):
        self.states = [
            [
                (0,-1), (0, 0), (0, 1),
                        (-1,0)
            ],
            [
                         (0, 1),
                (-1, 0), (0, 0),
                         (0,-1)
            ],
            [
                         (1, 0),
                (0, -1), (0, 0), (0, 1),
            ],
            [
                         (0, 1),
                         (0, 0), (1, 0),
                         (0,-1)
            ]
        ]
        self.color = 2
        super().__init__(*args, **kwargs)

class O(Block):
    def __init__(self, *args, **kwargs):
        self.states = [
            [
                (-1, 0), (0, 0),
                (-1,-1), (0,-1)
            ]
        ]
        self.color = 3
        super().__init__(*args, **kwargs)

class L(Block):
    def __init__(self, *args, **kwargs):
        self.states = [
            [
                (0, 1),
                (0, 0),
                (0,-1), (1,-1)
            ],
            [
                (-1,0),(0,0),(1,0),
                (-1,-1)
            ],
            [
                (-1, 1), (0, 1),
                         (0, 0),
                         (0,-1)
            ],
            [
                                 (1, 1),
                (-1, 0), (0, 0), (1, 0),
            ]
        ]
        self.color = 4
        super().__init__(*args, **kwargs)

class J(Block):
    def __init__(self, *args, **kwargs):
        self.states = [
            [
                        (0, 1),
                        (0, 0),
                (-1,1), (0,-1)
            ],
            [
                (-1, 1),
                (-1, 0), (0, 0), (1, 0),
            ],
            [
                        (0, 1), (1, 1),
                        (0, 0),
                        (0,-1)
            ],
            [
                (-1, 0), (0, 0), (1, 0),
                                 (1,-1)
            ]
        ]
        self.color = 5
        super().__init__(*args, **kwargs)

class S(Block):
    def __init__(self, *args, **kwargs):
        self.states = [
            [
                        (0, 1), (1, 1),
                (-1,0), (0, 0)
            ],
            [
                (0, 1),
                (0, 0), (1, 0),
                        (1,-1)
            ]
        ]
        self.color = 6
        super().__init__(*args, **kwargs)

class Z(Block):
    def __init__(self, *args, **kwargs):
        self.states = [
            [
                (-1,1), (0, 1),
                        (0, 0), (1, 0)
            ],
            [
                        (1, 1),
                (0, 0), (1, 0),
                (0,-1)
            ]
        ]
        self.color = 7
        super().__init__(*args, **kwargs)

blocks = [I,T,O,L,J,S,Z]