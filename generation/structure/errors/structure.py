from __future__ import annotations
from typing import (
    Type,
    NoReturn,
    TYPE_CHECKING,
)

if TYPE_CHECKING:
    from mcpi.vec3 import Vec3
    from generation.biome import Biome
    from generation.structure.builder import Builder


__all__ = [
    "DirectorDoesNotExist",
    "BiomeNotImplemented",
    "BiomeDoesNotExist",
    "BuilderNotImplemented",
    "CellDoesNotExist",
]


class DirectorDoesNotExist(NotImplementedError):
    def __init__(self, builder: Type[Builder]) -> NoReturn:
        self.builder = builder
        super().__init__(f"Director for {self.builder} does not exist.")


class BiomeNotImplemented(NotImplementedError):
    def __init__(self, biome: Biome) -> NoReturn:
        self.biome = biome
        super().__init__(f"Biome {self.biome} is not implemented.")


class BiomeDoesNotExist(NotImplementedError):
    def __init__(self) -> NoReturn:
        super().__init__(f"Given biome does not exist.")


class BuilderNotImplemented(NotImplementedError):
    def __init__(self, builder: Type[Builder]) -> NoReturn:
        super().__init__(f"Builder {builder} is not implemented.")


class CellDoesNotExist(ValueError):
    def __init__(self, pos: Vec3) -> NoReturn:
        super().__init__(f"Cell at ({pos=}) does not exist.")
