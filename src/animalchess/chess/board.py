
from typing import Self

import numpy as np
from loguru import logger

from .utils import SquareType, Piece, AnimalType


BOARD_WIDTH = 7
BOARD_HEIGHT = 9


class AnimalChessBoardMap:    # this is a singleton
    def __init__(self):
        self._board = np.empty((BOARD_HEIGHT, BOARD_WIDTH), dtype=np.int8)
        self._board.fill(SquareType.LAND.value)
        self._board[0, 2] = SquareType.TRAP.value
        self._board[0, 3] = SquareType.CAVE.value
        self._board[0, 4] = SquareType.TRAP.value
        self._board[1, 3] = SquareType.TRAP.value
        self._board[8, 2] = SquareType.TRAP.value
        self._board[8, 3] = SquareType.CAVE.value
        self._board[8, 4] = SquareType.TRAP.value
        self._board[7, 3] = SquareType.TRAP.value
        for col in [1, 2, 4, 5]:
            for row in range(3, 6):
                self._board[row, col] = SquareType.WATER.value

    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, "_instance"):
            logger.info("Creating new AnimalChessBoardMap instance")
            cls._instance = super().__new__(cls)
        return cls._instance

    def get_square_type(self, row: int, col: int) -> SquareType:
        if row < 0 or row >= BOARD_HEIGHT or col < 0 or col >= BOARD_WIDTH:
            raise ValueError("Invalid square position")
        return SquareType(self._board[row, col])


class RatPiece(Piece):
    def _animal_type(self) -> AnimalType:
        return AnimalType.RAT

    def is_valid_move(
            self,
            initial_position: tuple[int, int],
            final_position: tuple[int, int]
    ) -> bool:
        if initial_position[0] < 0 or initial_position[0] >= BOARD_HEIGHT or initial_position[1] < 0 or initial_position[1] >= BOARD_WIDTH:
            raise ValueError("Invalid initial position")
        if final_position[0] < 0 or final_position[0] >= BOARD_HEIGHT or final_position[1] < 0 or final_position[1] >= BOARD_WIDTH:
            raise ValueError("Invalid final position")

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
