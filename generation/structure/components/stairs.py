from __future__ import annotations
from generation import connection as server_conn
from generation.structure.utils.block_extension \
    import BlockExt as BlocEx
from generation.structure.env import MaterialPack
from mcpi.vec3 import Vec3

from typing import (
    runtime_checkable,
    NoReturn,
    Protocol,
    Final,
    final,
)
from enum import (
    StrEnum,
    unique,
    auto,
)

__all__ = [
    'StairType',
    'Stair',
    'StairFactory',
]


@unique
class StairType(StrEnum):
    SINGLE = auto()
    DOUBLE = auto()
    DOUBLE_SLAB = auto()


@runtime_checkable
class Stair(Protocol):
    """Stair Interface."""
    def set_current_stairs(self):
        """
        Stair placement of the current room.
        Independent of room dimensions.
        """

    def clear_room(self):
        """Clear internal space of the cell_center."""

    def set_above_stairs(self):
        """
        Stair placement of the above room.
        Independent of room dimensions.
        """


class SingleStair:
    def __init__(
            self,
            cell_center: Vec3,
            /,
            materials: MaterialPack,
    ) -> NoReturn:
        self._materials: Final = materials
        self._cell_center: Final = cell_center

    def set_current_stairs(self):
        cell_center: Vec3 = self._cell_center
        server_conn.setBlocks(
            cell_center + Vec3(1, 4, 1),
            cell_center + Vec3(2, 4, 3),
            self._materials['upstairs_floor'],
        )
        server_conn.setBlocks(
            cell_center + Vec3(3, 4, 1),
            cell_center + Vec3(3, 4, 3),
            BlocEx['AIR'],
        )
        server_conn.setBlock(
            cell_center + Vec3(3, 1, 1),
            self._materials['stairs'],
            2,
        )
        server_conn.setBlock(
            cell_center + Vec3(3, 2, 2),
            self._materials['stairs'],
            2,
        )
        server_conn.setBlock(
            cell_center + Vec3(3, 3, 3),
            self._materials['stairs'],
            2,
        )
        server_conn.setBlocks(
            cell_center + Vec3(4, 0, 1),
            cell_center + Vec3(4, 4, 3),
            self._materials['walls'],
        )
    
    def clear_room(self):
        cell_center: Vec3 = self._cell_center
        server_conn.setBlocks(
            cell_center + Vec3(1, 5, 1),
            cell_center + Vec3(3, 5, 3),
            BlocEx['AIR']
        )
        
    def set_above_stairs(self):
        cell_center: Vec3 = self._cell_center
        server_conn.setBlocks(
            cell_center + Vec3(1, 0, 1),
            cell_center + Vec3(2, 0, 3),
            self._materials['upstairs_floor'],
        )
        server_conn.setBlocks(
            cell_center + Vec3(3, 0, 1),
            cell_center + Vec3(3, 0, 3),
            BlocEx['AIR'],
        )


class DoubleStair(SingleStair):
    def set_current_stairs(self):
        cell_center: Vec3 = self._cell_center
        server_conn.setBlock(
            cell_center + Vec3(2, 1, 2),
            self._materials['stairs'],
            0,
        )
        server_conn.setBlock(
            cell_center + Vec3(3, 1, 2),
            self._materials['pillars']
        )
        server_conn.setBlock(
            cell_center + Vec3(3, 2, 1),
            self._materials['stairs'],
            3,
        )
        server_conn.setBlock(
            cell_center + Vec3(3, 2, 3),
            self._materials['stairs'],
            2,
        )
        server_conn.setBlock(
            cell_center + Vec3(2, 3, 1),
            self._materials['stairs'],
            1,
        )
        server_conn.setBlock(
            cell_center + Vec3(2, 3, 3),
            self._materials['stairs'],
            1,
        )
        server_conn.setBlocks(
            cell_center + Vec3(4, 0, 1),
            cell_center + Vec3(4, 4, 3),
            self._materials['walls'],
        )
        
    def clear_room(self):
        super().clear_room()

    def set_above_stairs(self):
        cell_center: Vec3 = self._cell_center
        server_conn.setBlocks(
            cell_center + Vec3(1, 0, 1),
            cell_center + Vec3(3, 0, 3),
            BlocEx['AIR'],
        )
        server_conn.setBlocks(
            cell_center + Vec3(1, 0, 1),
            cell_center + Vec3(1, 0, 3),
            self._materials['slab'],
            1,
        )
        server_conn.setBlock(
            cell_center + Vec3(2, 1, 2),
            self._materials['slab'],
        )
        server_conn.setBlock(
            cell_center + Vec3(3, 1, 2),
            self._materials['slab'],
        )


class DoubleSlabStair(SingleStair):
    def set_current_stairs(self):
        cell_center: Vec3 = self._cell_center
        server_conn.setBlocks(
            cell_center + Vec3(4, 0, 1),
            cell_center + Vec3(4, 4, 3),
            self._materials['walls'],
        )
        server_conn.setBlock(
            cell_center + Vec3(2, 1, 2),
            self._materials['slab']
        )
        server_conn.setBlock(
            cell_center + Vec3(3, 1, 2),
            self._materials['pillars']
        )
        server_conn.setBlock(
            cell_center + Vec3(3, 2, 1),
            self._materials['slab']
        )
        server_conn.setBlock(
            cell_center + Vec3(3, 2, 3),
            self._materials['slab']
        )
        server_conn.setBlock(
            cell_center + Vec3(2, 3, 1),
            self._materials['slab']
        )
        server_conn.setBlock(
            cell_center + Vec3(2, 3, 3),
            self._materials['slab']
        )

    def clear_room(self):
        super().clear_room()
        
    def set_above_stairs(self):
        cell_center: Vec3 = self._cell_center
        server_conn.setBlocks(
            cell_center + Vec3(1, 0, 1),
            cell_center + Vec3(3, 0, 3),
            BlocEx['AIR'],
        )
        server_conn.setBlocks(
            cell_center + Vec3(1, 0, 1),
            cell_center + Vec3(1, 0, 3),
            self._materials['slab'],
        )
        server_conn.setBlock(
            cell_center + Vec3(2, 0, 2),
            self._materials['slab']
        )
        server_conn.setBlock(
            cell_center + Vec3(3, 1, 2),
            self._materials['slab'],
        )


@final
class StairFactory:
    """Stair Factory. Does not retain ownership over produced instances."""
    __stair_types = {
        StairType.SINGLE: SingleStair,
        StairType.DOUBLE: DoubleStair,
        StairType.DOUBLE_SLAB: DoubleSlabStair,
    }

    @classmethod
    def create(
        cls,
        cell_center: Vec3,
        /,
        materials: MaterialPack,
        stair_type: StairType,
    ) -> Stair:
        return cls.__stair_types[stair_type](cell_center, materials)
