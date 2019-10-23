import unittest

class TestGame(unittest.TestCase):
    def test_game_init(self):
        from .game import Game
        game = Game()
        self.assertTrue(game)

