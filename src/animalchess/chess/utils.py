
from abc import ABC, abstractmethod
from enum import Enum
from typing import Self
from dataclasses import dataclass

from .player import Player


class AnimalType(Enum):   # specify the food chain
    RAT = 1
    CAT = 2
    DOG = 3
    WOLF = 4
    LEOPARD = 5
    TIGER = 6
    LION = 7
    ELEPHANT = 8


class Piece(ABC):
    def __init__(self, player: Player):
        self._player = player
        self._dead = False

    @abstractmethod
    def is_valid_move(
            self,
            initial_position: tuple[int, int],
            final_position: tuple[int, int]
    ) -> bool:   # does not account if the final position has another animal piece
        raise NotImplemented()

    @abstractmethod
    def _animal_type(self) -> AnimalType:
        raise NotImplemented()

    @property
    def animal_type(self) -> AnimalType:
        return self._animal_type()

    def __gt__(self, other: Self) -> bool:
        return self.animal_type.value > other.animal_type.value

    def __lt__(self, other: Self) -> bool:
        return self.animal_type.value < other.animal_type.value

    def __eq__(self, other: Self) -> bool:
        return self.animal_type.value == other.animal_type.value

    def __ge__(self, other: Self) -> bool:
        return (self > other) or (self == other)

    def __le__(self, other: Self) -> bool:
        return (self < other) or (self == other)

    def can_eat(self, other: Self) -> bool:
        return self >= other       # rule needed to be overriden for rat

    def die(self):
        self._dead = True

    @property
    def dead(self) -> bool:
        return self._dead


class SquareType(Enum):
    LAND = 1
    WATER = 2
    TRAP = 3
    CAVE = 4
