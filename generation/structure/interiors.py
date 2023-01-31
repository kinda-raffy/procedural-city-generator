from utils.block_extension import BlockExt as BlocEx
from cell import Cell
from typing import (
    Dict,
    Union,
    NotRequired,
    TypedDict,
)
from dataclasses import dataclass, field
import tomllib

__all__ = ["InteriorPack", "Interior"]


class InteriorPack(TypedDict):
    """
    Global furniture pack for structural generation.
    Scales with the size of a given cell.
    Divided into 3 categories:
        - `true`: The true 3-Dimensional center of a cell.
        - `side-center`: The center of a cell's 2-Dimensional side.
        - `corner`: The corner of a cell's 2-Dimensional side.
    """

    # Sunder identifiers.
    _name_: NotRequired[str]
    _variation_: NotRequired[int]
    _description_: NotRequired[str]
    _destructive_: bool
    # True cell center.
    true_center_floor: BlocEx
    true_center: BlocEx
    true_center_ceil: BlocEx
    # Relative center of a given cell's ceil-side.
    center_ceil_front: BlocEx
    center_ceil_back: BlocEx
    center_ceil_right: BlocEx
    center_ceil_left: BlocEx
    # Relative center of a given cell's floor-side.
    center_floor_front: BlocEx
    center_floor_back: BlocEx
    center_floor_right: BlocEx
    center_floor_left: BlocEx
    # Ceiling corners: Front.
    corner_ceil_front_right: BlocEx
    corner_ceil_front_left: BlocEx
    # Ceiling corners: Back.
    corner_ceil_back_right: BlocEx
    corner_ceil_back_left: BlocEx
    # Floor corners: Front.
    corner_floor_front_right: BlocEx
    corner_floor_front_left: BlocEx
    # Floor corners: Back.
    corner_floor_back_right: BlocEx
    corner_floor_back_left: BlocEx


InteriorCollection = Dict[str, Union[str, Dict[str, str]]]


def _load_interior_collection() -> InteriorCollection:
    """Load interior config file"""
    with open("config/interior.toml", "rb") as f:
        config = tomllib.load(f)
    return config["interior"]


@dataclass(frozen=True, kw_only=True)
class Interior:
    """
    A collection of furniture for a given cell.
    """

    blueprint: Dict[str, Cell]
    interior_collection: InteriorCollection = field(
        init=False, default_factory=_load_interior_collection
    )

    def place_interior(self) -> None:
        """Place interior furniture over a given signature."""

    @staticmethod
    def get_interior_pack() -> InteriorPack:
        """Grab a random interior pack for a cell."""
