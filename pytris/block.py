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
    """
    def __init__(self, *args, **kwargs):
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

        self.grid = kwargs['grid']
        grid_y, grid_x = self.grid.gridsize
        insert_point = (0, grid_x // 2)

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

    def down(self):
        now = self.anchor[-1]
        next = tuple(np.add(now, (0, 1)))
        self.anchor.append(next)

    def up(self):
        now = self.anchor[-1]
        next = tuple(np.subtract(now, (0, 1)))
        self.anchor.append(next)

    def left(self):
        now = self.anchor[-1]
        next = tuple(np.subtract(now, (1, 0)))
        self.anchor.append(next)

    def right(self):
        now = self.anchor[-1]
        next = tuple(np.add(now, (1, 0)))
        self.anchor.append(next)

    def clockwise(self):
        tmp = 0
        if len(self.states) > 1:
            tmp = self.rotation[-1] + 1
            tmp %= len(self.states) - 1
        self.rotation.append(tmp)

    def countercw(self):
        tmp = 0
        if len(self.states) > 1:
            tmp = self.rotation[-1] - 1
            if tmp < 0:
                tmp = len(self.states) - 1
        self.rotation.append(tmp)

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
        self.mark = 1
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
        self.mark = 2
        super().__init__(*args, **kwargs)

class O(Block):
    def __init__(self, *args, **kwargs):
        self.states = [
            [
                (-1, 0), (0, 0),
                (-1,-1), (0,-1)
            ]
        ]
        self.mark = 3
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
        self.mark = 4
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
        self.mark = 5
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
        self.mark = 6
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
        self.mark = 7
        super().__init__(*args, **kwargs)

blocks = [I,T,O,L,J,S,Z]