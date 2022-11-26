from __future__ import annotations
from generation import connection as server_connection
from mcpi.vec3 import Vec3
import dataclasses
import typing
import enum
import math
import json


terrain_type_codes = json.load("config/block_terrain_types.json")


class TerrainType(enum.Enum):
    GROUND = "Ground"
    WATER = "Water"
    SAND = "Sand"
    LAVA = "Lava"
    TREE = "Tree"


@dataclasses.dataclass
class VillageGridUnit:
    vector_position: Vec3
    coordinate_label: tuple[int, int]
    _terrain_type: TerrainType = None
    _path_predecessor: VillageGridUnit = (
        None  # Predecessor and distance to centre used for pathfinding.
    )
    _distance_to_centre: float = math.inf

    def __post_init__(self) -> None:
        # Use vector field to derive terrain.
        self._terrain_type = VillageGridUnit.derive_vector_terrain(self.vector_position)

    @staticmethod
    def derive_vector_terrain(block_position: Vec3) -> TerrainType:
        block_id = server_connection.getBlock(
            block_position.x, block_position.y, block_position.z
        )
        # Match the received block id against those grouped by terrain type.
        for terrain_type, terrain_type_value in TerrainType:
            terrain_type_block_ids = terrain_type_codes.get(terrain_type_value)
            if (
                terrain_type_block_ids is not None
                and block_id in terrain_type_block_ids
            ):
                return terrain_type
        # Return ground if no matches identified for another type.
        return TerrainType.GROUND

    # TODO: Clean up these functions below using decorators? Need to consolidate shared code.

    @staticmethod
    def create_unit_north(
        curr_unit: VillageGridUnit, *, vector_offset: int
    ) -> VillageGridUnit:
        label_x, label_y = curr_unit.coordinate_label
        coord_x, coord_z = curr_unit.vector_position.x, curr_unit.vector_position.z
        north_x = coord_x - vector_offset
        north_label = (label_x - 1, label_y)
        return VillageGridUnit(
            Vec3(north_x, server_connection.getHeight(north_x, coord_z), coord_z),
            north_label,
        )

    @staticmethod
    def create_unit_south(
        curr_unit: VillageGridUnit, *, vector_offset: int
    ) -> VillageGridUnit:
        label_x, label_y = curr_unit.coordinate_label
        coord_x, coord_z = curr_unit.vector_position.x, curr_unit.vector_position.z
        south_x = coord_x + vector_offset
        south_label = (label_x + 1, label_y)
        return VillageGridUnit(
            Vec3(south_x, server_connection.getHeight(south_x, coord_z), coord_z),
            south_label,
        )

    @staticmethod
    def create_unit_east(
        curr_unit: VillageGridUnit, *, vector_offset: int
    ) -> VillageGridUnit:
        label_x, label_y = curr_unit.coordinate_label
        coord_x, coord_z = curr_unit.vector_position.x, curr_unit.vector_position.z
        east_z = coord_z + vector_offset
        east_label = (label_x, label_y + 1)
        return VillageGridUnit(
            Vec3(coord_x, server_connection.getHeight(coord_x, east_z), east_z),
            east_label,
        )

    @staticmethod
    def create_unit_west(
        curr_unit: VillageGridUnit, *, vector_offset: int
    ) -> VillageGridUnit:
        label_x, label_y = curr_unit.coordinate_label
        coord_x, coord_z = curr_unit.vector_position.x, curr_unit.vector_position.z
        west_z = coord_z - vector_offset
        west_label = (label_x, label_y - 1)
        return VillageGridUnit(
            Vec3(coord_x, server_connection.getHeight(coord_x, west_z), west_z),
            west_label,
        )


def _village_grid_unit_test() -> None:
    raise NotImplementedError()


if __name__ == "__main__":
    _village_grid_unit_test()
