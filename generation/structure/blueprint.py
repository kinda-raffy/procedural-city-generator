from abc import *
from mcpi import *
from cell import *
from typing import *
from collections import *


class StructureSkeleton(metaclass=ABCMeta):
    def __init__(self, size: Vec3):
        self.__x, self.__y, self.__z = size
        self.permissible_levels = self.__y
        # Indexes represents levels.
        self.entrances: List[Cell | None] = [None for _ in range(self.permissible_levels)]

    def plan_cells(self): ...

    def plan_level(self, signature): ...

    def _get_signature(self): ...

    def __iter__(self):
        # BFS.
        ...

    def __len__(self):
        # Len of all cells in all levels.
        ...

    def __repr__(self):
        return f'Structure(level:{self.permissible_levels}, len{len(self)})'

    def __getitem__(self, level: int) -> Cell:
        # Get entrance node on a level basis.
        assert level <= self.permissible_levels, f'{level} is higher then what is permitted: {self.permissible_levels}'
        return self.entrances[level]
