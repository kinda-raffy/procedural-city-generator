from utils.temp import Vec3
from typing import Literal


class Cell:
    def __init__(self, vec: Vec3, c_type: Literal["door", "pool", "stair", "empty"]):
        self.__pos: Vec3 = vec
        self.type = c_type

    def __repr__(self):
        return f"Cell({str(self.__pos)}, {self.type})"

    def __eq__(self, other):
        return self.__pos == other.__pos and self.type == other.type

    def __hash__(self):
        # Don't allow for overlapping cells.
        return hash(self.__pos)
