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


import utils as ut
import random as r
import numpy as np

blocktypes = {
        'line'  :{
            'coords': [ (0,0), (-1,0), (-2,0), (-3,0) ], 
            'mark'  : '1' },
        't'     :{
            'coords': [ (-1,0), (0,-1), (0,0), (0,1) ],
            'mark': '2' },
        'square'  :{
            'coords': [ (0,0), (-1,0), (0,-1), (-1,-1) ], 
            'mark'  : '3' },
        'l'  :{
            'coords': [ (0,0), (-1,0), (-2,0), (0,1) ], 
            'mark'  : '4' },
        'rev_l'  :{
            'coords': [ (0,0), (-1,0), (-2,0), (0,-1) ], 
            'mark'  : '5' },
        'squig'  :{
            'coords': [ (0,0), (-1,0), (-1,1), (0,-1) ], 
            'mark'  : '6' },
        'rev_squig'  :{
            'coords': [ (0,0), (1,0), (1,-1), (0,1) ], 
            'mark'  : '7' }
        }
allowed_blocks = list(blocktypes.keys())
#allowed_blocks = ['test']
movements = {
        'down' : (1,0),
        'left' : (0,-1),
        'right': (0,1)
        }
allowed_moves = list(movements.keys())
rotations = {
        'fw'   : True,
        'rv'   : False
        }
allowed_rotations = list(rotations.keys())

def pick(keys):
    picked_key = keys[r.randint(0, len(keys)-1)]
    return picked_key

class Block():
    def __init__(self, **kwargs):
        """
        Base block object
            init(type, insert)      : Spawns new block of type "type" at "insert"

        Exposes following methods:
            rotate(fw)              : Rotates the block forward (True) or reverse (False)
            move(move)              : Moves the anchor by move tuple( y, x ) 
            position()              : Actual coordinates of all squares

        And properties:
            anchor                  : tuple( y, x ) to define anchor point
            mark                    : character to draw on the grid
            definition              : Base definition (constant)
            rotation                : Current relative rotation to anchor

        """
        # Initialize block definition
        if kwargs['block_type'] == 'random':
            block_type  = pick(allowed_blocks)
        block_def       = blocktypes[block_type]
        self.definition = block_def['coords']
        self.mark       = block_def['mark']
        self.anchor     = kwargs['insert_point']
        self.rotation   = self.definition

        # Save previous coords/anchor
        self.prev_anc       = self.anchor
        self.prev_rot       = self.rotation
        self.prev_move      = 'down'

        # Initialize tuple to determine rotation direction
        self.fw_rv      = (ut.switch_tuple, ut.invert_tuple)

    def __str__(self):
        grid = np.zeros((14, 10))
        for y, x in self.position():
            grid[y][x] = self.mark
        return str(grid)
    __repr__ = __str__
    def __iter__(self):
        return(iter(self.position()))

    def position(self, anchor=None, rotation=None):
        if not anchor:
            anchor = self.anchor
        if not rotation:
            rotation = self.rotation
        return ut.add_tuples(anchor, rotation)

    def update(func):
        def out_func(self, *args):
            self.prev_anc = self.anchor
            self.prev_rot = self.rotation
            func(self, *args)
        return out_func

    @update
    def rotate(self, rot_key):
        """
        Rotates the block forwards or reverse
        input: bool
        """
        if rot_key == 'random':
            rot_key = pick(allowed_rotations)
        rot_action = rotations[rot_key]
        if rot_key == 'fw':
            rot_func = self.fw_rv[0]
        else:
            rot_func = self.fw_rv[1]
        self.rotation = [ tuple([x, -y]) for y, x in self.rotation ] 
        self.fw_rv = ut.switch_tuple(self.fw_rv)
        self.prev_move = rot_key


    @update
    def move(self, move):
        """
        Moves the block anchor by "move" translation
        input: tuple( y, x )
        """
        if move == 'random':
            move = pick(allowed_moves)
        move_tup = movements[move]
        self.anchor = ut.add_tuples(self.anchor, move_tup)
        self.prev_move = move

    def revert(self):
        if self.prev_move == 'rv' or self.prev_move == 'fw':
            # Then it was a rotation
            self.rotation = self.prev_rot
            self.fw_rv = ut.switch_tuple(self.fw_rv)
        # Else it was a translation
        self.anchor = self.prev_anc

