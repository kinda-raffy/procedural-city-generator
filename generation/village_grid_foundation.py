from generation import connection
from village_grid_unit import VillageGridUnit
from mcpi.vec3 import Vec3
import typing
# TODO: Figure out if caching aids performance.
# import functools


class VillageGridFoundation:

    def __init__(self, unit_upper_bound: int = 300, unit_side_length: int = 3, height_variance_tolerance: int = 2) -> None:
        self.starting_position: Vec3 = connection.player.getTilePos() # Use current player position as the central grid unit.
        self.unit_upper_bound: int = unit_upper_bound
        self.unit_side_length: int = unit_side_length
        self.height_variance_tolerance: int = abs(height_variance_tolerance)
        # Maps reflecting a graph structure that underpins the village layout.
        self._adjacency_list: dict[VillageGridUnit, list[VillageGridUnit]] = dict()
        self._edge_weights: dict[tuple[VillageGridUnit, VillageGridUnit], int] = dict()

    def __iter__(self) -> typing.Iterator[VillageGridUnit]:
        for grid_unit in self._adjacency_list:
            yield grid_unit

    def __len__(self) -> int:
        return len(self._adjacency_list)

    @property
    def unit_upper_bound(self) -> int:
        return self.__unit_upper_bound

    @property
    def unit_side_length(self) -> int:
        return self.__unit_side_length

    @property
    def unit_separation(self) -> int:
        # The total blocks traversed when travelling between the centres of adjacent units.
        return self.unit_side_length + 1

    @unit_upper_bound.setter
    def unit_upper_bound(self, unit_upper_bound: int) -> None:
        if unit_upper_bound <= 0:
            raise ValueError('The unit upper bound needs to be positive.')
        self.__unit_upper_bound = unit_upper_bound

    @unit_side_length.setter
    def unit_side_length(self, unit_side_length: int) -> None:
        # Ensure side length, and thus separation, are not altered after grid is generated.
        if self.adjacency_list or self._edge_weights or unit_side_length % 2 == 0 or unit_side_length <= 0:
            raise ValueError('Side length is positive, odd and set before grid is generated.')
        self.__unit_side_length = unit_side_length

    def add_grid_unit(self, new_grid_unit: VillageGridUnit) -> None:
        if isinstance(new_grid_unit, VillageGridUnit) and new_grid_unit not in self._adjacency_list:
            # Add the new tile with an empty adjacency list.
            self._adjacency_list[new_grid_unit] = list()

    def build_village_grid(auto_connect: bool = True) -> None:
        raise NotImplementedError()

    def connect_village_grid() -> None:
        raise NotImplementedError()


def _village_grid_foundation_test() -> None:
    raise NotImplementedError


if __name__ == '__main__':
    _village_grid_foundation_test()