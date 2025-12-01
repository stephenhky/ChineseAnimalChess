
import unittest
from random import choice
from itertools import product

from animalchess.chess.utils import AnimalType, BOARD_HEIGHT, BOARD_WIDTH
from animalchess.chess.player import Player
from animalchess.chess.board import AnimalChessBoard


class TestCloneBoard(unittest.TestCase):
    def test_clone_1(self):
        player0 = Player("Alice")
        player1 = Player("Bob")
        board = AnimalChessBoard(player0, player1)

        for _ in range(5):
            # player 0
            # randomly pick animal type
            picked_animal_type = AnimalType(choice(range(len(AnimalType))))
            picked_position = choice(
                list(
                    board.exhaustively_iterate_available_destinations(0, picked_animal_type)
                )
            )
            board.move_piece(0, picked_animal_type, picked_position)

            # player 1
            picked_animal_type = AnimalType(choice(range(len(AnimalType))))
            picked_position = choice(
                list(
                    board.exhaustively_iterate_available_destinations(1, picked_animal_type)
                )
            )
            board.move_piece(1, picked_animal_type, picked_position)

        # cloning
        cloned_board = board.clone()

        # test cloned
        self.assertIsNot(board, cloned_board)
        self.assertIs(board._player0, cloned_board._player0)
        self.assertIs(board._player1, cloned_board._player1)
        self.assertIsNot(board._players_possessions[0], cloned_board._players_possessions[1])
        for player_id in [0, 1]:
            for animal_type, piece_info in board._players_possessions[player_id]._pieces.items():
                self.assertIsNot(
                    piece_info.piece,
                    cloned_board._players_possessions[player_id]._pieces[animal_type].piece
                )
                self.assertIs(
                    piece_info.piece.player,
                    cloned_board._players_possessions[player_id]._pieces[animal_type].piece.player
                )
                self.assertEqual(
                    piece_info.position,
                    cloned_board._players_possessions[player_id]._pieces[animal_type].position
                )
        for i, j in product(range(BOARD_HEIGHT), range(BOARD_WIDTH)):
            if board._board[i, j] is not None:
                original_piece = board._board[i, j]
                cloned_piece = cloned_board._board[i, j]
                self.assertIsNotNone(cloned_piece)
                self.assertIs(original_piece.player, cloned_piece.player)
                self.assertEqual(original_piece.dead, cloned_piece.dead)
                self.assertEqual(original_piece.animal_type, cloned_piece.animal_type)
            else:
                self.assertIsNone(cloned_board._board[i, j])


if __name__ == '__main__':
    unittest.main()

