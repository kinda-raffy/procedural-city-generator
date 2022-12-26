from __future__ import annotations
from typing import (
    Dict,
    Any,
    Final,
    NotRequired,
    TypedDict,
    Type,
    TYPE_CHECKING,
)
from dataclasses import dataclass
import random
import tomllib

from mcpi.vec3 import Vec3
from generation import connection as server_conn
from generation.structure.errors.structure \
    import BiomeNotImplemented
from generation.structure.utils.block_extension \
    import BlockExt as BlocEx
from generation.biome import Biome

if TYPE_CHECKING:
    from builder import Builder


__all__ = [
    "MaterialPack",
    "Environment",
]


class MaterialPack(TypedDict):
    """Global material pack for structural generation."""
    # Sunder identifiers. Used only for logging.
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


@dataclass(frozen=True, kw_only=True)
class Environment:
    """
    Collection of environment related functions.
    """
    biome: Biome
    builder: Type[Builder]

    def __new__(cls, biome, builder):
        if biome in (Biome.LAVA, Biome.JUNGLE):
            # TODO: Implement biomes.
            raise BiomeNotImplemented(biome)
        return super().__new__(cls)

    def get_material_pack(self) -> MaterialPack:
        """Load materials from TOML file."""
        biome: Final[str] = self.biome[0].name.lower()
        structure_type: Final[str] = \
            self.builder.__name__.removesuffix('Builder').lower()

        with open(f'config/material_packs/{biome}.toml', 'rb') as file:
            config: Dict[str, Any] = tomllib.load(file)
        assert structure_type in config['meta']['supported_structures'], \
            f'{biome} does not support {structure_type}.'

        pack: Dict[str, Any] = random.choice(config[biome][structure_type])
        # Transform materials into BlockExt objects.
        loaded_pack = {
            k: BlocEx[v.upper()]
            if isinstance(v, str) else v
            for k, v in pack.items()
        }
        # Add optional metadata for logging.
        for k, v in loaded_pack.pop('_info').items():
            loaded_pack[f'_{k}_'] = v
        return loaded_pack

    @staticmethod
    def clear_block(
            block_dimensions: Vec3,
            /, *,
            ground: int,
            cell_floor: int = 2
    ) -> None:
        block_dimensions.y += cell_floor
        server_conn.setBlocks(
            block_dimensions + Vec3(0, ground, 0),
            block_dimensions,
            BlocEx['AIR'],
            )
