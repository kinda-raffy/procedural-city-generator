from enum import (
    Enum,
    verify,
    global_enum,
    CONTINUOUS,
    unique,
)

__all__ = ["Biome"]


@unique
@global_enum
@verify(CONTINUOUS)
class Biome(Enum):
    GRASSY = 1
    DESSERT = 2
    WATER = 3
    LAVA = 4
    JUNGLE = 5
