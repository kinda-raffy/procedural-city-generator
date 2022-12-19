from typing import Type, NoReturn
from generation.biome import Biome
from generation.structure.builder import Builder
from mcpi.vec3 import Vec3

__all__ = [
    'DirectorDoesNotExist',
    'BiomeNotImplemented',
    'BiomeDoesNotExist',
    'CellDoesNotExist',
    'BuilderNotImplemented'
]


class DirectorDoesNotExist(NotImplementedError):
    def __init__(self, builder: Type[Builder]) -> NoReturn:
        self.builder = builder
        super().__init__(f'Director for {self.builder} does not exist.')


class BiomeNotImplemented(NotImplementedError):
    def __init__(self, biome: Biome) -> NoReturn:
        self.biome = biome
        super().__init__(f'Biome {self.biome} is not implemented.')


class BiomeDoesNotExist(NotImplementedError):
    def __init__(self) -> NoReturn:
        super().__init__(f'Given biome does not exist.')


class BuilderNotImplemented(NotImplementedError):
    def __init__(self, builder: Type[Builder]) -> NoReturn:
        super().__init__(f'Builder {builder} is not implemented.')


class CellDoesNotExist(ValueError):
    def __init__(self, pos: Vec3) -> NoReturn:
        super().__init__(f'Cell at ({pos=}) does not exist.')
