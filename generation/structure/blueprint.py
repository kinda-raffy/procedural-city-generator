# FIXME ~ Narrow
from abc import *
from mcpi.vec3 import Vec3
from cell import *
from typing import *
from collections import *
from enum import *
import random

__all__ = [
    'CellStorage',
    'CellStorageLevel',
    'CellStorageRow',
    'Direction',
    'Blueprint',
    'ResidentialBlueprint',
    'HouseBlueprint',
    'ApartmentBlueprint',
    'SkyscraperBlueprint',
    'BlueprintType',
    'BlueprintFactory',
]

CellStorage = List[List[List[Cell]]]
CellStorageLevel = List[List[Cell]]
CellStorageRow = List[Cell]
Direction = Literal['NORTH', 'SOUTH', 'EAST', 'WEST', 'UP', 'DOWN']


class Blueprint(metaclass=ABCMeta):
    """
    Base Blueprint Class defining the minimum design
    requirements for a blueprint.
    """

    def __init__(
            self,
            size: Vec3,
            /,
            entrance: Vec3,
            *,
            explore_factor: Annotated[
                float, '0 <= x <= 1'
            ] = 0.7,
            merge_factor: Annotated[
                float, '0 <= x <= 1'
            ] = 0.5,
            min_cells: Optional[
                Annotated[int, 'x > 2']
            ] = None,
    ):
        assert 0 <= explore_factor <= 1, 'Explore factor must be between 0 and 1.'
        assert min_cells > 2, 'Minimum cells must be greater than 2.'
        assert min_cells <= size.x * size.z, \
            'Minimum cells must be less than the total number of cells in a level.'

        self._dimensions: Final = size
        self._structure_entrance: Final = entrance
        self._permissible_levels: Final[int] = self._dimensions.y
        self._explore_factor: Final = explore_factor
        self._merge_factor: Final = merge_factor
        self._min_cells_per_level: Final = min_cells if min_cells else \
            (self._dimensions.x * self._dimensions.z) // 2
        # 3D Cell storage [level][row][column].
        self._cells: CellStorage = [
            [list() for _ in range(self._dimensions.x)]
            for _ in range(self._permissible_levels)
        ]
        # Flat list of level entrances.
        self._entrances: List[Optional[Cell]] = \
            [None for _ in range(self._permissible_levels)]

    def run_engine(self) -> NoReturn:
        """Define the order in which a blueprint is generated."""
        self._create_graph()
        self._connect_graph()
        self._plan_structure()

    def _create_graph(self) -> NoReturn:
        # Create a 3D graph with empty cells.
        for level in range(self._permissible_levels):
            for row in range(self._dimensions.x):
                for column in range(self._dimensions.z):
                    self._cells[level][row].append(
                        Cell(Vec3(row, level, column), CellType.DETACHED)
                    )

    def _connect_graph(self) -> NoReturn:
        # Connect all cells.
        for cell in self:
            neighbours: NeighbouringCells = NeighbouringCells(
                NORTH=self._get_cell(cell.pos + Vec3(1, 0, 0)),
                SOUTH=self._get_cell(cell.pos + Vec3(-1, 0, 0)),
                EAST=self._get_cell(cell.pos + Vec3(0, 0, 1)),
                WEST=self._get_cell(cell.pos + Vec3(0, 0, -1)),
                UP=self._get_cell(cell.pos + Vec3(0, 1, 0)),
                DOWN=self._get_cell(cell.pos + Vec3(0, -1, 0))
            )
            cell.neighbours = neighbours

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
        # Get a random cell from the level.
        return random.choice(
            [cell for cell in self._flatten(level) if _predicate(cell)]
        )

    @staticmethod
    def _get_random_cell_neighbour(
            cell: Cell,
            *,
            _predicate: Callable[
                [str, Cell], bool
            ] = lambda d, n: True
    ) -> Optional[Cell]:
        """Get a random neighbouring cell."""
        neighbours: List[Optional[Cell]] = [
            neighbour
            for direction, neighbour in cell.neighbours.items()
            if _predicate(direction, neighbour) and neighbour is not None
        ]
        return random.choice(neighbours)

    @staticmethod
    def breadth_traversal(
            start: Cell,
            /, *,
            _predicate: Callable[
                [str, Cell], bool
            ] = lambda k, c: True  # All cells will be considered.
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
                    if _predicate(k, c) and c is not None
                ]
                queue.extend(cells_to_explore)

    @final
    def _get_cell(self, pos: Vec3) -> Optional[Cell]:
        """Helper to safely get a cell from cell storage."""
        try:
            self._cells[pos.y][pos.x][pos.z]
        except IndexError:
            return None

    @final
    def _flatten(self, level: Optional[int] = None) -> List[Cell]:
        # Flatten a 3D signature into a single dimensional list.
        assert 0 < level <= self._permissible_levels, \
            f'Level {level} is not permitted.'
        if level is None:
            # Flatten all levels.
            return [
                cell
                for level in self._cells
                for row in level
                for cell in row
            ]
        # Flatten a specific level.
        return [
            cell
            for row in self._cells[level]
            for cell in row
        ]

    @final
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
        return f'Structure(levels:{self._permissible_levels}, cells:{len(self)})'

    @final
    def __setitem__(self, level: int, cell: Cell) -> NoReturn:
        # Set entrance node on a level basis.
        assert level <= self._permissible_levels, \
            f'{level} is higher then what is permitted: {self._permissible_levels}'
        cell.type_ = CellType.STRUCTURE_ENTRY if level == 0 else CellType.LEVEL_ENTRY
        self._entrances[level] = cell

    @final
    def __getitem__(self, level: int) -> Cell:
        # Get entrance node on a level basis.
        assert level <= self._permissible_levels, \
            f'{level} is higher then what is permitted: {self._permissible_levels}'
        return self._entrances[level]

    @property
    def signature(self) -> CellStorage:
        return self._cells

    @property
    def dimensions(self) -> Vec3:
        return self._dimensions


class ResidentialBlueprint(Blueprint):
    def _plan_structure(self) -> NoReturn:
        """Plan the structure blueprint."""
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
        assert cell, f'Entrance at {entrance} not found.'
        cell.type_ = CellType.ENTRANCE
        self._entrances[0] = cell

    def _plan_ground_level(self) -> NoReturn:
        assert self._entrances[0], 'Structure entry is not set.'
        # Plan the first level.
        structure_entrance: Cell = self._entrances[0]
        self._level_traversal(
            structure_entrance,
            _predicate=lambda k, c: k not in ('UP', 'DOWN')
        )

    def _plan_higher_level(self, level_no: int) -> NoReturn:
        level_entry: Cell = self._create_higher_level_entry(level_no)
        # Reserve the room above level entry.
        above_level_access: Optional[Cell] = level_entry.neighbours.get('UP')
        if above_level_access is not None:
            above_level_access.type_ = CellType.ABOVE_LEVEL_ENTRY

        # Generate the level.
        self._level_traversal(
            level_entry,
            _predicate=lambda k, c:
            k not in ('UP', 'DOWN') and c.neighbours.get('DOWN') is not None
        )

    def _create_higher_level_entry(
            self,
            level_no: int
    ) -> Annotated[Cell, 'Level entrance']:
        assert level_no <= self._permissible_levels, \
            f'{level_no} is higher then what is permitted: {self._permissible_levels}'
        assert level_no != 0, 'Level 0 is the structure entry.'
        # Create a level entry.
        previous_level_no: int = level_no - 1
        level_entry: Optional[Cell] = self._get_random_cell(
            previous_level_no,
            _predicate=lambda c: c.type_ == CellType.ROOM
        )
        # Sanity check in case level guidelines are not followed.
        assert level_entry is not None, \
            f'No cells found on level {previous_level_no}.'
        level_entry.type_ = CellType.LEVEL_ACCESS
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
            ] = lambda c: True
    ) -> NoReturn:
        for cell_count, cell in enumerate(
                self.breadth_traversal(
                    start_cell,
                    _predicate=_predicate
                )
        ):
            halt_traversal: bool = self._explore_factor > random.random()
            if halt_traversal and cell_count > self._min_cells_per_level:
                break
            if cell is not start_cell:
                cell.type_ = generative_type

    def _merge_cells(self) -> NoReturn:
        # Create larger cells by merging smaller ones.
        for entry in self._entrances:
            for cell in self.breadth_traversal(
                    entry,
                    _predicate=lambda k, c:
                    k not in ('UP', 'DOWN') and
                    c.type_ in (CellType.REGULAR, CellType.EMPTY)
            ):
                merge_cell: bool = self._merge_factor > random.random()
                if not merge_cell:
                    continue
                if other := self._get_random_cell_neighbour(
                        cell,
                        _predicate=lambda c:
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
            explore_factor=explore_factor,
            merge_factor=merge_factor,
            min_cells=min_cells
        )
