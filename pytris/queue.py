from .block import blocks

import copy
import random

class Queue(list):
    """
    The queue contains 1 copy of each block
    When the bag is depleted, it is again filled with blocks in random order
    Blocks are "popped" from the queue
    """
    def __init__(self, game, *args, **kwargs):
        self.game = game
        self.fill()

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
        block = super().pop(i)
        # Draw the next block in the next box
        self.game.screen.next()
        return block

    def next(self):
        """
        Return the next block in the queue
        """
        return self[0]