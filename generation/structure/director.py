from errors.structure import DirectorDoesNotExist
from utils.temp import Vec3
from builder import *
from typing import *
from typing_extensions import Self
from abc import *


class IDirector(metaclass=ABCMeta):
    """Director Interface"""
    # Bruh idk i was told this was a good idea.

    def build(self) -> None: ...


class ResidentialDirector(IDirector):
    def __init__(
            self,
            builder: Type[IResidentialBuilder],
            center: Vec3,
            door: Vec3,
            biome: Biome
    ) -> None:
        self.__builder = builder
        self.__center = center
        self.__door = door
        self.__biome = biome

    def build(self) -> None:
        with self.__builder(Biome()) as builder:
            builder.create_structure()
            builder.create_stairs()
            builder.create_doors()
            builder.create_roof()
            builder.create_pool()
            builder.create_windows()


class DirectorFactory:
    """
    Director factory that determines an appropriate director at runtime.
    """
    @staticmethod
    def register(
            builder: Type[IBuilder],
            center: Vec3,
            door: Vec3,
            biome: Biome
    ) -> Type[IDirector]:
        """
        Factory control switch. Registers a compatible director for a given builder.
        :return: An instantiated concrete director class.
        """
        # Grab inheritance tree.
        parent_tree = [cls.__name__ for cls in builder.__mro__]
        if "IResidentialBuilder" in parent_tree:
            return ResidentialDirector(builder, center, door, biome)
        elif "ICommercialBuilder" in parent_tree:
            raise NotImplementedError
        elif "IParkBuilder" in parent_tree:
            raise NotImplementedError
        else:
            raise DirectorDoesNotExist(builder)


def debug() -> None:
    house = DirectorFactory.register(HouseBuilder, Vec3(), Vec3(), Biome())
    house.build()


if __name__ == '__main__':
    debug()
