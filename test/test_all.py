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
    assert len(game.queue) == 7
    for _ in range(7):
        if len(game.queue) == 2:
            assert isinstance(game.queue.pop(), Block)
            assert len(game.queue) == 8
        assert isinstance(game.queue.pop(), Block)

def test_block(game):
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
    for _ in range(7):
        block = game.queue.pop()
        from pytris.block import Block
        assert isinstance(block, Block)
        # Down
        now = block.position()
        block.down()
        next = block.position()
        for (ax, ay), (bx, by) in zip(now, next):
            assert by == ay + 1
        # Up
        now = block.position()
        block.up()
        next = block.position()
        for (ax, ay), (bx, by) in zip(now, next):
            assert by == ay - 1
        # Left
        now = block.position()
        block.left()
        next = block.position()
        for (ax, ay), (bx, by) in zip(now, next):
            assert bx == ax - 1
        # Right
        now = block.position()
        block.right()
        next = block.position()
        for (ax, ay), (bx, by) in zip(now, next):
            assert bx == ax + 1
        # Clockwise
        for _ in range(6):
            block.clockwise()
        assert 0 <= block.rotation[-1] < len(block.states)
        # Countercw
        for _ in range(6):
            block.countercw()
        assert 0 <= block.rotation[-1] < len(block.states)
