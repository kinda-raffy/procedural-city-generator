from __future__ import annotations
from builder import (
    Builder,
    ResidentialBuilder,
    HouseBuilder
)
from generation.biome import Biome
from mcpi.vec3 import Vec3

from typing import (
    Protocol,
    NoReturn,
    Type,
    Final,
    final
)

__all__ = [
    'Director',
    'DirectorFactory',
]

from generation.structure.errors.structure import DirectorDoesNotExist


class Director(Protocol):
    """Director Interface."""
    # TODO ~ Add Documentation.

    def build(self) -> NoReturn:
        """Builds the structure through a given builder."""


@final
class ResidentialDirector:
    def __init__(  # type: ignore
            self,
            builder: Type[ResidentialBuilder],
            biome: Biome,
            /, *,
            dimensions: Vec3,
            entry: Vec3,
            center: Vec3
    ) -> NoReturn:
        self._builder: Final = builder
        self._biome: Final = biome
        self._size: Final = dimensions
        self._entrance: Final = entry
        self._center: Final = center

    def build(self) -> NoReturn:
        with self._builder(
            self._biome,
            build_dimensions=self._size,
            entry=self._entrance,
            center=self._center
        ) as builder:
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
            size: Vec3,
            *,
            entry: Vec3,
            center: Vec3,
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
                    dimensions=size,
                    entry=entry,
                    center=center
                )
        raise DirectorDoesNotExist(builder)


def debug() -> NoReturn:
    house: Director = DirectorFactory.register(
        HouseBuilder,
        Biome.GRASSY,
        size=Vec3(10, 10, 10),
        entry=Vec3(0, 0, 5),
        center=Vec3(5, 5, 5)
    )
    house.build()


if __name__ == '__main__':
    debug()
