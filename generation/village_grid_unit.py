from __future__ import annotations
import mcpi.minecraft
import mcpi.vec3
import enum
import dataclasses
import math
import json


# TODO: A better way of handling these server connection instances across files?
minecraft_instance = mcpi.minecraft.Minecraft.create()
terrain_type_codes = json.load('block_terrain_types.json')


class TerrainType(enum.Enum):
    GROUND = 'Ground'
    WATER = 'Water'
    SAND = 'Sand'
    LAVA = 'Lava'
    TREE = 'Tree'


@dataclasses.dataclass
class VillageGridUnit:
    vector_position: mcpi.vec3.Vec3
    coordinate_label: tuple[int, int]
    _terrain_type: TerrainType = None
    _path_predecessor: VillageGridUnit = None
    _distance_to_centre: float = math.inf

    def __post_init__(self):
        # Use vector field to derive terrain.
        self._terrain_type = VillageGridUnit.derive_vector_terrain(self.vector_position)

    @staticmethod
    def derive_vector_terrain(block_position: mcpi.vec3.Vec3) -> TerrainType:
        block_id = minecraft_instance.getBlock(
            block_position.x, block_position.y, block_position.z)
        # Match the received block id against those grouped by terrain type.
        for terrain_type, terrain_type_value in TerrainType:
            terrain_type_block_ids = terrain_type_codes.get(terrain_type_value)
            if terrain_type_block_ids is not None and block_id in terrain_type_block_ids:
                return terrain_type
        # Return ground if no matches identified for another type.
        return TerrainType.GROUND


def _village_grid_unit_test() -> None:
    raise NotImplementedError()


if __name__ == '__main__':
    _village_grid_unit_test()