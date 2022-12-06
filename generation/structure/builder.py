from abc import ABCMeta, abstractmethod
from utils.temp import Biome
from cell import Cell
from typing import *


class IBuilder(metaclass=ABCMeta):
    def __init__(self, biome: Biome):
        self.__biome: Biome = biome
        self.__blueprint: Dict[int, Cell] = self._generate_blueprint()

    def __enter__(self):
        """Initialises environment and perform sanity checks"""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Logs errors and cleans up"""
        ...

    def __iter__(self):
        for cell in self.__blueprint:
            yield cell

    def __len__(self):
        return len([cell for cell in self.__blueprint.values() if isinstance(cell, Cell)])

    @abstractmethod
    def _generate_blueprint(self) -> Dict[int, Cell]:
        """Generates a blueprint for the building"""
        ...

    @property
    def get_biome(self) -> Biome:
        return self.__biome

    @property
    def get_blueprint(self) -> Dict[int, Cell]:
        return self.__blueprint


class IResidentialBuilder(IBuilder, metaclass=ABCMeta):
    @abstractmethod
    def create_structure(self) -> None: ...

    @abstractmethod
    def create_stairs(self) -> None: ...

    @abstractmethod
    def create_doors(self) -> None: ...

    @abstractmethod
    def create_roof(self) -> None: ...

    @abstractmethod
    def create_pool(self) -> None: ...

    @abstractmethod
    def create_windows(self) -> None: ...


class HouseBuilder(IResidentialBuilder):
    def __init__(self, biome: Biome):
        super().__init__(biome)

    def _generate_blueprint(self) -> Dict[int, Cell]:
        """Generates a blueprint for the building"""
        ...

    def create_structure(self) -> None:
        ...

    def create_stairs(self) -> None:
        ...

    def create_doors(self) -> None:
        ...

    def create_roof(self) -> None:
        ...

    def create_pool(self) -> None:
        ...

    def create_windows(self) -> None:
        ...


class ApartmentBuilder(IResidentialBuilder):
    def __init__(self, biome: Biome):
        super().__init__(biome)

    def _generate_blueprint(self) -> Dict[int, Cell]:
        """Generates a blueprint for the building"""
        ...

    def create_structure(self) -> None:
        ...

    def create_stairs(self) -> None:
        ...

    def create_doors(self) -> None:
        ...

    def create_roof(self) -> None:
        ...

    def create_pool(self) -> None:
        ...

    def create_windows(self) -> None:
        ...


class SkyscraperBuilder(IResidentialBuilder):
    def __init__(self, biome: Biome):
        super().__init__(biome)

    def _generate_blueprint(self) -> Dict[int, Cell]:
        """Generates a blueprint for the building"""
        ...

    def create_structure(self) -> None:
        ...

    def create_stairs(self) -> None:
        ...

    def create_doors(self) -> None:
        ...

    def create_roof(self) -> None:
        ...

    def create_pool(self) -> None:
        ...

    def create_windows(self) -> None:
        ...