
from typing import Literal, Generator
from dataclasses import dataclass
from itertools import product
import warnings

import numpy as np
from loguru import logger

from .utils import Piece, AnimalType, AnimalChessBoardMap
from .utils import BOARD_HEIGHT, BOARD_WIDTH
from .player import Player
from .pieces import RatPiece, CatPiece, DogPiece, LeopardPiece, WolfPiece, TigerPiece, LionPiece, ElephantPiece


@dataclass
class PieceInformation:
    piece: Piece
    position: tuple[int, int]


class PlayerPossession:
    def __init__(self, player: Player, id: Literal[0, 1], reset: bool = True):
        self._player = player
        self._pieces = {}
        if reset:
            self.initialize_pieces(id)

    def initialize_pieces(self, id: Literal[0, 1]) -> None:
        if id == 0:
            self._pieces = {
                AnimalType.LION: PieceInformation(LionPiece(self.player), (0, 0)),
                AnimalType.TIGER: PieceInformation(TigerPiece(self.player), (0, 6)),
                AnimalType.DOG: PieceInformation(DogPiece(self.player), (1, 1)),
                AnimalType.CAT: PieceInformation(CatPiece(self.player), (1, 5)),
                AnimalType.RAT: PieceInformation(RatPiece(self.player), (2, 0)),
                AnimalType.LEOPARD: PieceInformation(LeopardPiece(self.player), (2, 2)),
                AnimalType.WOLF: PieceInformation(WolfPiece(self.player), (2, 4)),
                AnimalType.ELEPHANT: PieceInformation(ElephantPiece(self.player), (2, 6))
            }
        elif id == 1:
            self._pieces = {
                AnimalType.LION: PieceInformation(LionPiece(self.player), (8, 6)),
                AnimalType.TIGER: PieceInformation(TigerPiece(self.player), (8, 0)),
                AnimalType.DOG: PieceInformation(DogPiece(self.player), (7, 5)),
                AnimalType.CAT: PieceInformation(CatPiece(self.player), (7, 1)),
                AnimalType.RAT: PieceInformation(RatPiece(self.player), (6, 6)),
                AnimalType.LEOPARD: PieceInformation(LeopardPiece(self.player), (6, 4)),
                AnimalType.WOLF: PieceInformation(WolfPiece(self.player), (6, 2)),
                AnimalType.ELEPHANT: PieceInformation(ElephantPiece(self.player), (6, 0))
            }
        else:
            raise ValueError("Player ID must be 0 or 1!")

    def get_piece(self, animal: AnimalType) -> PieceInformation:
        return self._pieces[animal]

    def iterate_living_pieces(self) -> Generator[PieceInformation, None, None]:
        for animal_piece_info in self._pieces.values():
            if not animal_piece_info.piece.dead:
                yield animal_piece_info

    @property
    def player(self) -> Player:
        return self._player


class AnimalChessBoard:
    def __init__(self, player0: Player, player1: Player):
        self._map = AnimalChessBoardMap()
        self._player0 = player0
        self._player1 = player1
        self.initialize_board()

    def initialize_board(self) -> None:
        self._players_possessions = [
            PlayerPossession(self._player0, 0),
            PlayerPossession(self._player1, 1)
        ]

        self._board = np.empty((BOARD_HEIGHT, BOARD_WIDTH), dtype=object)
        for possession in self._players_possessions:
            for animal_piece_info in possession.iterate_living_pieces():
                self._board[*animal_piece_info.position] = animal_piece_info.piece

    def _any_pieces_in_between(
        self,
        initial_position: tuple[int, int],
        destination_position: tuple[int, int]
    ) -> bool:
        if initial_position[0] == destination_position[0]:
            x = initial_position[0]
            for y in range(initial_position[1], destination_position[1], 1 if destination_position[1] > initial_position[1] else -1):
                if self._board[x, y] is not None and isinstance(self._board[x, y], PieceInformation):
                    return True
        elif initial_position[1] == destination_position[1]:
            y = initial_position[1]
            for x in range(initial_position[0], destination_position[0], 1 if destination_position[0] > initial_position[0] else -1):
                if self._board[x, y] is not None and isinstance(self._board[x, y], PieceInformation):
                    return True
        else:
            warnings.warn("Cannot check as it is not horizontal or vertical.")
        return False

    def _simply_move(
            self,
            player_id: Literal[0, 1],
            animal: AnimalType,
            destination: tuple[int, int]
    ) -> None:
        piece_info = self._players_possessions[player_id].get_piece(animal)
        initial_position = piece_info.position
        self._board[*initial_position] = None
        piece_info.position = destination
        self._board[*destination] = piece_info
                
    def move_piece(
            self,
            player_id: Literal[0, 1],
            animal: AnimalType,
            destination: tuple[int, int]
    ) -> bool:   # success: True; failed: False
        piece_info = self._players_possessions[player_id].get_piece(animal)
        piece = piece_info.piece
        if piece.dead:
            logger.info(f"Player {self._players_possessions[player_id].player.name}: {piece.animal_type.name} is dead")
            return False

        initial_position = piece_info.position
        if not piece.is_valid_move(initial_position, destination):
            logger.info("Not a valid move.")
            return False

        if self._any_pieces_in_between(initial_position, destination):
            logger.info("There are pieces in between.")
            return False

        if self._board[*destination] is not None and isinstance(self._board[*destination], PieceInformation):
            destination_piece_info = self._board[*destination]
            destination_piece = destination_piece_info.piece
            if not piece.can_eat(destination_piece):
                logger.info(f"{piece.animal_type.name} cannot eat {destination_piece.animal_type.name}!")
                return False
            else:
                # eat
                logger.info(f"{piece.animal_type.name} is eating {destination_piece.animal_type.name}!")
                destination_piece.die()
                destination_piece_info.position = None

                # simply move
                self._simply_move(player_id, animal, destination)
                return True

        # simple move
        self._simply_move(player_id, animal, destination)
        return True

    def get_board_array(self) -> np.ndarray:
        printboard = np.empty((BOARD_HEIGHT, BOARD_WIDTH), dtype=object)
        for i, j in product(range(BOARD_HEIGHT), range(BOARD_WIDTH)):
            if self._board[i, j] is not None:
                piece = self._board[i, j]
                printboard[i, j] = f"{piece.player.name}: {piece.animal_type.name}"
        return printboard
