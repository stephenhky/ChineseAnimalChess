
from typing import Self
import warnings

from .utils import SquareType, Piece, AnimalType, AnimalChessBoardMap





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
        if other.animal_type == AnimalType.ELEPHANT:
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
