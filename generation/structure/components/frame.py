from __future__ import annotations
from generation import connection as server_conn
from generation.structure.cell import (
    CellDirection,
    Cell
)
from generation.structure.env import MaterialPack
from generation.structure.utils.block_extension import BlockExt as BlocEx
from mcpi.vec3 import Vec3

from abc import (
    ABCMeta,
    abstractmethod,
)
from typing import (
    NoReturn,
    Final,
    Dict,
    Tuple, List,
)

__all__ = [
    'Frame',
    'DefaultFrame',
]


class Frame(metaclass=ABCMeta):
    """Frame Interface."""
    def __init__(
            self,
            cell: Cell,
            /,
            materials: MaterialPack,
            *,
            cell_dim: Vec3 = Vec3(4, 4, 4),
    ) -> NoReturn:
        self._cell: Final = cell
        self._cell_center: Final[Vec3] = cell.pos
        self._materials: Final = materials
        self._cell_dim: Final = cell_dim
        # TODO ~ Verify vectors.
        self._cell_direction_pos: Final[
            Dict[CellDirection, Vec3]
        ] = {
            CellDirection.NORTH: self._cell_center + Vec3(0, 0, 0),
            CellDirection.SOUTH: self._cell_center + Vec3(0, 0, self._cell_dim.z),
            CellDirection.EAST: self._cell_center + Vec3(self._cell_dim.x, 0, 0),
            CellDirection.WEST: self._cell_center + Vec3(0, 0, 0),
        }

    @abstractmethod
    def set_cell_frame(self) -> NoReturn:
        """Frame placement of the current room."""

    @abstractmethod
    def perform_cell_merge(self) -> NoReturn:
        """Removes walls based on the cell merge list."""

    @abstractmethod
    def _remove_cell_wall(self, direction) -> NoReturn:
        """Removes the wall of the current room at a certain direction."""

    @abstractmethod
    def set_cell_floor(self) -> NoReturn:
        """Floor placement dispatcher."""

    @abstractmethod
    def _set_ground_floor(self) -> NoReturn:
        """Ground floor and foundation placement."""

    @abstractmethod
    def _set_upstairs_floor(self) -> NoReturn:
        """Upstairs floor placement."""

    @abstractmethod
    def set_external_pillars(self) -> NoReturn:
        """Pillar placement on outside cell sides."""

    @abstractmethod
    def set_internal_pillars(self) -> NoReturn:
        """Pillar placement on internal cell sides."""


class DefaultFrame(Frame):

    def set_cell_frame(self, *, floor_offset: int = 1) -> NoReturn:
        center_pos: Vec3 = self._cell_center + Vec3(0, floor_offset, 0)
        cell_dim: Vec3 = self._cell_dim
        server_conn.setBlocks(
            center_pos,
            center_pos + cell_dim,
            self._materials['walls'],
        )
        frame_offset: Vec3 = Vec3(1, 0, 1)
        server_conn.setBlocks(
            center_pos + frame_offset,
            center_pos + cell_dim - frame_offset,
            BlocEx['AIR'],
        )

    def perform_cell_merge(self) -> NoReturn:
        to_merge_directions: Tuple[CellDirection, ...] = \
            self._cell.get_merged_directions()
        for direction in to_merge_directions:
            self._remove_cell_wall(direction)

    def _remove_cell_wall(self, direction) -> NoReturn:
        server_conn.setBlocks(
            self._cell_direction_pos[direction],
            self._cell_direction_pos[direction] + Vec3(0, self._cell_dim.y, 0),
            BlocEx['AIR'],
        )

    def set_cell_floor(self) -> NoReturn:
        is_ground_floor: bool = self._cell.neighbours['DOWN'] is None
        if is_ground_floor:
            self._set_ground_floor()
        else:
            self._set_upstairs_floor()

    def _set_ground_floor(self, *, foundation_depth: int = 15) -> NoReturn:
        cell_center: Vec3 = self._cell_center
        cell_dim: Vec3 = self._cell_dim
        server_conn.setBlocks(
            cell_center,
            cell_center + Vec3(cell_dim.x, -foundation_depth, cell_dim.z),
            self._materials['foundation'],
        )

    def set_external_pillars(self) -> NoReturn:
        external_sides: List[CellDirection, ...] = [
            direction for direction in self._cell.faces_environment_direction()
            if direction not in (CellDirection.UP, CellDirection.DOWN)
        ]
        for side in external_sides:
            self._set_pillar(side)

    def set_internal_pillars(self) -> NoReturn:
        internal_sides: List[CellDirection, ...] = [
            direction for direction in self._cell.faces_environment_direction()
            if direction not in (CellDirection.UP, CellDirection.DOWN)
        ]
        for side in internal_sides:
            self._set_pillar(side)

    def _set_pillar(self, direction: CellDirection) -> NoReturn:
        # TODO ~ Verify vectors.
        assert direction not in (CellDirection.UP, CellDirection.DOWN), \
            "Pillars may only be placed horizontally."
        server_conn.setBlocks(
            self._cell_direction_pos[direction],
            self._cell_direction_pos[direction] + Vec3(0, self._cell_dim.y, 0),
            self._materials['pillars'],
        )

    def _set_upstairs_floor(self) -> NoReturn:
        cell_center: Vec3 = self._cell_center
        cell_dim: Vec3 = self._cell_dim
        server_conn.setBlocks(
            cell_center,
            cell_center + Vec3(cell_dim.x, 0, cell_dim.z),
            self._materials['upstairs_floor'],
        )
