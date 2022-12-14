from dataclasses import dataclass, field
from enum import IntEnum, auto


class Biome(IntEnum):
    GRASSY = auto()
    DESERT = auto()
    WATER = auto()
    LAVA = auto()
    JUNGLE = auto()


@dataclass()
class Vec3:
    x: int = 0
    y: int = 0
    z: int = 0
