from village_grid_unit import VillageGridUnit
from village_grid_foundation import VillageGridFoundation
import typing


class VillageEntity:

    def __init__(
        self, *, 
        grid_foundation: VillageGridFoundation = None,
        house_upper_bound: int = 200
    ) -> None:
        # Create grid with default values if no object provided.
        self.__grid_foundation: VillageGridFoundation = grid_foundation if \
            grid_foundation is not None else VillageGridFoundation()
        self.__curr_house_units: list[VillageGridUnit] = list()
        self.house_upper_bound: int = abs(house_upper_bound)

    def __iter__(self) -> typing.Iterable[VillageGridUnit]:
        for curr_house_unit in self.__curr_house_units:
            yield curr_house_unit

    def allocate_house_blocks(self) -> None:
        raise NotImplementedError()

    def __create_paths_dijkstra(self) -> None:
        raise NotImplementedError

    def __create_paths_a_star(self) -> None:
        raise NotImplementedError()


def _village_entity_test() -> None:
    raise NotImplementedError()


if __name__ == '__main__':
    _village_entity_test()
