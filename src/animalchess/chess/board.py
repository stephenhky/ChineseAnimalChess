
from typing import Literal, Generator
from dataclasses import dataclass

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

    def move_piece(
            self,
            player_id: Literal[0, 1],
            animal: AnimalType,
            destination: tuple[int, int]
    ) -> bool:   # success: True; failed: False
        piece_info = self._players_possessions[player_id].get_piece(animal)
        if piece_info.piece.dead:
            logger.info(f"Player {self._players_possessions[player_id].player.name}: {piece_info.piece.animal_type.name} is dead")
            return False

        if not piece_info.piece.is_valid_move():
            logger.info("Not a valid move.")
            return False


