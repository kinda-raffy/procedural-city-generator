# FIXME ~ Narrow
from abc import *
from enum import *
from typing import *

from generation.structure.utils.block_extension import BlockExt as BlocEx
from generation.structure.env import MaterialPack
from generation import connection as server_conn
from mcpi.vec3 import Vec3


class Door(metaclass=ABCMeta):
    """Door Interface."""
    def __init__(
            self,
            door_pos: Vec3,
            /,
            material: MaterialPack
    ) -> NoReturn:
        self._materials: Final = material
        self._pos: Final = door_pos

    @abstractmethod
    def place_single_door(self) -> NoReturn:
        """Places a single door."""

    @abstractmethod
    def place_double_door(self) -> NoReturn:
        """Places a double door."""


class OakDoor(Door):
    """A legacy oak door."""
    def place_single_door(self) -> NoReturn:
        # Make room
        server_conn.setBlocks(
            self._pos + Vec3(0, 0, 0),
            self._pos + Vec3(0, 1, 0),
            BlocEx['AIR'],
        )
        assert self._materials['door'] == BlocEx['OAK_DOOR'], \
            "OakDoor can only place legacy oak doors."
        # Door window.
        server_conn.setBlock(
            self._pos + Vec3(0, 1, 0),
            self._materials['door'],
            13
        )
        # Door base.
        server_conn.setBlock(
            self._pos,
            self._materials['door'],
            2
        )

    def place_double_door(self) -> NoReturn:
        # TODO ~ Create a double door.
        super(OakDoor, self).place_double_door()


class NonOakDoor(Door):
    """A non-oak door with contemporary secondary codes."""
    def place_single_door(self) -> NoReturn:
        # Make room
        server_conn.setBlocks(
            self._pos + Vec3(0, 0, 0),
            self._pos + Vec3(0, 1, 0),
            BlocEx['AIR'],
        )
        assert self._materials['door'] != BlocEx['OAK_DOOR'], \
            "NonOakDoor cannot place legacy oak doors."
        # Door window.
        server_conn.setBlock(
            self._pos + Vec3(0, 1, 0),
            self._materials['door'],
            10
        )
        # Door base.
        server_conn.setBlock(
            self._pos,
            self._materials['door'],
            5
        )

    def place_double_door(self) -> NoReturn:
        # TODO ~ Create a double door.
        super(NonOakDoor, self).place_double_door()


@final
class DoorFactory:
    """Door Factory. Does not retain ownership over produced instances."""
    @staticmethod
    def create(
            door_pos: Vec3,
            /,
            material: MaterialPack,
    ) -> Door:
        """Creates a door."""
        if material['door'] == BlocEx['OAK_DOOR']:
            return OakDoor(door_pos, material)
        return NonOakDoor(door_pos, material)
