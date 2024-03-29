from __future__ import annotations
from mcpi.vec3 import Vec3

from typing import (
    TypedDict,
    Optional,
    Final,
    Set,
    Self,
    NoReturn,
    Tuple,
)
from enum import (
    StrEnum,
    unique,
    auto,
)

__all__ = [
    'CellType',
    'CellDirection',
    'NeighbouringCells',
    'Cell',
]


@unique
class CellType(StrEnum):
    DETACHED = auto()  # Not part of structure.
    # Cells that are part of the visible structure.
    STRUCTURE_ENTRY = auto()
    LEVEL_ENTRY = auto()
    ABOVE_LEVEL_ENTRY = auto()
    REGULAR = auto()
    EMPTY = auto()
    POOL = auto()


@unique
class CellDirection(StrEnum):
    NORTH = 'NORTH'
    SOUTH = 'SOUTH'
    EAST = 'EAST'
    WEST = 'WEST'
    UP = 'UP'
    DOWN = 'DOWN'


class NeighbouringCells(TypedDict):
    """Contains references to neighbouring cells."""
    # X-Axis.
    NORTH: Optional[Cell]
    SOUTH: Optional[Cell]
    # Z-Axis.
    EAST: Optional[Cell]
    WEST: Optional[Cell]
    # Y-Axis.
    UP: Optional[Cell]
    DOWN: Optional[Cell]


class Cell:

    def __init__(
            self,
            center_pos: Vec3,
            /,
            cell_type: CellType,
            *,
            neighbours: Optional[NeighbouringCells] = None
    ):
        self.pos: Final = center_pos
        self._type: CellType = cell_type
        self._neighbours: NeighbouringCells = neighbours \
            if neighbours else dict.fromkeys(NeighbouringCells.__required_keys__)
        # Cells that coalesce to form a larger cell.
        self._merged_cells: Set[Cell] = set()

    def add_merged_cell(self, other: Cell) -> NoReturn:
        assert other not in self._merged_cells, \
            f'{other!r} is already in connected_cells'
        assert any([other == neighbour for neighbour in self._neighbours.values()]), \
            f'{other!r} is not a neighbour of {self!r}'
        self._merged_cells.add(other)

    def get_merged_directions(self) -> Tuple[CellDirection, ...]:
        return tuple(
            [CellDirection[direction]
             for direction, neighbour in self._neighbours.items()
             if neighbour in self._merged_cells]
        )

    def faces_environment(self) -> bool:
        return any(
            [neighbour is None or neighbour._type == CellType.DETACHED
                for neighbour in self._neighbours.values()]
        )

    def faces_environment_direction(self) -> Tuple[CellDirection, ...]:
        return tuple(
            [CellDirection[direction]
             for direction, neighbour in self._neighbours.items()
             if neighbour is None or neighbour._type == CellType.DETACHED]
        )

    def faces_internal_directions(self) -> Tuple[CellDirection, ...]:
        return tuple(
            [CellDirection[internal_direction]
             for internal_direction in CellDirection
             if internal_direction not in self.faces_environment_direction()]
        )

    def __len__(self) -> int:
        return len(self._merged_cells)

    def __repr__(self) -> str:
        return f"Cell({str(self.pos)}, type: {self._type}, merged: {len(self)})"

    def __eq__(self, other) -> bool:
        return False if other is None else self.pos == other.pos

    def __hash__(self) -> int:
        assert self.pos is not None, f'{self!r} has no position'
        # Don't allow overlapping cells.
        return hash((self.pos.x, self.pos.y, self.pos.z))

    @property
    def connected_cells(self) -> Set[Cell]:
        return self._merged_cells

    @property
    def type_(self) -> CellType:
        return self._type

    @type_.setter
    def type_(self, new_type: CellType) -> NoReturn:
        self._type = new_type

    @property
    def neighbours(self) -> NeighbouringCells:
        return self._neighbours

    @neighbours.setter
    def neighbours(self, neighbours: NeighbouringCells) -> NoReturn:
        self._neighbours = neighbours
