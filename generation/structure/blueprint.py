from __future__ import annotations
from cell import (
    Cell,
    CellType,
    NeighbouringCells,
)
from mcpi.vec3 import Vec3

from typing import (
    Optional,
    List,
    Annotated,
    Final,
    NoReturn,
    Callable,
    Iterator,
    Set,
    Deque,
    final,
)
from collections import deque
from abc import (
    ABCMeta,
    abstractmethod,
)
from enum import (
    Enum,
    unique,
    auto,
)
import random

__all__ = [
    'CellStorage',
    'CellStorageLevel',
    'CellStorageRow',
    'Blueprint',
    'ResidentialBlueprint',
    'HouseBlueprint',
    'ApartmentBlueprint',
    'SkyscraperBlueprint',
    'BlueprintType',
    'BlueprintFactory',
]

from generation.structure.errors.structure import CellDoesNotExist

CellStorage = List[List[List[Cell]]]
CellStorageLevel = List[List[Cell]]
CellStorageRow = List[Cell]


class Blueprint(metaclass=ABCMeta):
    """
    Defines the minimum design
    requirements for a blueprint.
    """

    def __init__(
            self,
            size: Vec3,
            /,
            entrance: Vec3,
            center: Vec3,
            *,
            explore_factor: Annotated[
                float, '0 <= x <= 1'
            ] = 0.95,
            merge_factor: Annotated[
                float, '0 <= x <= 1'
            ] = 0.5,
            min_cells: Optional[
                Annotated[int, 'x > 2']
            ] = None,
    ):
        self._dimensions: Final = size
        # Ground floor determined from entrance.
        self._structure_entrance: Final = entrance
        self._structure_center: Final = center
        self._permissible_levels: Final[int] = self._dimensions.y
        self._explore_factor: Final = explore_factor  # Bounded by min cells per level.
        self._merge_factor: Final = merge_factor
        self._min_cells_per_level: Final = min_cells if min_cells else \
            (self._dimensions.x * self._dimensions.z) // 5
        # 3D Cell storage ~ [level][row][column].
        self._cells: CellStorage = [
            [list() for _ in range(self._dimensions.x + 1)]
            for _ in range(self._permissible_levels + 1)
        ]
        # Flat list of level entrances.
        self._entrances: List[Optional[Cell]] = \
            [None for _ in range(self._permissible_levels)]
        self._inclusive: bool = True

        self._validate_params()

    def _validate_params(self) -> NoReturn:
        entry_: Vec3 = self._structure_entrance
        center_: Vec3 = self._structure_center
        dim_: Vec3 = self._dimensions
        # Validate blueprint properties.
        assert 0 <= self._explore_factor <= 1, \
            'Explore factor must be between 0 and 1.'
        assert self._min_cells_per_level > 2, \
            'Minimum cells must be greater than 2.'
        assert self._min_cells_per_level <= dim_.x * dim_.z, \
            'Minimum cells must be less than the total number of cells in a level.'
        # Entrance must be no part of center.
        assert entry_ != center_, 'Entrance and center must not be the same.'
        assert entry_.y != center_.y and self._permissible_levels != 1, \
            'A true three-dimensional center is required.'
        # Entrance must be within the horizontal bounding perimeter.
        assert entry_.x + dim_.x // 2 == center_.x or \
               entry_.x - dim_.x // 2 == center_.x or \
               entry_.z + dim_.z // 2 == center_.z or \
               entry_.z - dim_.z // 2 == center_.z, \
            'Center misaligned with entrance horizontally.'
        # Entrance may only be on the ground floor.
        assert entry_.y + dim_.y // 2 == center_.y, \
            'Center misaligned with entrance vertically.'

    def run_engine(self) -> NoReturn:
        """Define the order in which generate a blueprint."""
        self._create_graph()
        self._connect_graph()
        self._plan_structure()

    def _create_graph(self) -> NoReturn:
        """Create a 3D graph with empty cells."""
        # Begin generation from the ground, south-west corner.
        left_bound: Vec3 = self._structure_center - Vec3(
            self._dimensions.x // 2,
            self._dimensions.y // 2,
            self._dimensions.z // 2
        )
        for cell_index in self._seq_index_iter():
            mc_world_pos: Vec3 = left_bound + cell_index
            self._cells[cell_index.y][cell_index.x].append(
                Cell(mc_world_pos, CellType.DETACHED)
            )

    def _connect_graph(self) -> NoReturn:
        # Connect all cells.
        for cell_index in self._seq_index_iter():
            neighbours: NeighbouringCells = NeighbouringCells(
                NORTH=self._get_cell(cell_index + Vec3(1, 0, 0)),
                SOUTH=self._get_cell(cell_index + Vec3(-1, 0, 0)),
                EAST=self._get_cell(cell_index + Vec3(0, 0, 1)),
                WEST=self._get_cell(cell_index + Vec3(0, 0, -1)),
                UP=self._get_cell(cell_index + Vec3(0, 1, 0)),
                DOWN=self._get_cell(cell_index + Vec3(0, -1, 0))
            )
            target_cell: Cell = self._get_cell(cell_index)
            target_cell.neighbours = neighbours

    @abstractmethod
    def _plan_structure(self) -> NoReturn:
        """
        Subclass hook.
        Delegates work in a specific order to create a cohesive structure.
        """

    @abstractmethod
    def _create_structure_entry(self) -> NoReturn:
        """
        Subclass hook.
        Finds and designates a ground level entrance.
        """

    @abstractmethod
    def _plan_ground_level(self) -> NoReturn:
        """
        Subclass hook.
        Plans the first floor.
        """

    @abstractmethod
    def _plan_higher_level(self, level_no: int) -> NoReturn:
        """
        Subclass hook.
        Plan levels above the first floor.
        """

    @abstractmethod
    def _create_higher_level_entry(
            self,
            level_no: int
    ) -> Annotated[Cell, 'Level entrance']:
        """
        Subclass hook.
        Finds and designates a level entry cell for higher levels.
        """

    @abstractmethod
    def _level_traversal(
            self,
            start_cell: Cell,
            *,
            generative_type: Annotated[
                CellType, 'Cell type to generate'
            ] = CellType.REGULAR,
            _predicate: Callable[
                [str, Cell], bool
            ] = lambda c: True
    ) -> NoReturn:
        """
        Subclass hook.
        Using BFS, navigates the level from a specified location and
        dynamically converts traversed cells to a generative type.
        """

    @abstractmethod
    def _merge_cells(self) -> NoReturn:
        """
        Subclass hook.
        Merges smaller cells to create larger spaces.
        """

    def _get_random_cell(
            self,
            level: int,
            *,
            _predicate: Callable[
                [Cell], bool
            ] = lambda c: True
    ) -> Optional[Cell]:
        # Get a random cell from a level.
        try:
            return random.choice(
                [cell for cell in self._flatten(level) if _predicate(cell)]
            )
        except IndexError:
            return None

    @staticmethod
    def _get_random_cell_neighbour(
            cell: Cell,
            *,
            _predicate: Callable[
                [str, Cell], bool
            ] = lambda d, n: True
    ) -> Optional[Cell]:
        """Get a random neighbouring cell."""
        assert cell is not None, 'Hook cell cannot be None.'
        neighbours: List[Optional[Cell]] = [
            neighbour
            for direction, neighbour in cell.neighbours.items()
            if neighbour is not None and _predicate(direction, neighbour)
        ]
        try:
            return random.choice(neighbours)
        except IndexError:
            return None

    @staticmethod
    def breadth_traversal(
            start: Cell,
            /, *,
            _predicate: Callable[
                [str, Cell], bool
            ] = lambda k, c: True
    ) -> Iterator[Cell]:
        """
        Breadth first traversal of the structure.
        Args:
            start (Cell): Traversal is relative to the starting cell.
            _predicate (Callable): Predicate function determines the behavior
             of the breadth-first traversal by filtering cells based on its
             criteria.
        """
        visited: Set[Cell] = set()
        queue: Deque[Cell] = deque([start])
        while queue:
            cell = queue.popleft()
            if cell not in visited:
                visited.add(cell)
                yield cell
                cells_to_explore: List[Cell] = [
                    c for k, c in cell.neighbours.items()
                    if c is not None and _predicate(k, c)
                ]
                queue.extend(cells_to_explore)

    @final
    def _get_cell(self, pos: Vec3) -> Optional[Cell]:
        """Helper to safely get a cell from cell storage."""
        try:
            return self._cells[pos.y][pos.x][pos.z]
        except IndexError:
            return None

    @final
    def _flatten(self, level_no: Optional[int] = None) -> List[Cell]:
        # Flatten a 3D signature into a single dimensional list.
        if level_no is None:
            # Flatten all levels.
            return [
                cell
                for level in self._cells
                for row in level
                for cell in row
            ]
        assert 0 <= level_no <= self._permissible_levels, \
            f'Level {level_no} is not permitted.'
        # Flatten a specific level.
        return [
            cell
            for row in self._cells[level_no]
            for cell in row
        ]

    def _seq_index_iter(self) -> Iterator[Vec3]:
        levels, rows, columns = map(
            lambda x: x + 1 if self._inclusive else x,
            (self._permissible_levels, self._dimensions.x, self._dimensions.z)
        )
        for level in range(levels):
            for row in range(rows):
                for column in range(columns):
                    yield Vec3(row, level, column)

    def __iter__(self) -> Iterator[Cell]:
        # Iterate over all cells in numerical order.
        for level in self._cells:
            for row in level:
                yield from row

    @final
    def __len__(self) -> int:
        # Len of all cells that will be generated.
        return len(
            [cell for cell in self._flatten()
             if cell.type_ != CellType.DETACHED]
        )

    def __repr__(self) -> str:
        dim_: Vec3 = self._dimensions.clone()
        if self._inclusive:
            dim_ = dim_ + Vec3(1, 1, 1)
        max_cells: int = dim_.x * dim_.y * dim_.z
        return f'Structure(levels:{self._permissible_levels}, ' \
               f'cells:{len(self)}/{max_cells})'

    def __getitem__(self, pos: Vec3) -> Cell:
        # Get cell by position.
        cell: Optional[Cell] = next(
            (cell for cell in self if cell.pos == pos),
            None
        )
        if cell is None:
            raise CellDoesNotExist(pos)
        return cell

    @property
    def signature(self) -> CellStorage:
        return self._cells

    @property
    def dimensions(self) -> Vec3:
        return self._dimensions


class ResidentialBlueprint(Blueprint):
    def _plan_structure(self) -> NoReturn:
        """Delegates the planning of the structure blueprint."""
        self._create_structure_entry()
        self._plan_ground_level()
        # Plan all other levels.
        for level_no in range(1, self._permissible_levels):
            self._plan_higher_level(level_no)
        # Create rooms out of smaller cells.
        self._merge_cells()

    def _create_structure_entry(self) -> NoReturn:
        # Register structure entrance on first level.
        entrance = self._structure_entrance
        first_level: CellStorageLevel = self._cells[0]
        cell = next(
            (cell
             for row in first_level
             for cell in row
             if cell.pos == entrance), None
        )
        assert cell is not None, f'Entrance at {entrance} not found.'
        cell.type_ = CellType.STRUCTURE_ENTRY
        self._entrances[0] = cell

    def _plan_ground_level(self) -> NoReturn:
        assert self._entrances[0] is not None, 'Structure entry is not set.'
        # Plan the first level.
        structure_entrance: Cell = self._entrances[0]
        self._level_traversal(
            structure_entrance,
            _predicate=lambda k, c: k not in ('UP', 'DOWN')
        )

    def _plan_higher_level(self, level_no: int) -> NoReturn:
        # Entrance to level is on previous level.
        level_entry: Cell = self._create_higher_level_entry(level_no)
        # Current floor.
        above_level_entry: Optional[Cell] = level_entry.neighbours.get('UP')
        # Reserve the room above level entry.
        if above_level_entry is not None:
            above_level_entry.type_ = CellType.ABOVE_LEVEL_ENTRY
        # Generate the level.
        self._level_traversal(
            above_level_entry,
            _predicate=lambda k, c: k not in ('UP', 'DOWN') and
                                    c.neighbours.get('DOWN') is not None
        )

    def _create_higher_level_entry(
            self,
            level_no: int
    ) -> Annotated[Cell, 'Level entrance']:
        assert level_no <= self._permissible_levels, \
            f'{level_no} is higher then what is permitted: {self._permissible_levels}'
        assert level_no != 0, 'Level 0 is the structure entry.'
        # Find suitable level entry on the previous floor.
        previous_level_no: int = level_no - 1
        level_entry: Optional[Cell] = self._get_random_cell(
            previous_level_no,
            _predicate=lambda c: c.type_ == CellType.REGULAR and
                                 c.neighbours.get('UP') is not None
        )
        # Ensure level guidelines are followed.
        assert level_entry is not None, \
            f'No cells found on level {previous_level_no}.'
        level_entry.type_ = CellType.LEVEL_ENTRY
        self._entrances[level_no] = level_entry
        # Above level entry handled by level planner.
        return level_entry

    def _level_traversal(
            self,
            start_cell: Cell,
            *,
            generative_type: Annotated[
                CellType, 'Cell type to generate'
            ] = CellType.REGULAR,
            _predicate: Callable[
                [str, Cell], bool
            ] = lambda k, c: True
    ) -> NoReturn:
        for cell_count, cell in enumerate(
                self.breadth_traversal(
                    start_cell,
                    _predicate=_predicate
                )
        ):
            halt_traversal: bool = random.random() > self._explore_factor
            if halt_traversal and cell_count > self._min_cells_per_level:
                break
            if cell is not start_cell:
                cell.type_ = generative_type

    def _merge_cells(self) -> NoReturn:
        assert None not in self._entrances, f'Entrance(s) missing.'
        # Create larger cells by merging smaller ones.
        for entry in self._entrances:
            for cell in self.breadth_traversal(
                    entry,
                    _predicate=lambda k, c:
                    k not in ('UP', 'DOWN') and
                    c.type_ in (CellType.REGULAR, CellType.EMPTY)
            ):
                merge_cell: bool = random.random() > self._merge_factor
                if not merge_cell:
                    continue
                if other := self._get_random_cell_neighbour(
                        cell,
                        _predicate=lambda _, c:
                        c.type_ in (CellType.REGULAR, CellType.EMPTY)
                ):
                    cell.add_merged_cell(other)
                    other.add_merged_cell(cell)


@final
class HouseBlueprint(ResidentialBlueprint):
    """TODO"""


@final
class ApartmentBlueprint(ResidentialBlueprint):
    """TODO"""


@final
class SkyscraperBlueprint(ResidentialBlueprint):
    """TODO"""


@unique
class BlueprintType(Enum):
    HOUSE = auto()
    APARTMENT = auto()
    SKYSCRAPER = auto()


class BlueprintFactory:
    __blueprint_types: Final = {
        BlueprintType.HOUSE: HouseBlueprint,
        BlueprintType.APARTMENT: ApartmentBlueprint,
        BlueprintType.SKYSCRAPER: SkyscraperBlueprint
    }

    @classmethod
    def create(
            cls,
            type_: BlueprintType,
            size: Vec3,
            /,
            entrance: Vec3,
            center: Vec3,
            *,
            explore_factor: Annotated[
                float, '0 <= x <= 1'
            ] = 0.7,
            merge_factor: Annotated[
                float, '0 <= x <= 1'
            ] = 0.5,
            min_cells: Optional[
                Annotated[int, 'x > 2']
            ] = None
    ) -> Blueprint:
        return cls.__blueprint_types[type_](
            size,
            entrance,
            center,
            explore_factor=explore_factor,
            merge_factor=merge_factor,
            min_cells=min_cells
        )