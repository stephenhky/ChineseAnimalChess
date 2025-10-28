
from typing import Self, Literal, Generator
from dataclasses import dataclass

import numpy as np

from .utils import SquareType, Piece, AnimalType, AnimalChessBoardMap
from .utils import BOARD_HEIGHT, BOARD_WIDTH
from .player import Player


class RatPiece(Piece):
    def _animal_type(self) -> AnimalType:
        return AnimalType.RAT

    def _livable_in_square_types(self) -> set[SquareType]:
        return {SquareType.LAND, SquareType.TRAP, SquareType.WATER}

    def is_valid_move(
            self,
            initial_position: tuple[int, int],
            final_position: tuple[int, int]
    ) -> bool:
        self._verify_position_move_within_range(initial_position, final_position)
        self._verify_initial_positions_livable(initial_position)

        if initial_position == final_position:
            return False

        if initial_position[0] == final_position[0]:
            return abs(initial_position[1] - final_position[1]) == 1
        elif initial_position[1] == final_position[1]:
            return abs(initial_position[0] - final_position[0]) == 1
        else:
            return False

    def can_eat(self, other: Self) -> bool:
        if (self.player is not other.player) and (other.animal_type == AnimalType.ELEPHANT):
            return True
        else:
            return super().can_eat(other)


class CatPiece(Piece):
    def _animal_type(self) -> AnimalType:
        return AnimalType.CAT

    def _livable_in_square_types(self) -> set[SquareType]:
        return {SquareType.LAND, SquareType.TRAP}

    def is_valid_move(
            self,
            initial_position: tuple[int, int],
            final_position: tuple[int, int]
    ) -> bool:
        self._verify_position_move_within_range(initial_position, final_position)
        self._verify_initial_positions_livable(initial_position)

        destination_square_type = self._map.get_square_type(*final_position)
        if not (self.livable(destination_square_type) or destination_square_type == SquareType.CAVE):
            return False

        if initial_position == final_position:
            return False

        if initial_position[0] == final_position[0]:
            return abs(initial_position[1] - final_position[1]) == 1
        elif initial_position[1] == final_position[1]:
            return abs(initial_position[0] - final_position[0]) == 1
        else:
            return False


class DogPiece(Piece):
    def _animal_type(self) -> AnimalType:
        return AnimalType.DOG

    def _livable_in_square_types(self) -> set[SquareType]:
        return {SquareType.LAND, SquareType.TRAP}

    def is_valid_move(
            self,
            initial_position: tuple[int, int],
            final_position: tuple[int, int]
    ) -> bool:
        self._verify_position_move_within_range(initial_position, final_position)
        self._verify_initial_positions_livable(initial_position)

        destination_square_type = self._map.get_square_type(*final_position)
        if not (self.livable(destination_square_type) or destination_square_type == SquareType.CAVE):
            return False

        if initial_position == final_position:
            return False

        if initial_position[0] == final_position[0]:
            return abs(initial_position[1] - final_position[1]) == 1
        elif initial_position[1] == final_position[1]:
            return abs(initial_position[0] - final_position[0]) == 1
        else:
            return False


class WolfPiece(Piece):
    def _animal_type(self) -> AnimalType:
        return AnimalType.WOLF

    def _livable_in_square_types(self) -> set[SquareType]:
        return {SquareType.LAND, SquareType.TRAP}

    def is_valid_move(
            self,
            initial_position: tuple[int, int],
            final_position: tuple[int, int]
    ) -> bool:
        self._verify_position_move_within_range(initial_position, final_position)
        self._verify_initial_positions_livable(initial_position)

        destination_square_type = self._map.get_square_type(*final_position)
        if not (self.livable(destination_square_type) or destination_square_type == SquareType.CAVE):
            return False

        if initial_position == final_position:
            return False

        if initial_position[0] == final_position[0]:
            return abs(initial_position[1] - final_position[1]) == 1
        elif initial_position[1] == final_position[1]:
            return abs(initial_position[0] - final_position[0]) == 1
        else:
            return False


class LeopardPiece(Piece):
    def _animal_type(self) -> AnimalType:
        return AnimalType.LEOPARD

    def _livable_in_square_types(self) -> set[SquareType]:
        return {SquareType.LAND, SquareType.TRAP}

    def is_valid_move(
            self,
            initial_position: tuple[int, int],
            final_position: tuple[int, int]
    ) -> bool:
        self._verify_position_move_within_range(initial_position, final_position)
        self._verify_initial_positions_livable(initial_position)

        destination_square_type = self._map.get_square_type(*final_position)
        if not (self.livable(destination_square_type) or destination_square_type == SquareType.CAVE):
            return False

        if initial_position == final_position:
            return False

        if initial_position[0] == final_position[0]:
            return abs(initial_position[1] - final_position[1]) == 1
        elif initial_position[1] == final_position[1]:
            return abs(initial_position[0] - final_position[0]) == 1
        else:
            return False


river_jumping_movement_set = {
    ((3, 0), (3, 3)),
    ((4, 0), (4, 3)),
    ((5, 0), (5, 3)),
    ((3, 3), (3, 6)),
    ((4, 3), (4, 6)),
    ((5, 3), (5, 6)),
    ((3, 3), (3, 0)),
    ((4, 3), (4, 0)),
    ((5, 3), (5, 0)),
    ((3, 6), (3, 3)),
    ((4, 6), (4, 3)),
    ((5, 6), (5, 3)),
    ((2, 1), (6, 1)),
    ((2, 2), (6, 2)),
    ((2, 4), (6, 4)),
    ((2, 5), (6, 5)),
    ((6, 1), (2, 1)),
    ((6, 2), (2, 2)),
    ((6, 4), (2, 4)),
    ((6, 5), (2, 5))
}


class TigerPiece(Piece):
    def _animal_type(self) -> AnimalType:
        return AnimalType.TIGER

    def _livable_in_square_types(self) -> set[SquareType]:
        return {SquareType.LAND, SquareType.TRAP}

    def is_valid_move(
            self,
            initial_position: tuple[int, int],
            final_position: tuple[int, int]
    ) -> bool:
        self._verify_position_move_within_range(initial_position, final_position)
        self._verify_initial_positions_livable(initial_position)

        destination_square_type = self._map.get_square_type(*final_position)
        if not (self.livable(destination_square_type) or destination_square_type == SquareType.CAVE):
            return False

        if initial_position == final_position:
            return False

        if (initial_position, final_position) in river_jumping_movement_set: # consider river jumping
            return True
        elif initial_position[0] == final_position[0]:
            return abs(initial_position[1] - final_position[1]) == 1
        elif initial_position[1] == final_position[1]:
            return abs(initial_position[0] - final_position[0]) == 1
        else:
            return False


class LionPiece(Piece):
    def _animal_type(self) -> AnimalType:
        return AnimalType.LION

    def _livable_in_square_types(self) -> set[SquareType]:
        return {SquareType.LAND, SquareType.TRAP}

    def is_valid_move(
            self,
            initial_position: tuple[int, int],
            final_position: tuple[int, int]
    ) -> bool:
        self._verify_position_move_within_range(initial_position, final_position)
        self._verify_initial_positions_livable(initial_position)

        destination_square_type = self._map.get_square_type(*final_position)
        if not (self.livable(destination_square_type) or destination_square_type == SquareType.CAVE):
            return False

        if initial_position == final_position:
            return False

        if (initial_position, final_position) in river_jumping_movement_set: # consider river jumping
            return True
        elif initial_position[0] == final_position[0]:
            return abs(initial_position[1] - final_position[1]) == 1
        elif initial_position[1] == final_position[1]:
            return abs(initial_position[0] - final_position[0]) == 1
        else:
            return False


class ElephantPiece(Piece):
    def _animal_type(self) -> AnimalType:
        return AnimalType.ELEPHANT

    def _livable_in_square_types(self) -> set[SquareType]:
        return {SquareType.LAND, SquareType.TRAP}

    def is_valid_move(
            self,
            initial_position: tuple[int, int],
            final_position: tuple[int, int]
    ) -> bool:
        self._verify_position_move_within_range(initial_position, final_position)
        self._verify_initial_positions_livable(initial_position)

        destination_square_type = self._map.get_square_type(*final_position)
        if not (self.livable(destination_square_type) or destination_square_type == SquareType.CAVE):
            return False

        if initial_position == final_position:
            return False

        if initial_position[0] == final_position[0]:
            return abs(initial_position[1] - final_position[1]) == 1
        elif initial_position[1] == final_position[1]:
            return abs(initial_position[0] - final_position[0]) == 1
        else:
            return False


@dataclass
class PieceInformation:
    piece: Piece
    position: tuple[int, int]
    alive: bool = True


class PlayerPossession:
    def __init__(self, player: Player, id: Literal[0, 1], reset: bool = True):
        self._player = player
        self._pieces = {}
        if reset:
            self.initialize_pieces(id)

    def initialize_pieces(self, id: Literal[0, 1]):
        if id == 0:
            self._pieces = {
                AnimalType.LION: PieceInformation(LionPiece(self.player), (0, 0)),
                AnimalType.TIGER: PieceInformation(TigerPiece(self.player), (0, 7)),
                AnimalType.DOG: PieceInformation(DogPiece(self.player), (1, 1)),
                AnimalType.CAT: PieceInformation(CatPiece(self.player), (1, 5)),
                AnimalType.RAT: PieceInformation(RatPiece(self.player), (2, 0)),
                AnimalType.LEOPARD: PieceInformation(LeopardPiece(self.player), (2, 2)),
                AnimalType.WOLF: PieceInformation(WolfPiece(self.player), (2, 4)),
                AnimalType.ELEPHANT: PieceInformation(ElephantPiece(self.player), (2, 6))
            }
        else:
            self._pieces = {
                AnimalType.LION: PieceInformation(LionPiece(self.player), (8, 6)),
                AnimalType.TIGER: PieceInformation(TigerPiece(self.player), (8, 0),
                AnimalType.DOG: PieceInformation(DogPiece(self.player), (7, 5)),
                AnimalType.CAT: PieceInformation(CatPiece(self.player), (7, 1)),
                AnimalType.RAT: PieceInformation(RatPiece(self.player), (6, 6)),
                AnimalType.LEOPARD: PieceInformation(LeopardPiece(self.player), (6, 4)),
                AnimalType.WOLF: PieceInformation(WolfPiece(self.player), (6, 2)),
                AnimalType.ELEPHANT: PieceInformation(ElephantPiece(self.player), (6, 0))
            }

    def get_piece(self, animal: AnimalType) -> PieceInformation:
        return self._pieces[animal]

    def iterate_living_pieces(self) -> Generator[PieceInformation, None, None]:
        for animal_piece_info in self._pieces.values():
            if animal_piece_info.alive:
                yield animal_piece_info

    @property
    def player(self) -> Player:
        return self._player


class AnimalChessBoard:
    def __init__(self, player1: Player, player2: Player):
        self._map = AnimalChessBoardMap()
        self._player1 = player1
        self._player2 = player2
        self.initialize_board()

    def initialize_board(self) -> None:
        self._player1_possession = PlayerPossession(self._player1, 0)
        self._player2_possession = PlayerPossession(self._player2, 1)

        self._board = np.empty((BOARD_HEIGHT, BOARD_WIDTH), dtype=object)
        for animal_piece_info in self._player1_possession.iterate_living_pieces():
            self._board[*animal_piece_info.position] = animal_piece_info.piece
        for animal_piece_info in self._player2_possession.iterate_living_pieces():
            self._board[*animal_piece_info.position] = animal_piece_info.piece

