from mcpi.vec3 import Vec3
from typing import *
from enum import *
from abc import *
from dataclasses import *


class Node(Protocol):
    """Interface"""
    ...


@unique
class CellType(StrEnum):
    # Base cells.
    EMPTY = auto()
    REGULAR = auto()
    # Special cells.
    LEVEL_ACCESS = auto()
    ENTRANCE = auto()
    POOL = auto()


class NeighbouringCells(TypedDict):
    # Horizontal.
    NORTH: Cell | None
    SOUTH: Cell | None
    EAST: Cell | None
    WEST: Cell | None
    # Vertical.
    UP: Cell | None
    DOWN: Cell | None


class Cell:
    def __init__(
            self,
            center_pos: Vec3,
            /, *,
            cell_type: CellType,
            neighbours: NeighbouringCells
    ):
        self.__pos: Final[Vec3] = center_pos
        self.__type: Final[CellType] = cell_type

        self.__neighbours: Final[NeighbouringCells] = neighbours
        self.__connected_cells: Set[Cell] = set()

    def add_connected_cell(self, other: Cell) -> NoReturn:
        assert other not in self.__connected_cells, f'{other} is already in connected_cells'
        assert any([other == neighbour
                    for neighbour in self.__neighbours.values()]), f'{other} is not a neighbour of {self}'
        self.__connected_cells.add(other)

    def __len__(self):
        return len(self.__connected_cells)

    def __repr__(self):
        return f"Cell({str(self.__pos)}, {self.__type})"

    def __eq__(self, other):
        return self.__pos == other.__pos

    def __hash__(self):
        # Don't allow overlapping cells.
        return hash(self.__pos)  # Use default mcpi.vec3 hashing.

    @property
    def get_connected_cells(self) -> Set[Cell]:
        return self.__connected_cells

    @property
    def get_cell_type(self) -> CellType:
        return self.__type

    @property
    def get_neigbours(self) -> NeighbouringCells:
        return self.__neighbours
