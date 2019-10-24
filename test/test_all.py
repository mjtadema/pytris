import pytest

@pytest.fixture
def game():
    from pytris.game import Game
    return Game()

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

@pytest.fixture
def screen():
    #from pytris.screen import Screen
    #return Screen(debug = True)
    pass

def test_screen(screen):
    pass