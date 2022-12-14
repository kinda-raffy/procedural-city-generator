from generation.structure.cell import Cell
from abc import ABCMeta, abstractmethod
from generation.biome import Biome
from typing import *


Blueprint = Dict[int, Cell]


class Builder(metaclass=ABCMeta):
    # TODO ~ Add Documentation.
    def __init__(self, biome: Biome):
        self.__biome: Final[Biome] = biome
        self.__blueprint: Blueprint = self._generate_blueprint()

    def __enter__(self):
        """Initialises environment and perform sanity checks"""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Perform clean up and logging"""
        ...

    @final
    def __iter__(self):
        for cell in self.__blueprint:
            yield cell

    @final
    def __len__(self):
        return len([cell for cell in self.__blueprint.values() if isinstance(cell, Cell)])

    @property
    def get_biome(self) -> Biome:
        return self.__biome

    @property
    def get_blueprint(self) -> Blueprint:
        return self.__blueprint

    @abstractmethod
    def _generate_blueprint(self) -> Blueprint: ...


class ResidentialBuilder(Builder, metaclass=ABCMeta):
    def _generate_blueprint(self) -> Blueprint: ...

    @abstractmethod
    def create_structure(self) -> NoReturn: ...

    @abstractmethod
    def create_stairs(self) -> NoReturn: ...

    @abstractmethod
    def create_doors(self) -> NoReturn: ...

    @abstractmethod
    def create_roof(self) -> NoReturn: ...

    @abstractmethod
    def create_pool(self) -> NoReturn: ...

    @abstractmethod
    def create_windows(self) -> NoReturn: ...


@final
class HouseBuilder(ResidentialBuilder):
    def _generate_blueprint(self) -> Blueprint:
        return super()._generate_blueprint()

    def create_structure(self) -> NoReturn: ...

    def create_stairs(self) -> NoReturn: ...

    def create_doors(self) -> NoReturn: ...

    def create_roof(self) -> NoReturn: ...

    def create_pool(self) -> NoReturn: ...

    def create_windows(self) -> NoReturn: ...


@final
class ApartmentBuilder(ResidentialBuilder):
    def _generate_blueprint(self) -> Blueprint: ...

    def create_structure(self) -> NoReturn: ...

    def create_stairs(self) -> NoReturn: ...

    def create_doors(self) -> NoReturn: ...

    def create_roof(self) -> NoReturn: ...

    def create_pool(self) -> NoReturn: ...

    def create_windows(self) -> NoReturn: ...


@final
class SkyscraperBuilder(ResidentialBuilder):
    def _generate_blueprint(self) -> Dict[int, Cell]:
        ...

    def create_structure(self) -> NoReturn:
        ...

    def create_stairs(self) -> NoReturn:
        ...

    def create_doors(self) -> NoReturn:
        ...

    def create_roof(self) -> NoReturn:
        ...

    def create_pool(self) -> NoReturn:
        ...

    def create_windows(self) -> NoReturn:
        ...
