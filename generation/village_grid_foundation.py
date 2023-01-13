from generation import connection as server_connection
from collections import deque
from village_grid_unit import VillageGridUnit, TerrainType
from mcpi.vec3 import Vec3
import typing

# TODO: Figure out if caching aids performance.
# import functools


class VillageGridFoundation:  # TODO: Test function to display edges between connected units?
    def __init__(
        self,
        *,
        unit_upper_bound: int = 2000,
        unit_side_length: int = 3,
        height_variance_tolerance: int = 2,
        prohibited_terrain: set[TerrainType] = None,
        water_road_penalty: int = 7,
    ) -> None:
        self.starting_position: Vec3 = (
            server_connection.player.getTilePos()
        )  # Use current player position as the central grid unit.
        self.unit_upper_bound: int = unit_upper_bound
        self.unit_side_length: int = unit_side_length
        self.height_variance_tolerance: int = abs(height_variance_tolerance)
        # Maps reflecting an undirected graph structure that underpins the village layout.
        self._adjacency_list: dict[VillageGridUnit, list[VillageGridUnit]] = dict()
        self._edge_weights: dict[tuple[VillageGridUnit, VillageGridUnit], int] = dict()
        self.__water_road_penalty = water_road_penalty
        self.__prohibited_terrain = (
            prohibited_terrain
            if prohibited_terrain is not None
            else {TerrainType.LAVA, TerrainType.TREE}
        )
        # Functions used repeatedly to create adjacent units.
        self.__adjacent_unit_functions: list[typing.Callable] = [
            VillageGridUnit.create_unit_north,
            VillageGridUnit.create_unit_east,
            VillageGridUnit.create_unit_south,
            VillageGridUnit.create_unit_west,
        ]

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
        # Total blocks traversed when travelling between centres of adjacent units.
        return self.unit_side_length + 1

    @unit_upper_bound.setter
    def unit_upper_bound(self, unit_upper_bound: int) -> None:
        if unit_upper_bound <= 0:
            raise ValueError("The unit upper bound needs to be positive.")
        self.__unit_upper_bound = unit_upper_bound

    @unit_side_length.setter
    def unit_side_length(self, unit_side_length: int) -> None:
        # Ensure side length and separation are not altered after grid is generated.
        if (
            self.adjacency_list
            or self._edge_weights
            or unit_side_length % 2 == 0
            or unit_side_length <= 0
        ):
            raise ValueError(
                "Side length is positive, odd and set before grid is generated."
            )
        self.__unit_side_length = unit_side_length

    def add_grid_unit(self, new_grid_unit: VillageGridUnit) -> None:
        if (
            isinstance(new_grid_unit, VillageGridUnit)
            and new_grid_unit not in self._adjacency_list
        ):
            # Add the new tile with an empty adjacency list.
            self._adjacency_list[new_grid_unit] = list()

    def find_grid_unit(
        self, *, coordinate_label: tuple[int, int] = None, vector_position: Vec3 = None
    ) -> typing.Optional[VillageGridUnit]:
        if coordinate_label is None and vector_position is None:
            return None
        checking_coord_label: bool = coordinate_label is not None
        # Return the grid unit object that corresponds with the search arg; label used by default.
        search_value = coordinate_label if checking_coord_label else vector_position
        for grid_unit in self:
            if search_value == (
                grid_unit.coordinate_label
                if checking_coord_label
                else grid_unit.vector_position
            ):
                return grid_unit

    def add_grid_edge(
        self, unit_one: VillageGridUnit, unit_two: VillageGridUnit
    ) -> bool:
        unit_pair_one: tuple[VillageGridUnit] = (
            unit_one,
            unit_two,
        )  # Use both pairs for an undirected edge.
        unit_pair_two: tuple[VillageGridUnit] = reversed(unit_pair_one)
        # Return and don't create the edge if it's pre-existing or invalid.
        if unit_pair_one in self._edge_weights or unit_pair_two in self._edge_weights:
            return False
        edge_weight = self.__derive_edge_weight(unit_one, unit_two)
        if edge_weight is None:
            return False
        # Add edges in both directions including weight
        for (unit_x, unit_y) in [unit_pair_one, unit_pair_two]:
            self._adjacency_list[unit_x].append(unit_y)
            self._edge_weights[(unit_x, unit_y)] = edge_weight
        return True

    def __derive_edge_weight(
        self,
        unit_one: VillageGridUnit,
        unit_two: VillageGridUnit,
    ) -> typing.Optional[int]:
        # Return null if the edge is not allowed due to terrain or height variation.
        terrain_one: TerrainType = unit_one._terrain_type
        terrain_two: TerrainType = unit_two._terrain_type
        if (
            terrain_one in self.__prohibited_terrain
            or terrain_two in self.__prohibited_terrain
        ):
            return None
        elevation_difference: int = abs(
            unit_one.vector_position.y - unit_two.vector_position.y
        )
        if elevation_difference > self.height_variance_tolerance:
            return None
        # Add one to the difference so edge weights are always positive.
        edge_weight: int = elevation_difference + 1
        return (
            edge_weight + self.__water_road_penalty
            if (terrain_one == TerrainType.WATER or terrain_two == TerrainType.WATER)
            else edge_weight
        )

    def build_village_grid(self, *, auto_connect: bool = True) -> set[VillageGridUnit]:
        visited_units: set[VillageGridUnit] = set()
        include_units: set[VillageGridUnit] = set()
        # The frontier tracks all units to be visited from starting position.
        frontier: deque[VillageGridUnit] = deque()
        frontier.append(VillageGridUnit(self.starting_position, (0, 0)))
        # Visit each unit using breadth-first search.
        # Connect adjacent units if they exist and create new units where they don't.
        while frontier and len(include_units) < self.unit_upper_bound:
            current_unit: VillageGridUnit = frontier.popleft()
            if current_unit not in visited_units:
                visited_units.add(current_unit)
                include_units.add(current_unit)
                label_x, label_y = current_unit.coordinate_label
                adjacent_exists: list[bool] = self.__connect_existing_grid_units(
                    current_unit, label_x, label_y
                )
                for unit_already_exists, unit_creation_function in zip(
                    adjacent_exists, self.__adjacent_unit_functions
                ):
                    # If no unit exists yet, create one and connect it to the grid.
                    if not unit_already_exists:
                        adjacent_unit = unit_creation_function(
                            current_unit, vector_offset=self.unit_separation
                        )
                        self.__handle_created_grid_unit(
                            current_unit, adjacent_unit, frontier
                        )
        # Ensure all units in the grid are connected where possible.
        if auto_connect:
            for added_unit in self:
                label_x, label_y = added_unit.coordinate_label
                self.__connect_existing_grid_units()
        return include_units

    def __connect_existing_grid_units(
        self,
        current_unit: VillageGridUnit,
        label_x: int,
        label_y: int,
    ) -> list[bool]:
        adjacent_unit_exists: list[bool] = [False] * 4  # Four cardinal directions.
        label_direction_offsets: list[tuple[int]] = [(-1, 0), (0, 1), (1, 0), (0, -1)]
        # Check each direction for existing unit and connect if found.
        for index, (x_offset, y_offset) in enumerate(label_direction_offsets):
            new_x, new_y = label_x + x_offset, label_y + y_offset
            if (
                found_unit := self.find_grid_unit(coordinate_label=(new_x, new_y))
                is not None
            ):
                self.add_grid_edge(current_unit, found_unit)
                adjacent_unit_exists[index] = True
        return adjacent_unit_exists  # Return indication of where units exist.

    def __handle_created_grid_unit(
        self,
        current_unit: VillageGridUnit,
        created_unit: VillageGridUnit,
        frontier: deque[VillageGridUnit],
    ) -> None:
        self.add_grid_unit(created_unit)
        if self.add_grid_edge(current_unit, created_unit):
            frontier.append(created_unit)

    def connect_village_grid(self) -> None:
        # TODO: Figure out if this function is required.
        raise NotImplementedError()


def _village_grid_foundation_test() -> None:
    default_test_grid = VillageGridFoundation()  # Use all default values.
    default_test_grid.build_village_grid()
    for grid_unit in default_test_grid:
        grid_unit._set_test_block()


if __name__ == "__main__":
    _village_grid_foundation_test()
