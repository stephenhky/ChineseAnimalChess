
from itertools import product
import unittest

from animalchess.chess.board import AnimalChessBoard, PlayerPossession, BOARD_HEIGHT, BOARD_WIDTH
from animalchess.chess.player import Player
from animalchess.chess.utils import AnimalType, AnimalChessBoardMap, SquareType


class TestActions(unittest.TestCase):
    def setUp(self):
        self.player0 = Player("Player 0")
        self.player1 = Player("Player 1")
        self.board = AnimalChessBoard(self.player0, self.player1)

    def test_corner(self):
        player0_possession = PlayerPossession(self.player0, 0, reset=False)
        player1_possession = PlayerPossession(self.player1, 1, reset=False)
        player0_possession.set_piece_info(AnimalType.LION, (0, 0))
        player1_possession.set_piece_info(AnimalType.LION, (8, 6))
        board = AnimalChessBoard(
            self.player0,
            self.player1,
            initial_players_possessions=[player0_possession, player1_possession]
        )

        player0_lion_possible_destinations = [(0, 1), (1, 0)]
        player0_system_lion_possible_destinations = [
            (new_i, new_j)
            for new_i, new_j in board.exhaustively_iterate_available_destinations(0, AnimalType.LION)
        ]
        for i, j in product(range(BOARD_HEIGHT), range(BOARD_WIDTH)):
            if (i, j) in player0_lion_possible_destinations:
                self.assertIn((i, j), player0_system_lion_possible_destinations)
            else:
                self.assertFalse((i, j) in player0_system_lion_possible_destinations)

        player1_lion_possible_destinations = [(8, 5), (7, 6)]
        player1_system_lion_possible_destinations = [
            (new_i, new_j)
            for new_i, new_j in board.exhaustively_iterate_available_destinations(1, AnimalType.LION)
        ]
        for i, j in product(range(BOARD_HEIGHT), range(BOARD_WIDTH)):
            if (i, j) in player1_lion_possible_destinations:
                self.assertIn((i, j), player1_system_lion_possible_destinations)
            else:
                self.assertFalse((i, j) in player1_system_lion_possible_destinations)

    def test_jumps(self):
        player0_possession = PlayerPossession(self.player0, 0, reset=False)
        player1_possession = PlayerPossession(self.player1, 1, reset=False)
        player0_possession.set_piece_info(AnimalType.LION, (3, 3))
        player0_possession.set_piece_info(AnimalType.RAT, (3, 2))
        player1_possession.set_piece_info(AnimalType.LION, (6, 1))
        board = AnimalChessBoard(
            self.player0,
            self.player1,
            initial_players_possessions=[player0_possession, player1_possession]
        )

        player0_lion_possible_destinations = [(2, 3), (4, 3), (3, 6)]
        player0_system_lion_possible_destinations = [
            (new_i, new_j)
            for new_i, new_j in board.exhaustively_iterate_available_destinations(0, AnimalType.LION)
        ]
        for i, j in product(range(BOARD_HEIGHT), range(BOARD_WIDTH)):
            if (i, j) in player0_lion_possible_destinations:
                self.assertIn((i, j), player0_system_lion_possible_destinations)
            else:
                self.assertFalse((i, j) in player0_system_lion_possible_destinations)

        player1_lion_possible_destinations = [(6, 0), (6, 2), (7, 1), (2, 1)]
        player1_system_lion_possible_destinations = [
            (new_i, new_j)
            for new_i, new_j in board.exhaustively_iterate_available_destinations(1, AnimalType.LION)
        ]
        for i, j in product(range(BOARD_HEIGHT), range(BOARD_WIDTH)):
            if (i, j) in player1_lion_possible_destinations:
                self.assertIn((i, j), player1_system_lion_possible_destinations)
            else:
                self.assertFalse((i, j) in player1_system_lion_possible_destinations)

        # test the rat amphibian moves
        player0_rat_possible_destinations = [(3, 1), (2, 2), (4, 2)]
        player0_system_rat_possible_destinations = [
            (new_i, new_j)
            for new_i, new_j in board.exhaustively_iterate_available_destinations(0, AnimalType.RAT)
        ]
        for i, j in product(range(BOARD_HEIGHT), range(BOARD_WIDTH)):
            if (i, j) in player0_rat_possible_destinations:
                self.assertIn((i, j), player0_system_rat_possible_destinations)
            else:
                self.assertFalse((i, j) in player0_system_rat_possible_destinations)

    def test_ordinary_moves(self):
        player0_possession = PlayerPossession(self.player0, 0, reset=False)
        player1_possession = PlayerPossession(self.player1, 1, reset=False)
        player0_possession.set_piece_info(AnimalType.DOG, (1, 1))
        player1_possession.set_piece_info(AnimalType.CAT, (7, 1))
        board = AnimalChessBoard(
            self.player0,
            self.player1,
            initial_players_possessions=[player0_possession, player1_possession]
        )

        player0_dog_possible_destinations = [(0, 1), (1, 0), (1, 2), (2, 1)]
        player0_system_dog_possible_destinations = [
            (new_i, new_j)
            for new_i, new_j in board.exhaustively_iterate_available_destinations(0, AnimalType.DOG)
        ]
        for i, j in product(range(BOARD_HEIGHT), range(BOARD_WIDTH)):
            if (i, j) in player0_dog_possible_destinations:
                self.assertIn((i, j), player0_system_dog_possible_destinations)
            else:
                self.assertFalse((i, j) in player0_system_dog_possible_destinations)

        player1_cat_possible_destinations = [(6, 1), (8, 1), (7, 0), (7, 2)]
        player1_system_cat_possible_destinations = [
            (new_i, new_j)
            for new_i, new_j in board.exhaustively_iterate_available_destinations(1, AnimalType.CAT)
        ]
        for i, j in product(range(BOARD_HEIGHT), range(BOARD_WIDTH)):
            if (i, j) in player1_cat_possible_destinations:
                self.assertIn((i, j), player1_system_cat_possible_destinations)
            else:
                self.assertFalse((i, j) in player1_system_cat_possible_destinations)

    def test_player0_cave_trap(self):
        player0_possession = PlayerPossession(self.player0, 0, reset=False)
        player1_possession = PlayerPossession(self.player1, 1, reset=False)
        player0_possession.set_piece_info(AnimalType.DOG, (0, 2))
        player1_possession.set_piece_info(AnimalType.LION, (0, 1))
        player0_possession.set_piece_info(AnimalType.RAT, (1, 4))
        player1_possession.set_piece_info(AnimalType.TIGER, (1, 3))
        board = AnimalChessBoard(
            self.player0,
            self.player1,
            initial_players_possessions=[player0_possession, player1_possession]
        )

        player0_dog_possible_destinations = [(1, 2)]
        player0_system_dog_possible_destinations = [
            (new_i, new_j)
            for new_i, new_j in board.exhaustively_iterate_available_destinations(0, AnimalType.DOG)
        ]
        for i, j in product(range(BOARD_HEIGHT), range(BOARD_WIDTH)):
            if (i, j) in player0_dog_possible_destinations:
                self.assertIn((i, j), player0_system_dog_possible_destinations)
            else:
                self.assertFalse((i, j) in player0_system_dog_possible_destinations)

        player1_lion_possible_destinations = [(0, 0), (1, 1)]
        player1_system_lion_possible_destinations = [
            (new_i, new_j)
            for new_i, new_j in board.exhaustively_iterate_available_destinations(1, AnimalType.LION)
        ]
        for i, j in product(range(BOARD_HEIGHT), range(BOARD_WIDTH)):
            if (i, j) in player1_lion_possible_destinations:
                self.assertIn((i, j), player1_system_lion_possible_destinations)
            else:
                self.assertFalse((i, j) in player1_system_lion_possible_destinations)

        player0_rat_possible_destinations = [(1, 3), (2, 4), (1, 5), (0, 4)]
        player0_system_rat_possible_destinations = [
            (new_i, new_j)
            for new_i, new_j in board.exhaustively_iterate_available_destinations(0, AnimalType.RAT)
        ]
        for i, j in product(range(BOARD_HEIGHT), range(BOARD_WIDTH)):
            if (i, j) in player0_rat_possible_destinations:
                self.assertIn((i, j), player0_system_rat_possible_destinations)
            else:
                self.assertFalse((i, j) in player0_system_rat_possible_destinations)

        player1_tiger_possible_destinations = [(1, 2), (1, 4), (2, 3), (0, 3)]
        player1_system_tiger_possible_destinations = [
            (new_i, new_j)
            for new_i, new_j in board.exhaustively_iterate_available_destinations(1, AnimalType.TIGER)
        ]
        for i, j in product(range(BOARD_HEIGHT), range(BOARD_WIDTH)):
            if (i, j) in player1_tiger_possible_destinations:
                self.assertIn((i, j), player1_system_tiger_possible_destinations)
            else:
                self.assertFalse((i, j) in player1_system_tiger_possible_destinations)

    def test_player1_cave_trap(self):
        player0_possession = PlayerPossession(self.player0, 0, reset=False)
        player1_possession = PlayerPossession(self.player1, 1, reset=False)
        player0_possession.set_piece_info(AnimalType.DOG, (8, 1))
        player1_possession.set_piece_info(AnimalType.LEOPARD, (8, 2))
        player0_possession.set_piece_info(AnimalType.LION, (7, 3))
        player1_possession.set_piece_info(AnimalType.CAT, (7, 2))
        board = AnimalChessBoard(
            self.player0,
            self.player1,
            initial_players_possessions=[player0_possession, player1_possession]
        )

        player0_dog_possible_destinations = [(8, 0), (7, 1)]
        player0_system_dog_possible_destinations = [
            (new_i, new_j)
            for new_i, new_j in board.exhaustively_iterate_available_destinations(0, AnimalType.DOG)
        ]
        for i, j in product(range(BOARD_HEIGHT), range(BOARD_WIDTH)):
            if (i, j) in player0_dog_possible_destinations:
                self.assertIn((i, j), player0_system_dog_possible_destinations)
            else:
                self.assertFalse((i, j) in player0_system_dog_possible_destinations)

        player1_leopard_possible_destinations = [(8, 1)]
        player1_system_leopard_possible_destinations = [
            (new_i, new_j)
            for new_i, new_j in board.exhaustively_iterate_available_destinations(1, AnimalType.LEOPARD)
        ]
        for i, j in product(range(BOARD_HEIGHT), range(BOARD_WIDTH)):
            if (i, j) in player1_leopard_possible_destinations:
                self.assertIn((i, j), player1_system_leopard_possible_destinations)
            else:
                self.assertFalse((i, j) in player1_system_leopard_possible_destinations)

        player0_lion_possible_destinations = [(7, 2), (6, 3), (8, 3), (7, 4)]
        player0_system_lion_possible_destinations = [
            (new_i, new_j)
            for new_i, new_j in board.exhaustively_iterate_available_destinations(0, AnimalType.LION)
        ]
        for i, j in product(range(BOARD_HEIGHT), range(BOARD_WIDTH)):
            if (i, j) in player0_lion_possible_destinations:
                self.assertIn((i, j), player0_system_lion_possible_destinations)
            else:
                self.assertFalse((i, j) in player0_system_lion_possible_destinations)

        player1_cat_possible_destinations = [(7, 3), (6, 2), (7, 1)]
        player1_system_cat_possible_destinations = [
            (new_i, new_j)
            for new_i, new_j in board.exhaustively_iterate_available_destinations(1, AnimalType.CAT)
        ]
        print(player1_system_cat_possible_destinations)
        for i, j in product(range(BOARD_HEIGHT), range(BOARD_WIDTH)):
            if (i, j) in player1_cat_possible_destinations:
                self.assertIn((i, j), player1_system_cat_possible_destinations)
            else:
                self.assertFalse((i, j) in player1_system_cat_possible_destinations)


if __name__ == '__main__':
    unittest.main()
