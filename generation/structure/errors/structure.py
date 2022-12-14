from typing import Type, NoReturn
from generation.biome import Biome
from generation.structure.builder import Builder


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
