from dataclasses import dataclass
from enum import IntEnum, auto


class Biome(IntEnum):
    GRASSY = auto()
    DESERT = auto()
    WATER = auto()
    LAVA = auto()
    JUNGLE = auto()


@dataclass()
class Vec3:
    x: int
    y: int
    z: int
