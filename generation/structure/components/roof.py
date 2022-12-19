from generation import connection as server_conn
from generation.structure.env import MaterialPack
from mcpi.vec3 import Vec3
from typing import *    # FIXME ~ Narrow
from enum import *      # FIXME ~ Narrow


@unique
class RoofType(StrEnum):
    DEFAULT = auto()
    FLAT = auto()
    ANGLED_FLAT = auto()
    STAIR_FLAT = auto()
    STAIR_MEDIUM = auto()


@runtime_checkable
class Roof(Protocol):
    """Roof Interface."""
    def place_base(self) -> NoReturn:
        """Places the essential roof elements."""

    def place_corners(self, *, deviation: Vec3 = Vec3(0, 0, 0)) -> NoReturn:
        """
        Places decorative roof corners.
        Args:
            deviation (Vec3): Allows adjustment from standard positioning.
        """


class DefaultRoof:
    def __init__(
            self,
            cell_center: Vec3,
            /,
            materials: MaterialPack,
            *,
            cell_dim: Vec3
    ) -> NoReturn:
        self._materials: Final = materials
        self._cell_dim: Final = cell_dim
        self._cell_center: Final = cell_center

    def place_base(self) -> NoReturn:
        cell_center: Vec3 = self._cell_center
        offset: Vec3 = self._cell_dim

        # Outer ring.
        server_conn.setBlocks(
            cell_center + Vec3(0, offset.y, 0),
            cell_center + offset,
            self._materials['roof_outer']
        )

        # Middle sunroof.
        x_middle = offset.x // 2
        z_middle = offset.z // 2
        server_conn.setBlock(
            cell_center + Vec3(x_middle, offset.y, z_middle),
            self._materials['sunroof'],
        )

    def place_corners(self, *, deviation: Vec3 = Vec3(0, 0, 0)) -> NoReturn:
        pass


class FlatRoof(DefaultRoof):
    def place_base(self) -> NoReturn:
        super(FlatRoof, self).place_base()

    def place_corners(self, *, deviation: Vec3 = Vec3(0, 0, 0)) -> NoReturn:
        super(FlatRoof, self).place_corners()

        offset: Vec3 = self._cell_dim
        cell_center: Vec3 = self._cell_center
        rotating_vec: Vec3 = self._cell_center + Vec3(deviation.x, deviation.y, -deviation.z)
        # Iterate from the front-left corner.
        for index in range(5):
            server_conn.setBlock(
                rotating_vec + Vec3(0, offset.y, 0),
                self._materials['roof_corner'],
            )

            # Move z to the right else left.
            rotating_vec.z = cell_center.z + deviation.z + cell_center.z \
                if index % 2 else cell_center.z - deviation.z

            # Move x to the back after the two front corners.
            if index > 1:
                rotating_vec.x = cell_center.x - deviation.x + offset.x


class AngledFlatRoof(FlatRoof):
    def place_base(self):
        super(AngledFlatRoof, self).place_base()

        cell_center = self._cell_center
        offset = self._cell_dim
        # North.
        server_conn.setBlocks(
            cell_center + Vec3(0, offset.y, 0),
            cell_center + Vec3(0, offset.y, offset.z),
            self._materials['slab'],
        )
        # East.
        server_conn.setBlocks(
            cell_center + Vec3(0, offset.y, offset.z),
            cell_center + offset,
            self._materials['slab'],
        )
        # West.
        server_conn.setBlocks(
            cell_center + Vec3(0, offset.y, 0),
            cell_center + Vec3(offset.x, offset.y, 0),
            self._materials['slab'],
        )
        # South.
        server_conn.setBlocks(
            cell_center + Vec3(offset.x, offset.y, 0),
            cell_center + offset,
            self._materials['slab'],
        )
        
    def place_corners(self, *, deviation: Vec3 = Vec3(0, 0, 0)) -> NoReturn:
        super(AngledFlatRoof, self).place_corners()
    
    
class StairFlatRoof(FlatRoof):
    def place_base(self) -> NoReturn:
        super(StairFlatRoof, self).place_base()

        offset = self._cell_dim
        cell_center = self._cell_center
        _north, _south, _west, _east = range(4)  # Secondary stair codes.
        server_conn.setBlocks(
            cell_center + Vec3(0, offset.y, 0),
            cell_center + Vec3(0, offset.y, offset.z),
            self._materials['stairs'],
            _north,
        )
        server_conn.setBlocks(
            cell_center + Vec3(0, offset.y, offset.z),
            cell_center + offset,
            self._materials['stairs'],
            _east,
        )
        server_conn.setBlocks(
            cell_center + Vec3(0, offset.y, 0),
            cell_center + Vec3(offset.x, offset.y, 0),
            self._materials['stairs'],
            _west,
        )
        server_conn.setBlocks(
            cell_center + Vec3(offset.x, offset.y, 0),
            cell_center + offset,
            self._materials['stairs'],
            _south,
        )
        
    def place_corners(self, *, deviation: Vec3 = Vec3(0, 0, 0)) -> NoReturn:
        super(StairFlatRoof, self).place_corners()


class StairMedRoof(StairFlatRoof):
    def place_base(self) -> NoReturn:
        super(StairMedRoof, self).place_base()

        cell_center = self._cell_center
        offset = self._cell_dim
        _north, _south, _west, _east = range(4)  # Secondary stair codes.
        x_deviation, y_deviation, z_deviation = Vec3(1, 1, -1)
        # Second level of stairs.
        server_conn.setBlocks(
            cell_center + Vec3(
                x_deviation,
                y_deviation + offset.y,
                -z_deviation
            ),
            cell_center + Vec3(
                x_deviation,
                y_deviation + offset.y,
                z_deviation + offset.z
            ),
            self._materials['stairs'],
            _north,
        )
        server_conn.setBlocks(
            cell_center + Vec3(
                x_deviation,
                y_deviation + offset.y,
                z_deviation + offset.z
            ),
            cell_center + Vec3(
                -x_deviation + offset.x,
                y_deviation + offset.y,
                z_deviation + offset.z
            ),
            self._materials['stairs'],
            _east,
        )
        server_conn.setBlocks(
            cell_center + Vec3(
                x_deviation,
                y_deviation + offset.y,
                -z_deviation
            ),
            cell_center + Vec3(
                -x_deviation + offset.x,
                y_deviation + offset.y,
                -z_deviation
            ),
            self._materials['stairs'],
            _west,
        )
        server_conn.setBlocks(
            cell_center + Vec3(
                -x_deviation + offset.x,
                y_deviation + offset.y,
                -z_deviation
            ),
            cell_center + Vec3(
                -x_deviation + offset.x,
                y_deviation + offset.y,
                z_deviation + offset.z
            ),
            self._materials['stairs'],
            _south,
        )

    def place_corners(self, *, deviation: Vec3 = Vec3(0, 0, 0)) -> NoReturn:
        super(StairMedRoof, self).place_corners(deviation=Vec3(1, 1, -1))


@final
class RoofFactory:
    """Roof Factory. Does not retain ownership over produced instances."""
    __roof_types = {
        RoofType.DEFAULT: DefaultRoof,
        RoofType.FLAT: FlatRoof,
        RoofType.ANGLED_FLAT: AngledFlatRoof,
        RoofType.STAIR_FLAT: StairFlatRoof,
        RoofType.STAIR_MEDIUM: StairMedRoof
    }

    @classmethod
    def create(
            cls,
            cell_center: Vec3,
            /,
            materials: MaterialPack,
            roof_type: RoofType,
            *,
            cell_dim: Vec3 = Vec3(4, 4, 4)
    ) -> Roof:
        return cls.__roof_types[roof_type](
            cell_center,
            materials,
            cell_dim=cell_dim
        )
