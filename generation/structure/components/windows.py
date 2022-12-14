from abc import *
from typing import *
from enum import *
from generation import connection as server_conn
from generation.structure.env import MaterialPack
from mcpi.vec3 import Vec3


@unique
class WindowType(StrEnum):
    DOUBLE_BAR = auto()
    HORIZONTAL_STRIP = auto()
    PLUS = auto()
    SINGLE_CENTER = auto()
    FULL = auto()


@unique
class WindowOrientation(StrEnum):
    VERTICAL = auto()
    HORIZONTAL = auto()


class WindowPos(NamedTuple):
    start: Vec3
    stop: Vec3


class BaseWindow(metaclass=ABCMeta):
    """Window Interface."""

    def __init__(
            self,
            window_pos: WindowPos,
            /,
            materials: MaterialPack,
    ) -> NoReturn:
        self._materials: Final = materials
        self._start_pos: Final = window_pos.start
        self._end_pos: Final = window_pos.stop

    @abstractmethod
    def place(self) -> NoReturn:
        """Places the window."""


class DirectionalWindow(BaseWindow, metaclass=ABCMeta):
    """Windows were placement varies depending on direction."""

    def __init__(
            self,
            window_pos: WindowPos,
            /,
            materials: MaterialPack,
            *,
            direction: WindowOrientation
    ) -> NoReturn:
        super().__init__(window_pos, materials)
        self.__direction: Final = direction

    def place(self) -> NoReturn:
        """Places the window based on direction."""
        match self.__direction:
            case WindowOrientation.HORIZONTAL:
                self._place_horizontal()
            case WindowOrientation.VERTICAL:
                self._place_vertical()

    @abstractmethod
    def _place_vertical(self) -> NoReturn:
        """Places the window vertically."""

    @abstractmethod
    def _place_horizontal(self) -> NoReturn:
        """Places the window horizontally."""


class DoubleBarWindow(BaseWindow):

    def place(self) -> NoReturn:
        start_pos: Vec3 = self._start_pos
        end_pos: Vec3 = self._end_pos
        server_conn.setBlocks(
            start_pos + Vec3(0, 2, 0),
            end_pos + Vec3(0, 3, 0),
            self._materials['windows'],
        )


class HorizontalStripWindow(BaseWindow):

    def place(self) -> NoReturn:
        start_pos: Vec3 = self._start_pos
        end_pos: Vec3 = self._end_pos
        server_conn.setBlocks(
            start_pos + Vec3(0, 2, 0),
            end_pos + Vec3(0, 2, 0),
            self._materials['windows'],
        )


class PlusWindow(DirectionalWindow):

    def _place_vertical(self) -> NoReturn:
        start_pos: Vec3 = self._start_pos
        end_pos: Vec3 = self._end_pos
        server_conn.setBlock(
            start_pos + Vec3(1, 1, 0),
            self._materials['windows'],
        )
        server_conn.setBlock(
            start_pos + Vec3(1, 3, 0),
            self._materials['windows'],
        )
        server_conn.setBlocks(
            start_pos + Vec3(0, 2, 0),
            end_pos + Vec3(0, 2, 0),
            self._materials['windows'],
        )

    def _place_horizontal(self) -> NoReturn:
        start_pos: Vec3 = self._start_pos
        end_pos: Vec3 = self._end_pos
        server_conn.setBlock(
            start_pos + Vec3(0, 3, 1),
            self._materials['windows'],
        )
        server_conn.setBlock(
            start_pos + Vec3(0, 1, 1),
            self._materials['windows'],
        )
        server_conn.setBlocks(
            start_pos + Vec3(0, 2, 0),
            end_pos + Vec3(0, 2, 0),
            self._materials['windows'],
        )


class SingleCenterWindow(DirectionalWindow):

    def _place_vertical(self) -> NoReturn:
        start_pos: Vec3 = self._start_pos
        server_conn.setBlock(
            start_pos + Vec3(1, 2, 0),
            self._materials['windows'],
        )

    def _place_horizontal(self) -> NoReturn:
        start_pos: Vec3 = self._start_pos
        server_conn.setBlock(
            start_pos + Vec3(0, 2, 1),
            self._materials['windows'],
        )


class FullWindow(BaseWindow):

    def place(self) -> NoReturn:
        start_pos: Vec3 = self._start_pos
        end_pos: Vec3 = self._end_pos
        server_conn.setBlocks(
            start_pos + Vec3(0, 1, 0),
            end_pos + Vec3(0, 3, 0),
            self._materials['windows'],
        )


@final
class WindowFactory:
    """Window Factory. Does not retain ownership over produced instances."""

    __base_window_types: Final = {
        WindowType.DOUBLE_BAR: DoubleBarWindow,
        WindowType.HORIZONTAL_STRIP: HorizontalStripWindow,
        WindowType.FULL: FullWindow,
    }

    __directional_window_types: Final = {
        WindowType.PLUS: PlusWindow,
        WindowType.SINGLE_CENTER: SingleCenterWindow,
    }

    @classmethod
    def create(
            cls,
            window_pos: WindowPos,
            material: MaterialPack,
            /,
            window_type: WindowType = WindowType.FULL,
            *,
            direction: WindowOrientation = None
    ) -> BaseWindow:
        if direction is None:
            return cls.__base_window_types[window_type](window_pos, material)
        else:
            return cls.__directional_window_types[window_type](
                window_pos,
                material,
                direction=direction
            )
