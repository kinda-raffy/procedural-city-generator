from errors.structure import (
    BiomeDoesNotExist,
    BiomeNotImplemented
)
from typing import (
    ClassVar,
    NotRequired,
    TypedDict,
    Type
)
from utils.block_extension import BlockExt as BlocEx
from generation import connection as conn
from builder import IBuilder
from generation.biome import Biome
from dataclasses import dataclass
from utils.temp import Vec3
import random
import tomllib


class MaterialPack(TypedDict):
    """Global material pack for structural generation."""
    # Sunder identifiers.
    _name_: NotRequired[str]
    _description_: NotRequired[str]

    # Horizontal surfaces.
    foundation: BlocEx
    stone: BlocEx
    upstairs_floor: BlocEx

    # Vertical surfaces.
    walls: BlocEx
    pillars: BlocEx
    slab: BlocEx

    # Structural elements.
    stairs: BlocEx
    windows: BlocEx
    door: BlocEx

    # Decorative elements.
    fence: BlocEx
    fence_gate: BlocEx

    # Pool materials.
    pool_wall: BlocEx
    pool_container: BlocEx
    pool_liquid: BlocEx

    # Roof materials.
    sunroof: BlocEx
    roof_outer: BlocEx
    roof_corner: BlocEx


class FurniturePack(TypedDict):
    """
    Global furniture pack for structural generation.
    Scales with the size of a given cell.
    Divided into 3 categories:
        - `true`: The true 3-Dimensional center of a cell.
        - `side-center`: The center of a cell's 2-Dimensional side.
        - `corner`: The corner of a cell's 2-Dimensional side.
    """
    # Sunder identifiers.
    _name_: NotRequired[str]
    _variation_: NotRequired[int]
    _description_: NotRequired[str]

    # True cell center.
    true_center_floor: BlocEx
    true_center: BlocEx
    true_center_ceil: BlocEx

    # Relative center of a given cell's ceil-side.
    center_ceil_front: BlocEx
    center_ceil_back: BlocEx
    center_ceil_right: BlocEx
    center_ceil_left: BlocEx

    # Relative center of a given cell's floor-side.
    center_floor_front: BlocEx
    center_floor_back: BlocEx
    center_floor_right: BlocEx
    center_floor_left: BlocEx

    # Ceiling corners: Front.
    corner_ceil_front_right: BlocEx
    corner_ceil_front_left: BlocEx

    # Ceiling corners: Back.
    corner_ceil_back_right: BlocEx
    corner_ceil_back_left: BlocEx

    # Floor corners: Front.
    corner_floor_front_right: BlocEx
    corner_floor_front_left: BlocEx

    # Floor corners: Back.
    corner_floor_back_right: BlocEx
    corner_floor_back_left: BlocEx


@dataclass(frozen=True, kw_only=True)
class Environment:
    biome: Biome
    builder: Type[IBuilder]
    material_pack: ClassVar[MaterialPack]

    def __new__(cls, biome: Biome, builder: Type[IBuilder]):
        if biome not in Biome:
            raise BiomeDoesNotExist(biome)
        return super().__new__(cls)

    @classmethod
    def _load_material_pack(cls) -> MaterialPack:
        """Load materials from TOML file."""
        pass

    def material_selector(self) -> MaterialPack:
        match biome := self.biome:
            case Biome.GRASSY:
                return random.choice(grass_biome)
            case Biome.DESERT:
                return random.choice(sand_biome)
            case Biome.WATER:
                return random.choice(water_biome)
            case Biome.LAVA:
                raise BiomeNotImplemented(biome)
            case Biome.JUNGLE:
                raise BiomeNotImplemented(biome)
            case _:
                raise BiomeDoesNotExist()

    @staticmethod
    def clear_block(
            center: Vec3,
            *,
            radius: int = 7,
            floor: int = 2
    ) -> None:
        # Vec3 should be center of the building.
        center.y += floor
        conn.setBlocks(
            center.x - radius, center.y, center.z - radius,     # Start coordinates.
            center + radius,                                    # End coordinates.
            BlocEx.AIR
        )

