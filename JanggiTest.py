import unittest
from JanggiGame import Board, JanggiGame, Pieces


class MyTestCase(unittest.TestCase):
    def test_something(self):
        self.assertEqual(True, False)

    def test_get_board(self):
        board = Board()
        self.assertEqual(board.get_item_from_board(2, 1), 2)



if __name__ == '__main__':
    unittest.main()
