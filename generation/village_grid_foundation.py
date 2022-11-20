from generation import connection
from village_grid_unit import VillageGridUnit, TerrainType
from mcpi.vec3 import Vec3
import typing
# TODO: Figure out if caching aids performance.
# import functools


class VillageGridFoundation:

    def __init__(
        self, *,
        unit_upper_bound: int = 800,
        unit_side_length: int = 3,
        height_variance_tolerance: int = 2,
        prohibited_terrain: set[TerrainType] = None,
        water_road_penalty: int = 7,
    ) -> None:
        self.starting_position: Vec3 = connection.player.getTilePos() # Use current player position as the central grid unit.
        self.unit_upper_bound: int = unit_upper_bound
        self.unit_side_length: int = unit_side_length
        self.height_variance_tolerance: int = abs(height_variance_tolerance)
        # Maps reflecting an undirected graph structure that underpins the village layout.
        self._adjacency_list: dict[VillageGridUnit, list[VillageGridUnit]] = dict()
        self._edge_weights: dict[tuple[VillageGridUnit, VillageGridUnit], int] = dict()
        self.__water_road_penalty = water_road_penalty
        self.__prohibited_terrain = prohibited_terrain if prohibited_terrain is not None \
            else {TerrainType.LAVA, TerrainType.TREE}

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

    def find_grid_unit(
        self, *,
        coordinate_label: tuple[int, int] = None,
        vector_position: Vec3 = None
    ) -> typing.Optional[VillageGridUnit]:
        if coordinate_label is None and vector_position is None:
            return None
        checking_coord_label: bool = coordinate_label is not None
        # Return the grid unit object that corresponds with the passed search value; label used by default.
        search_value = coordinate_label if checking_coord_label else vector_position
        for grid_unit in self:
            if search_value == (grid_unit.coordinate_label if checking_coord_label else grid_unit.vector_position):
                return grid_unit

    def add_grid_edge(self, unit_one: VillageGridUnit, unit_two: VillageGridUnit) -> bool:
        unit_pair_one: tuple[VillageGridUnit] = (unit_one, unit_two) # Use both pairs for an undirected edge.
        unit_pair_two: tuple[VillageGridUnit] = reversed(unit_pair_one)
        # Return and don't create the edge if it's pre-existing or invalid.
        if unit_pair_one in self._edge_weights or unit_pair_two in self._edge_weights:
            return False
        edge_weight = self.__derive_edge_weight(unit_one, unit_two)
        if edge_weight is None:
            return False
        # Add edges in both directions including weight; indexing is okay since there's always two units.
        for edge_pair in (unit_pair_one, unit_pair_two):
            self._adjacency_list[edge_pair[0]].append(edge_pair[1])
            self._edge_weights[edge_pair] = edge_weight
        return True

    def __derive_edge_weight(self, unit_one: VillageGridUnit, unit_two: VillageGridUnit) -> typing.Optional[int]:
        # Return null if the edge is not allowed due to invalid terrain or excessive height variation.
        terrain_one: TerrainType = unit_one._terrain_type
        terrain_two: TerrainType = unit_two._terrain_type
        if terrain_one in self.__prohibited_terrain or terrain_two in self.__prohibited_terrain:
            return None
        elevation_difference: int = abs(unit_one.vector_position.y - unit_two.vector_position.y)
        if elevation_difference > self.height_variance_tolerance:
            return None
        # Add one to the difference so edge weights are always positive.
        edge_weight: int = elevation_difference + 1
        return edge_weight + self.__water_road_penalty if \
            (terrain_one == TerrainType.WATER or terrain_two == TerrainType.WATER) else edge_weight

    def build_village_grid(self, auto_connect: bool = True) -> None:
        raise NotImplementedError()

    def connect_village_grid(self) -> None:
        raise NotImplementedError()


def _village_grid_foundation_test() -> None:
    raise NotImplementedError


if __name__ == '__main__':
    _village_grid_foundation_test()