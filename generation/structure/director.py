from errors.structure import DirectorDoesNotExist
from utils.temp import Vec3
from builder import *
from typing import *
from abc import *


class Director(metaclass=ABCMeta):
    """Interface"""
    # TODO ~ Add Documentation.

    @abstractmethod
    def build(self) -> NoReturn: ...


@final
class ResidentialDirector(Director):
    def __init__(
            self,
            builder: Type[ResidentialBuilder],
            biome: Biome,
            /, *,
            center: Vec3,
            door: Vec3,
    ) -> NoReturn:
        self.__builder: Final[
            Type[ResidentialBuilder]
        ] = builder
        self.__biome:   Final[Biome] = biome
        self.__center:  Final[Vec3] = center
        self.__door:    Final[Vec3] = door

    def build(self) -> NoReturn:
        with self.__builder(Biome()) as builder:
            builder.create_structure()
            builder.create_stairs()
            builder.create_doors()
            builder.create_roof()
            builder.create_pool()
            builder.create_windows()


@final
class DirectorFactory:
    """Director factory that determines an appropriate director at runtime."""
    # TODO ~ Add Documentation.
    D = TypeVar('Director', bound=Director)

    @staticmethod
    def register(
            builder: Type[Builder],
            center: Vec3,
            door: Vec3,
            biome: Biome
    ) -> Type[D]:
        """
        Factory control switch. Registers a compatible director for a given builder.
        :return: An instantiated concrete director class.
        """
        # Grab inheritance tree.
        parent_tree = [cls.__name__ for cls in builder.__mro__]
        if "ResidentialBuilder" in parent_tree:
            return ResidentialDirector(builder, center, door, biome)
        elif "CommercialBuilder" in parent_tree:
            raise NotImplementedError
        elif "ParkBuilder" in parent_tree:
            raise NotImplementedError
        else:
            raise DirectorDoesNotExist(builder)


def debug() -> NoReturn:
    house = DirectorFactory.register(HouseBuilder, Vec3(), Vec3(), Biome())
    house.build()


if __name__ == '__main__':
    debug()
