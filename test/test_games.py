
import unittest

from animalchess.chess.board import AnimalChessBoard
from animalchess.chess.player import Player
from animalchess.chess.utils import AnimalType
from animalchess.chess.utils import SquareType


class TestGame(unittest.TestCase):
    def test_game1(self):
        # initialize the game
        player0, player1 = Player("Bob"), Player("Alice")
        board = AnimalChessBoard(player0, player1)
        board_map = board._map

        # round 1
        self.assertTrue(board.move_piece(0, AnimalType.LION, (1, 0)))
        self.assertTrue(board.move_piece(1, AnimalType.RAT, (5, 6)))

        # round 2
        self.assertTrue(board.move_piece(0, AnimalType.DOG, (1, 2)))
        self.assertTrue(board.move_piece(1, AnimalType.RAT, (5, 5)))

        self.assertEqual(
            board_map.get_square_type(*board._players_possessions[1].get_piece(AnimalType.RAT).position),
            SquareType.WATER
        )

        # round 3
        self.assertTrue(board.move_piece(0, AnimalType.DOG, (1, 3)))
        self.assertTrue(board.move_piece(1, AnimalType.LION, (7, 6)))

        self.assertEqual(
            board_map.get_square_type(*board._players_possessions[0].get_piece(AnimalType.DOG).position),
            SquareType.TRAP0
        )

        # round 4
        self.assertTrue(board.move_piece(0, AnimalType.LION, (1, 1)))
        self.assertTrue(board.move_piece(1, AnimalType.LION, (6, 6)))

        # round 5
        self.assertTrue(board.move_piece(0, AnimalType.LION, (2, 1)))
        self.assertTrue(board.move_piece(1, AnimalType.LION, (5, 6)))

        # round 6
        self.assertTrue(board.move_piece(0, AnimalType.LION, (6, 1)))
        self.assertFalse(board.move_piece(1, AnimalType.LION, (5, 3)))
        self.assertTrue(board.move_piece(1, AnimalType.LION, (4, 6)))

        # round 7
        self.assertTrue(board.move_piece(0, AnimalType.LION, (6, 2)))
        self.assertTrue(board._players_possessions[1].get_piece(AnimalType.WOLF).piece.dead)
        self.assertTrue(board.move_piece(1, AnimalType.DOG, (7, 4)))

        # round 8
        self.assertTrue(board.move_piece(0, AnimalType.LION, (7, 2)))
        self.assertTrue(board.move_piece(1, AnimalType.DOG, (7, 3)))

        self.assertEqual(
            board_map.get_square_type(*board._players_possessions[1].get_piece(AnimalType.DOG).position),
            SquareType.TRAP1
        )

        # round 9
        self.assertFalse(board.move_piece(0, AnimalType.LION, (7, 3)))
        self.assertTrue(board.move_piece(0, AnimalType.LION, (8, 2)))
        self.assertTrue(board.move_piece(1, AnimalType.CAT, (7, 2)))

        self.assertEqual(
            board_map.get_square_type(*board._players_possessions[0].get_piece(AnimalType.LION).position),
            SquareType.TRAP1
        )

        # round 10
        self.assertTrue(board.move_piece(0, AnimalType.RAT, (3, 0)))
        self.assertTrue(board.move_piece(1, AnimalType.CAT, (8, 2)))
        self.assertTrue(board._players_possessions[0].get_piece(AnimalType.LION).piece.dead)

        # round 11
        self.assertTrue(board.move_piece(0, AnimalType.RAT, (4, 0)))
        self.assertTrue(board.move_piece(1, AnimalType.ELEPHANT, (5, 0)))

        # round 12
        self.assertTrue(board.move_piece(0, AnimalType.RAT, (5, 0)))
        self.assertTrue(board._players_possessions[1].get_piece(AnimalType.ELEPHANT).piece.dead)
        self.assertTrue(board.move_piece(1, AnimalType.LION, (4, 3)))

        # round 13
        self.assertTrue(board.move_piece(0, AnimalType.RAT, (6, 0)))
        self.assertTrue(board.move_piece(1, AnimalType.LION, (3, 3)))

        # round 14
        self.assertTrue(board.move_piece(0, AnimalType.RAT, (6, 1)))
        self.assertTrue(board.move_piece(1, AnimalType.DOG, (6, 3)))

        # round 15
        self.assertTrue(board.move_piece(0, AnimalType.RAT, (7, 1)))
        self.assertTrue(board.move_piece(1, AnimalType.CAT, (8, 1)))

        # round 16
        self.assertTrue(board.move_piece(0, AnimalType.RAT, (7, 2)))
        self.assertTrue(board.move_piece(1, AnimalType.CAT, (7, 1)))

        # round 17
        self.assertTrue(board.move_piece(0, AnimalType.RAT, (8, 2)))
        self.assertTrue(board.move_piece(1, AnimalType.DOG, (7, 3)))

        self.assertEqual(
            board_map.get_square_type(*board._players_possessions[0].get_piece(AnimalType.RAT).position),
            SquareType.TRAP1
        )

        # round 18
        self.assertTrue(board.move_piece(0, AnimalType.ELEPHANT, (3, 6)))
        self.assertFalse(board.move_piece(1, AnimalType.DOG, (8, 3)))
        self.assertTrue(board.move_piece(1, AnimalType.CAT, (7, 2)))

        # round 20
        self.assertTrue(board.move_piece(0, AnimalType.RAT, (8, 3)))
        self.assertTrue(board._players_possessions[0].winned)
        self.assertFalse(board._players_possessions[1].winned)


if __name__ == '__main__':
    unittest.main()
