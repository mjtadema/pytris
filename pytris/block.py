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
import random

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
        insert_point = (self.game.grid.width // 2, self.game.grid.top_buffer - 2)
        self.mobile = True

        # Initialize block definition
        self.anchor = [insert_point]
        self.rotation = [0]



    def __str__(self):
        return self.__class__.__name__

    def position(self, anchor = None):
        """
        Optional: set a custom anchor
        returns: an array of coordinates
        """
        if anchor == None:
            anchor = self.anchor[-1]
        return np.add(anchor, self.states[self.rotation[-1]])

    def last(self):
        """
        Get the previous position, used for blanking old block position
        only if len of anchor and rotation >= 2..
        """
        try:
            return np.add(self.anchor[-2], self.states[self.rotation[-2]])
        except IndexError:
            return self.position() # Should be fine...

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
                # Block is not mobile but trying to move block
                return False
            move_func(self)
            self.game.screen.print("Moved "+move_func.__name__)
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
                    # If the block was at the top of the screen, trigger game over
                    self.game.gameover = self.is_gameover()
                    self.game.screen.block()
                    return False

            self.game.screen.block()
            return True
        return wrapper

    def random_move(self):
        # Init all moves, used for picking a random move
        self.moves = [
            self.down,
            self.left,
            self.right,
            self.clockwise,
            self.countercw
        ]
        picked_move = self.moves[random.randint(0, len(self.moves) - 1)]
        return picked_move()

    def is_gameover(self):
        """
        Test whether an y coord is above the buffer zone
        """
        for x, y in self.position():
            if y <= self.game.grid.top_buffer:
                return True
        return False

    def collision(self):
        """
        Check if any block position intersects with a block on
        the grid or a wall
        :return: Boolean
        """
        for x, y in self.position():
            if not 0 <= x < self.game.grid.width:
                return True
            if not 0 <= y < self.game.grid.height:
                return True
            if self.game.grid[x][y] != 0:
                return True
        return False


    def to_grid(self):
        self.game.grid.set(self.color, self.position())

    @move
    def down(self):
        now = self.anchor[-1]
        next = tuple(np.add(now, (0, 1)))
        self.anchor.append(next)
        self.rotation.append(self.rotation[-1])

    """
    Obviously the blocks cannot possibly move up..
    """
    #@move
    #def up(self):
    #    now = self.anchor[-1]
    #    next = tuple(np.subtract(now, (0, 1)))
    #    self.anchor.append(next)
    #    self.rotation.append(self.rotation[-1])

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
            tmp = tmp % (len(self.states))
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
                         (0, 1),
                (-1, 0), (0, 0), (1, 0),
            ],

            [
                         (0, 1),
                (-1, 0), (0, 0),
                         (0,-1)
            ],
            [
                (-1, 0), (0, 0), (1, 0),
                         (0, -1)
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
                (-1,-1), (0,-1)
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