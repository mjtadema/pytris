import pytest

@pytest.fixture
def game():
    """
    Initialize a game object with "debug" flag set
    """
    from pytris.game import Game
    return Game(debug = True)

def test_queue(game):
    """
    The queue object initializes all blocks (7) once
    When the final two are reached, the queue is supplemented
    with 7 blocks again.
    The queue.pop() method pops the first block
    """
    from pytris.block import Block
    assert game.queue
    # Is now 6 because one is popped at game init
    assert len(game.queue) == 6
    for _ in range(7):
        if len(game.queue) == 2:
            assert isinstance(game.queue.pop(), Block)
            assert len(game.queue) == 8
        assert isinstance(game.queue.pop(), Block)

class TestBlock():
    """
    Tests block functionality
      0 1 2 3 4 5 ...
    0
    1
    2
    3
    4
    ...
    """
    def test_block(self, game):
        from pytris.block import Block
        for _ in range(7):
            block = game.queue.pop()
            assert isinstance(block, Block)

    def test_down(self, game):
        # Down
        block = game.queue.pop()
        now = block.position()
        block.down()
        next = block.position()
        for (ax, ay), (bx, by) in zip(now, next):
            assert by == ay + 1

    def test_left(self, game):
        # Left
        block = game.queue.pop()
        now = block.position()
        block.left()
        next = block.position()
        for (ax, ay), (bx, by) in zip(now, next):
            assert bx == ax - 1

    def test_right(self, game):
        block = game.queue.pop()
        # Right
        now = block.position()
        block.right()
        next = block.position()
        for (ax, ay), (bx, by) in zip(now, next):
            assert bx == ax + 1

    def test_clockwise(self, game):
        # Clockwise
        block = game.queue.pop()
        for _ in range(6):
            block.clockwise()
        assert 0 <= block.rotation[-1] < len(block.states)

    def test_countercw(self, game):
        # Countercw
        block = game.queue.pop()
        for _ in range(6):
            block.countercw()
        assert 0 <= block.rotation[-1] < len(block.states)

    def test_walls(self, game):
        # Test wall collisions
        block = game.queue.pop()
        for _ in range(10):
            block.left()
        for x, y in block.position():
            assert 0 <= x < block.game.grid.width
        block = game.queue.pop()
        for _ in range(10):
            block.right()
        for x, y in block.position():
            assert 0 <= x < block.game.grid.width

    def test_bottom(self, game):
        # Test collision with bottom of grid
        block = game.queue.pop()
        for _ in range(40):
            if not block.down():
                break # collision
        for x, y in block.position():
            assert 0 <= y < block.game.grid.height

import numpy as np
class TestGrid:
    """
    Grid needs to be able to clear rows and to properly accept new blocks.
    Blocks should handle collisions with old blocks as well
    """
    def test_grid(self, game):
        """
        Print the grid just to test that it looks okay
        """
        assert len(game.grid) == game.grid.width # first dimension should be x/width
        col = [ game.grid[0][i] for i in range(game.grid.height) ]
        assert len(col) == game.grid.height # Second dimension should be y/height

    def test_full_row(self, game):
        bottom_row = game.grid.height - 1
        for j in range(game.grid.width):
            game.grid[j][bottom_row] = 1
        game.grid.row_is_full()
        assert np.sum([game.grid[j][bottom_row] for j in range(game.grid.width)]) == 0
        # Test if the score is properly incremented
        assert game.score == 1

    def test_block_to_grid(self, game):
        pos = game.block.position()
        game.block.to_grid()
        for x, y in pos:
            assert game.grid[x][y] != 0

    def test_grid_fill(self, game):
        for _ in range(3):
            block = game.queue.pop()
            for _ in range(40):
                if not block.down():
                    break
        height = game.grid.height
        start = height - 1
        stop = height - 6
        step = -1
        # This should at least put something in the last 5 rows..
        for row in range(start, stop, step):
            assert np.sum([game.grid[j][row] for j in range(game.grid.width)]) != 0

    def test_game_over(self, game):
        # Now test for game over condition
        while not game.gameover:
            for _ in range(10):
                block = game.queue.pop()
                for _ in range(40):
                    if not block.down():
                        break
        assert game.gameover

        # Also assert that the buffer rows aren't empty
        row_sum = 0
        for i in range(game.grid.top_buffer + 1):
            row = [game.grid[j][i] for j in range(game.grid.width)]
            row_sum += np.sum(row)
        assert row_sum != 0

class TestGame():

    def test_simulate_game(self, game):
        """
        Now simulate some games with random moves and make sure nothing breaks and all that
        """
        for _ in range(20):
            self.simulate_game(game)

    def simulate_game(self, game):
        import random
        cycles = 0
        while not game.gameover:
            block = game.queue.pop()
            while True:
                if not block.down():
                    break
                if not block.random_move():
                    break # Upon collision
                cycles += 1
                if cycles > 1000:
                    raise Exception("Infinite loop")

        # Also assert that the buffer rows aren't empty
        row_sum = 0
        for i in range(game.grid.top_buffer + 1):
            row = [game.grid[j][i] for j in range(game.grid.width)]
            row_sum += np.sum(row)
        assert row_sum != 0

    def test_start_game(self,game):
        game.start()