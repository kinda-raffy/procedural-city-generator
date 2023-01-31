from __future__ import annotations
from generation import connection as server_conn
from generation.structure.components.door import DoorFactory, Door
from generation.structure.components.roof import Roof, RoofType, RoofFactory
from generation.structure.utils.block_extension import BlockExt as BlocEx
from generation.structure.env import MaterialPack
from mcpi.vec3 import Vec3

from abc import (
    ABCMeta,
    abstractmethod,
)
from enum import (
    Enum,
    unique,
    auto,
)
from typing import (
    NamedTuple,
    runtime_checkable,
    Protocol,
    NoReturn,
    Optional,
    Final,
    final,
)
import random

__all__ = [
    "VecRange",
    "JoinOrientation",
    "PoolStructureType",
    "Pool",
    "CellPool",
    "PoolStructure",
    "PoolStructureFactory",
    "PoolFacade",
]


class VecRange(NamedTuple):
    start: Vec3
    stop: Vec3


@unique
class JoinOrientation(Enum):
    HORIZONTAL = auto()
    VERTICAL = auto()


@unique
class PoolStructureType(Enum):
    INDOOR = auto()
    FENCED = auto()
    OUTDOOR = auto()


@runtime_checkable
class Pool(Protocol):
    """
    Pool is tasked with managing the container and ensuring an
    appropriate volume of water is maintained within.
    """

    def place_pool(self) -> NoReturn:
        """Places a pool container and fills its volume with water."""

    def place_pool_foundation(self) -> NoReturn:
        """Places the foundation for the pool."""

    def join_pools_horizontally(self) -> NoReturn:
        """
        Merges two cellular pools along a horizontal divider
        to create a more extensive pool.
        """

    def join_pools_vertically(self) -> NoReturn:
        """
        Merges two cellular pools along a horizontal divider
        to create a more extensive pool.
        """


class CellPool:
    """Implements the Pool interface. Generates a cell-wide pool."""

    def __init__(
        self,
        cell_center: Vec3,
        /,
        materials: MaterialPack,
    ):
        self._cell_center: Final = cell_center
        self._materials: Final = materials

    def place_pool(self) -> NoReturn:
        """Places a pool container and fills it with water."""
        cell_center = self._cell_center
        server_conn.setBlocks(
            cell_center + Vec3(1, 0, 1), cell_center + Vec3(3, 3, 3), BlocEx["AIR"]
        )
        # Create pool container.
        server_conn.setBlocks(
            cell_center, cell_center + Vec3(4, -2, 4), self._materials["pool_container"]
        )
        # Fill the pool with water.
        server_conn.setBlocks(
            cell_center + Vec3(1, 0, 1),
            cell_center + Vec3(3, -1, 3),
            self._materials["pool_liquid"],
        )
        # Destroy existing walls.
        server_conn.setBlocks(
            cell_center + Vec3(1, 1, 0), cell_center + Vec3(3, 3, 0), BlocEx["AIR"]
        )
        server_conn.setBlocks(
            cell_center + Vec3(1, 1, 4), cell_center + Vec3(3, 3, 4), BlocEx["AIR"]
        )
        server_conn.setBlocks(
            cell_center + Vec3(0, 1, 1), cell_center + Vec3(0, 3, 3), BlocEx["AIR"]
        )
        server_conn.setBlocks(
            cell_center + Vec3(4, 1, 1), cell_center + Vec3(4, 3, 3), BlocEx["AIR"]
        )

    def place_pool_foundation(self) -> NoReturn:
        cell_center = self._cell_center
        server_conn.setBlocks(
            cell_center + Vec3(0, -3, 0),
            cell_center + Vec3(4, -12, 4),
            self._materials["foundation"],
        )

    def join_pools_horizontally(self) -> NoReturn:
        cell_center = self._cell_center
        server_conn.setBlocks(
            cell_center + Vec3(4, -1, 1), cell_center + Vec3(4, 3, 3), BlocEx["AIR"]
        )

    def join_pools_vertically(self) -> NoReturn:
        cell_center = self._cell_center
        server_conn.setBlocks(
            cell_center + Vec3(1, -1, 0), cell_center + Vec3(3, 3, 0), BlocEx["AIR"]
        )


class PoolStructure(metaclass=ABCMeta):
    """
    PoolStructure is charged with overseeing the peripheral
    components of the pool environment, including doors,
    walls, pillars, and fences.
    """

    def __init__(
        self,
        cell_center: Vec3,
        /,
        material: MaterialPack,
        *,
        pool_roof: Roof,
    ) -> NoReturn:
        self._cell_center: Final = cell_center
        self._materials: Final = material
        self._pool_roof: Final = pool_roof

    @abstractmethod
    def create_structure(self) -> NoReturn:
        ...

    @abstractmethod
    def _add_pool_door(self, build_pos: VecRange) -> NoReturn:
        ...

    def _add_pillar(self, offset: Vec3) -> NoReturn:
        start_pos_pillar = self._cell_center + offset
        server_conn.setBlocks(
            start_pos_pillar,
            start_pos_pillar + Vec3(0, 4, 0),
            self._materials["pillars"],
        )

    def _add_pool_shade(self) -> NoReturn:
        # Stands.
        self._add_pillar(Vec3(0, 0, 0))
        self._add_pillar(Vec3(4, 0, 0))
        self._add_pillar(Vec3(4, 0, 4))
        self._add_pillar(Vec3(0, 0, 4))
        # Cover.
        self._pool_roof.place_base()
        self._pool_roof.place_corners()


class IndoorPoolStructure(PoolStructure):
    def create_structure(self) -> NoReturn:
        # North wall.
        north_pos: VecRange = VecRange(
            self._cell_center + Vec3(4, 1, 0), self._cell_center + Vec3(4, 3, 4)
        )
        self._add_pool_wall(north_pos)
        self._add_pool_door(north_pos)
        # East wall.
        east_pos: VecRange = VecRange(
            self._cell_center + Vec3(0, 1, 0), self._cell_center + Vec3(4, 3, 0)
        )
        self._add_pool_wall(east_pos)
        self._add_pool_door(east_pos)
        # South wall.
        south_pos: VecRange = VecRange(
            self._cell_center + Vec3(0, 1, 0), self._cell_center + Vec3(0, 3, 4)
        )
        self._add_pool_wall(south_pos)
        self._add_pool_door(south_pos)
        # West wall.
        west_pos: VecRange = VecRange(
            self._cell_center + Vec3(0, 1, 4), self._cell_center + Vec3(4, 3, 4)
        )
        self._add_pool_wall(west_pos)
        self._add_pool_door(west_pos)

        self._add_pool_shade()

    def _add_pool_door(self, build_pos: VecRange, /) -> NoReturn:
        is_horizontal: bool = build_pos.start.x == build_pos.stop.x
        is_vertical: bool = build_pos.start.z == build_pos.stop.z
        assert not (
            is_horizontal and is_vertical
        ), "Door must be horizontal or vertical."

        middle = Vec3(
            (build_pos.stop.x + build_pos.start.x) // 2,
            build_pos.start.y,
            (build_pos.stop.z + build_pos.start.z) // 2,
        )
        is_outdoors: bool = self._is_outdoors(build_pos.start + Vec3(1, 2, 0))
        if is_horizontal and not is_outdoors:
            door: Door = DoorFactory.create(middle, self._materials)
            door.place_single_door()
        is_outdoors: bool = self._is_outdoors(build_pos.start + Vec3(0, 3, 1))
        if is_vertical and not is_outdoors:
            door: Door = DoorFactory.create(middle, self._materials)
            door.place_single_door()

    def _add_pool_wall(self, build_pos: VecRange, /) -> NoReturn:
        server_conn.setBlocks(
            build_pos.start, build_pos.stop, self._materials["pool_wall"]
        )

    @staticmethod
    def _is_outdoors(pos: Vec3, /) -> bool:
        return server_conn.getBlock(pos) == BlocEx["AIR"]


class FencedPoolStructure(PoolStructure):
    def create_structure(self) -> NoReturn:
        self._add_pool_fence_west()
        self._add_pool_fence_north()
        self._add_pool_fence_south()
        self._add_pool_fence_east()

        self._add_pool_gates()
        # Pool shade generation.
        self._add_pool_shade() if random.randint(0, 1) > 0.6 else None

    def _add_pool_door(self, build_pos: VecRange) -> NoReturn:
        super(FencedPoolStructure, self)._add_pool_door(build_pos)

    def _add_pool_fence_north(self) -> NoReturn:
        cell_center = self._cell_center
        server_conn.setBlocks(
            cell_center + Vec3(4, 1, 1),
            cell_center + Vec3(4, 1, 3),
            self._materials["fence"],
        )
        self._place_fence_pillar_join(cell_center + Vec3(4, 1, 0))
        self._place_fence_pillar_join(cell_center + Vec3(4, 1, 4))

    def _add_pool_fence_west(self) -> NoReturn:
        cell_center = self._cell_center
        server_conn.setBlocks(
            cell_center + Vec3(1, 1, 0),
            cell_center + Vec3(3, 1, 0),
            self._materials["fence"],
        )
        self._place_fence_pillar_join(cell_center + Vec3(0, 1, 0))
        self._place_fence_pillar_join(cell_center + Vec3(4, 1, 0))

    def _add_pool_fence_south(self) -> NoReturn:
        cell_center = self._cell_center
        server_conn.setBlocks(
            cell_center + Vec3(0, 1, 1),
            cell_center + Vec3(0, 1, 3),
            self._materials["fence"],
        )
        self._place_fence_pillar_join(cell_center + Vec3(0, 1, 0))
        self._place_fence_pillar_join(cell_center + Vec3(0, 1, 4))

    def _add_pool_fence_east(self) -> NoReturn:
        cell_center = self._cell_center
        server_conn.setBlocks(
            cell_center + Vec3(1, 1, 4),
            cell_center + Vec3(3, 1, 4),
            self._materials["fence"],
        )
        self._place_fence_pillar_join(cell_center + Vec3(0, 1, 4))
        self._place_fence_pillar_join(cell_center + Vec3(4, 1, 4))

    def _add_pool_gates(self) -> NoReturn:
        cell_center = self._cell_center

        server_conn.setBlock(
            cell_center + Vec3(0, 1, 2), self._materials["fence_gate"], 1
        )
        server_conn.setBlock(
            cell_center + Vec3(4, 1, 2),
            self._materials["fence_gate"],
            1,
        )
        server_conn.setBlock(
            cell_center + Vec3(2, 1, 4),
            self._materials["fence_gate"],
            2,
        )
        server_conn.setBlock(
            cell_center + Vec3(2, 1, 0), self._materials["fence_gate"], 2
        )

    def _place_fence_pillar_join(
        self, pos: Vec3, y_offset: Optional[int] = 1
    ) -> NoReturn:
        above_pos = pos + Vec3(0, y_offset, 0)
        block_above_is_air: bool = server_conn.getBlock(above_pos) == BlocEx["AIR"]
        if block_above_is_air:
            server_conn.setBlock(pos, self._materials["fence"])
        else:
            server_conn.setBlock(pos, self._materials["pillars"])


class OutdoorPoolStructure(FencedPoolStructure, IndoorPoolStructure):
    """
    Pool structure features an outdoor fenced perimeter and internal
    house-facing walls.
    """

    def create_structure(self) -> NoReturn:
        # TODO ~ Check if door placement overrides the roof
        #  and update values accordingly.
        # Resolution order for create_structure() ~
        #  OutdoorPoolStructure, FencedPoolStructure, End.
        super(OutdoorPoolStructure, self).create_structure()
        cell_center = self._cell_center

        # North.
        north_pos: VecRange = VecRange(
            cell_center + Vec3(4, 1, 1), cell_center + Vec3(4, 3, 3)
        )
        self._add_pool_wall(north_pos)
        self._add_pool_door(north_pos)
        # South.
        south_pos: VecRange = VecRange(
            cell_center + Vec3(0, 1, 1), cell_center + Vec3(0, 3, 3)
        )
        self._add_pool_wall(south_pos)
        self._add_pool_door(south_pos)
        # West.
        west_pos: VecRange = VecRange(
            cell_center + Vec3(1, 1, 0), cell_center + Vec3(3, 3, 0)
        )
        self._add_pool_wall(west_pos)
        self._add_pool_door(west_pos)
        # East.
        east_pos: VecRange = VecRange(
            cell_center + Vec3(1, 1, 4), cell_center + Vec3(3, 3, 4)
        )
        self._add_pool_wall(east_pos)
        self._add_pool_door(east_pos)

        # Pool shade has been generated by FencedPoolStructure.

    def _add_pool_wall(self, build_pos: VecRange, /) -> NoReturn:
        is_horizontal: bool = build_pos.start.x == build_pos.stop.x
        is_vertical: bool = build_pos.start.z == build_pos.stop.z
        assert not (
            is_horizontal and is_vertical
        ), "Wall must be either horizontal or vertical."

        is_outdoors: bool = self._is_outdoors(build_pos.start + Vec3(1, 2, 0))
        if is_horizontal and not is_outdoors:
            IndoorPoolStructure._add_pool_wall(self, build_pos)
        is_outdoors: bool = self._is_outdoors(build_pos.start + Vec3(0, 3, 1))
        if is_vertical and not is_outdoors:
            IndoorPoolStructure._add_pool_wall(self, build_pos)

    def _add_pool_door(self, build_pos: VecRange) -> NoReturn:
        IndoorPoolStructure._add_pool_door(self, build_pos)


@final
class PoolStructureFactory:
    """Pool Factory. Does not retain ownership over produced instances."""

    __pool_structures: Final = {
        PoolStructureType.INDOOR: IndoorPoolStructure,
        PoolStructureType.OUTDOOR: OutdoorPoolStructure,
        PoolStructureType.FENCED: FencedPoolStructure,
    }

    @classmethod
    def create(
        cls,
        cell_center: Vec3,
        /,
        material: MaterialPack,
        pool_type: PoolStructureType,
        *,
        pool_roof: RoofType,
    ) -> PoolStructure:
        """Create a pool structure of the specified type."""
        roof: Roof = RoofFactory.create(cell_center, material, pool_roof)
        return cls.__pool_structures[pool_type](cell_center, material, pool_roof=roof)


@final
class PoolFacade:
    """
    Handles the underlying setup, coordination
    and method execution for the PoolCell and
    PoolStructure classes.
    """

    def __init__(
        self,
        pool: Pool,
        /,
        pool_structure: PoolStructure,
    ) -> NoReturn:
        self._pool: Final = pool
        self._pool_structure: Final = pool_structure

    def build(self) -> NoReturn:
        # Must be done in order to prevent block overlap.
        self._pool.place_pool()
        self._pool_structure.create_structure()

    def create_larger_pool(self, pool_join: JoinOrientation, /) -> NoReturn:
        match pool_join:
            case JoinOrientation.VERTICAL:
                self._pool.join_pools_vertically()
            case JoinOrientation.HORIZONTAL:
                self._pool.join_pools_horizontally()
