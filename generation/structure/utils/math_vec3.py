from __future__ import annotations
from typing import overload
from mcpi.vec3 import Vec3


class MathVec3(Vec3):
    """Extends mcpi.vec3 with mathematical dunders."""

    def __truediv__(self, other: MathVec3) -> MathVec3:
        return MathVec3(self.x / other, self.y / other, self.z / other)

    def __itruediv__(self, other: MathVec3) -> MathVec3:
        return MathVec3(self / other)

    def __floordiv__(self, other: MathVec3) -> MathVec3:
        return MathVec3(self.x // other, self.y // other, self.z // other)

    def __abs__(self) -> MathVec3:
        return MathVec3(abs(self.x), abs(self.y), abs(self.z))

    def __hash__(self) -> int:
        return hash((self.x, self.y, self.z))

    def __mod__(self, other: MathVec3) -> MathVec3:
        return MathVec3(self.x % other, self.y % other, self.z % other)
