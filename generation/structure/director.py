# FIXME ~ Narrow
from errors.structure import DirectorDoesNotExist
from generation.biome import Biome
from mcpi.vec3 import Vec3
from builder import *
from typing import *
from abc import *
from enum import *


class Director(Protocol):
    """Director Interface."""
    # TODO ~ Add Documentation.

    def build(self) -> NoReturn:
        """Builds the structure through a given builder."""


@final
class ResidentialDirector:
    def __init__(
            self,
            builder: Type[ResidentialBuilder],
            biome: Biome,
            /, *,
            dimensions: Vec3,
            entry: Vec3,
    ) -> NoReturn:
        self._builder: Final = builder
        self._biome: Final = biome
        self._size: Final = dimensions
        self._door: Final = entry

    def build(self) -> NoReturn:
        with self._builder(self._biome) as builder:
            builder.create_structure()
            builder.create_stairs()
            builder.create_doors()
            builder.create_roof()
            builder.create_pool()
            builder.create_windows()


@final
class DirectorFactory:
    """Determines an appropriate director at runtime."""
    # TODO ~ Add Documentation.

    __builder_to_director_map: Final = {
        'ResidentialBuilder': ResidentialDirector
    }

    @classmethod
    def register(
            cls,
            builder: Type[Builder],
            /,
            biome: Biome,
            *,
            structure_center: Vec3,
            entry: Vec3,
    ) -> Director:
        """
        Registers a house request with an appropriate director.
        :return: An instantiated concrete director class.
        """
        # Compatible builder will be the first encountered
        # under C3 linearization.
        for builder_ in [cls_.__name__ for cls_ in builder.__mro__]:
            if builder_ in cls.__builder_to_director_map:
                return cls.__builder_to_director_map[builder_](
                    builder,
                    biome,
                    structure_center=structure_center,
                    entry=entry
                )


def debug() -> NoReturn:
    house: Director = DirectorFactory.register(
        HouseBuilder,
        Biome.GRASSY,
        structure_center=Vec3(1, 1, 1),
        entry=Vec3(2, 1, 1),
    )
    house.build()


if __name__ == '__main__':
    debug()
