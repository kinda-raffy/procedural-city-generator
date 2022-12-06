from typing import Type
from generation.structure.builder import IBuilder


class DirectorDoesNotExist(NotImplementedError):
    def __init__(self, builder: Type[IBuilder]):
        self.builder = builder
        super().__init__(f'Director for {self.builder} does not exist.')


class BiomeNotImplemented(NotImplementedError):
    def __init__(self, biome: Biome):
        self.biome = biome
        super().__init__(f'Biome {self.biome} is not implemented.')


class BiomeDoesNotExist(NotImplementedError):
    def __init__(self):
        super().__init__(f'Given biome does not exist.')