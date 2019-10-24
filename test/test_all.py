import pytest

@pytest.fixture
def game():
    from pytris.game import Game
    return Game(debug = True)

def test_game(game):
    assert game

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

from pytris.block import Block
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
    def test_up(self, game):
        # Up
        block = game.queue.pop()
        now = block.position()
        block.up()
        next = block.position()
        for (ax, ay), (bx, by) in zip(now, next):
            assert by == ay - 1

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
            assert 0 <= x < block.game.grid.grid_x
        block = game.queue.pop()
        for _ in range(10):
            block.right()
        for x, y in block.position():
            assert 0 <= x < block.game.grid.grid_x
