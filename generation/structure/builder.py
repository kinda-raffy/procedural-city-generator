from __future__ import annotations
from abc import (
    ABCMeta,
    abstractmethod,
)
from enum import Enum
from typing import (
    TypedDict,
    Optional,
    Tuple,
    Final,
    NoReturn,
    List,
    Self,
    final,
)

import random
import logging

# Components.
from generation.structure.components.frame import (
    Frame,
    DefaultFrame,
)
from generation.structure.components.stairs import (
    Stair,
    StairFactory,
    StairType,
)
from generation.structure.components.door import (
    Door,
    DoorFactory,
)
from generation.structure.components.pool import (
    Pool,
    CellPool,
    PoolFacade,
    PoolStructure,
    PoolStructureType,
    PoolStructureFactory,
)
from generation.structure.components.roof import (
    Roof,
    RoofFactory,
    RoofType,
)
from generation.structure.components.windows import (
    Window,
    WindowFactory,
    WindowType,
)

# Structure.
from generation.structure.cell import (
    CellType,
    CellDirection,
)
from env import (
    MaterialPack,
    Environment,
)
from blueprint import (
    Blueprint,
    BlueprintType,
    BlueprintFactory,
)

from mcpi.vec3 import Vec3
from generation.biome import Biome
from generation.structure.errors.structure import BuilderNotImplemented



__all__ = [
    'GlobalComponentsPreference',
    'GlobalComponents',
    'Builder',
    'ResidentialBuilder',
    'HouseBuilder',
    'ApartmentBuilder',
    'SkyscraperBuilder',
]

logger = logging.getLogger('structure')

class GlobalComponentsPreference(TypedDict):
    """
    User defined global component preferences to be
    used during building.
    If no type is specified, the component is not
    bound to any types, and all types will be allowed.
    If a tuple is provided where it is allowed, a type
    will be chosen at random.
    Concrete methods may override global
    preferences to generate unique types per cell.
    """
    StairType: Optional[Tuple[StairType, ...]]
    RoofType: Optional[Tuple[RoofType, ...]]
    WindowType: Optional[Tuple[WindowType, ...]]
    PoolStructureType: Optional[PoolStructureType]


class GlobalComponents(TypedDict):
    """
    Chosen global components
    that will be used during building.
    """
    StairType: StairType
    RoofType: RoofType
    WindowType: WindowType
    PoolStructureType: PoolStructureType


class Builder(metaclass=ABCMeta):
    # TODO ~ Add Documentation.
    # TODO ~ Add custom cell dimension support to builder methods.
    def __init__(
            self,
            biome: Biome,
            /, *,
            build_dimensions: Vec3,
            entry: Vec3,
            center: Vec3
    ):
        self._biome: Final[Biome] = biome,
        self._size: Final = build_dimensions
        self._entrance: Final = entry
        self._structure_center: Final = center
        self._blueprint: Optional[Blueprint] = None
        self._materials: Optional[MaterialPack] = None
        self._global_component_spec: Optional[
            GlobalComponents
        ] = None

    @abstractmethod
    def _generate_blueprint(self) -> Blueprint:
        """Generate a structural blueprint."""

    @abstractmethod
    def _add_external_obj(self) -> NoReturn:
        """
        Dispatches the addition of external
        decorative objects around the
        surrounding environment.
        """

    @staticmethod
    @abstractmethod
    def global_component_preference() -> GlobalComponentsPreference:
        """Specify the components preferred."""

    @staticmethod
    def _evaluate_components(spec) -> GlobalComponents:
        """
        Evaluate preferred components
        and choose a component type to build.
        """
        # Evaluate specification.
        for component, value in spec.items():
            if value is None:
                loaded_component: Enum = eval(component)
                component_types: List[str] = \
                    loaded_component.__dict__['_member_names_']
                assert len(component_types) > 0, \
                    f'No component types found for {component}'
                selected_type: str = random.choice(component_types)
                spec[component] = loaded_component[selected_type]
            else:
                spec[component] = random.choice(value)
        assert all([type_ is not None for type_ in spec.values()]), \
            'Component specification is invalid.'
        logger.debug(f'Global component specification: {spec}')
        return spec

    def __enter__(self) -> Self:
        """
        Perform required initialization before
        building and logging.
        """
        logger.info(f'Building structure of type {self.__class__.__name__}')
        self._global_component_spec = self._evaluate_components(
            self.global_component_preference()
        )
        self._blueprint = self._generate_blueprint()
        env = Environment(
            biome=self._biome,
            builder=type(self)
        )
        env.clear_block(self._size, ground=self._entrance.y)
        self._materials = env.get_material_pack()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> Optional[bool]:
        """
        Perform clean up, add external decorative
        items and logging.
        """
        if exc_type is not None:
            # If error occurs while building, reset the build area.
            logger.error(f'Error occurred while building: {exc_val}')
            logger.exception(exc_tb)
            Environment.clear_block(self._size, ground=self._entrance.y)
            return False  # Let the exception propagate.
        self._add_external_obj()
        logger.info(f'Finished building structure {self}.')

    def __repr__(self) -> str:
        return f'<{self.__class__.__name__} at {self._structure_center}>'

    @final
    def __len__(self) -> int:
        assert self._blueprint is not None
        return len(self._blueprint)

    @property
    def biome(self) -> Biome:
        return self._biome

    @property
    def blueprint(self) -> Blueprint:
        return self._blueprint


class ResidentialBuilder(Builder, metaclass=ABCMeta):
    @abstractmethod
    def create_structure(self) -> NoReturn: ...
    @abstractmethod
    def create_stairs(self) -> NoReturn: ...
    @abstractmethod
    def create_doors(self) -> NoReturn: ...
    @abstractmethod
    def create_roof(self) -> NoReturn: ...
    @abstractmethod
    def create_pool(self) -> NoReturn: ...
    @abstractmethod
    def create_windows(self) -> NoReturn: ...


@final
class HouseBuilder(ResidentialBuilder):
    def global_component_preference(self) -> GlobalComponentsPreference:
        return {
            'StairType': None,
            'RoofType': None,
            'WindowType': (WindowType.DOUBLE_BAR, WindowType.HORIZONTAL_STRIP, WindowType.FULL),
            'PoolStructureType': None,
        }

    def _generate_blueprint(self) -> Blueprint:
        blueprint: Blueprint = BlueprintFactory().create(
            BlueprintType.HOUSE,
            self._size,
            entrance=self._entrance,
            center=self._structure_center,
            explore_factor=0.5
        )
        blueprint.run_engine()
        return blueprint

    def create_structure(self) -> NoReturn:
        logger.debug('Creating structural frame.')
        for cell in self._blueprint:
            frame: Frame = DefaultFrame(
                cell,
                self._materials
            )
            frame.set_cell_frame()
            frame.perform_cell_merge()
            frame.set_cell_floor()
            frame.set_external_pillars()
            frame.set_internal_pillars()

    def create_stairs(self) -> NoReturn:
        # Uses global stairs.
        stair_type: StairType = self._global_component_spec['StairType']
        logger.debug(f'Placing stairs of type {stair_type}.')
        for cell in self._blueprint.breadth_traversal(
                self._blueprint[self._entrance],
                _predicate=lambda k, c: c.type_ == CellType.LEVEL_ENTRY
        ):
            stair: Stair = StairFactory().create(
                cell.pos,
                self._materials,
                stair_type,
            )
            stair.clear_room()
            stair.set_current_stairs()
            stair.set_above_stairs()

    def create_doors(self) -> NoReturn:
        logger.debug('Placing doors.')
        for cell in self._blueprint:
            door: Door = DoorFactory().create(
                cell.pos,
                self._materials
            )
            door.place_single_door()

    def create_roof(self) -> NoReturn:
        # Uses global roof.
        roof_type: RoofType = self._global_component_spec['RoofType']
        logger.debug(f'Placing roof of type {roof_type}.')
        for cell in self._blueprint.breadth_traversal(
                self._blueprint[self._entrance],
                _predicate=lambda k, c: c.type_ != CellType.POOL
        ):
            roof: Roof = RoofFactory().create(
                cell.pos,
                self._materials,
                roof_type,
            )
            roof.place_base()
            roof.place_corners()

    def create_pool(self) -> NoReturn:
        # Uses global pool structure and roof.
        pool_struct_type: PoolStructureType = \
            self._global_component_spec['PoolStructureType']
        logger.debug(f'Placing pool of type {pool_struct_type}.')
        roof_type: RoofType = self._global_component_spec['RoofType']
        for cell in self._blueprint.breadth_traversal(
                self._blueprint[self._entrance],
                _predicate=lambda k, c: c.type_ == CellType.POOL
        ):
            pool: Pool = CellPool(
                cell.pos,
                self._materials,
            )
            pool_struct: PoolStructure = PoolStructureFactory().create(
                cell.pos,
                self._materials,
                pool_struct_type,
                pool_roof=roof_type,
            )
            pool_facade: PoolFacade = PoolFacade(
                pool,
                pool_struct,
            )
            pool_facade.build()

    def create_windows(self) -> NoReturn:
        # TODO ~ Add builder support for directional windows.
        # Overrides global windows.
        window_type: WindowType = random.choice(
            [WindowType.DOUBLE_BAR, WindowType.HORIZONTAL_STRIP, WindowType.FULL]
        )
        logger.debug(f'Placing windows of type {window_type}.')
        for cell in self._blueprint.breadth_traversal(
                self._blueprint[self._entrance],
                _predicate=lambda k, c: c.faces_environment()
        ):
            outside_faces: Tuple[CellDirection, ...] = \
                cell.faces_environment_direction()
            for face in outside_faces:
                window: Window = WindowFactory().create(
                    cell.pos,
                    self._materials,
                    cell_window_faces=face,
                    window_type=window_type,
                )
                window.place()

    def _add_external_obj(self) -> NoReturn:
        logger.debug('Adding external objects.')
        self._add_family()
        self._add_flowers()

    def _add_family(self) -> NoReturn:
        """TODO ~ Add a family of villagers."""

    def _add_flowers(self) -> NoReturn:
        """TODO ~ Add flowers around the perimeter."""


@final
class ApartmentBuilder(ResidentialBuilder):
    def __new__(cls, *args, **kwargs):
        # TODO ~ Implement apartment builder.
        raise BuilderNotImplemented(cls)

    def global_component_preference(self) -> GlobalComponentsPreference:
        return {
            'StairType': None,
            'RoofType': (RoofType.FLAT, RoofType.ANGLED_FLAT),
            'WindowType': (WindowType.DOUBLE_BAR, WindowType.FULL),
            'PoolStructureType': None,
        }

    def _generate_blueprint(self) -> Blueprint:
        blueprint: Blueprint = BlueprintFactory().create(
            BlueprintType.APARTMENT,
            self._size,
            entrance=self._entrance,
            center=self._structure_center,
        )
        blueprint.run_engine()
        return blueprint

    def create_structure(self) -> NoReturn: ...
    def create_stairs(self) -> NoReturn: ...
    def create_doors(self) -> NoReturn: ...
    def create_roof(self) -> NoReturn: ...
    def create_pool(self) -> NoReturn: ...
    def create_windows(self) -> NoReturn: ...
    def _add_external_obj(self) -> NoReturn: ...


@final
class SkyscraperBuilder(ResidentialBuilder):
    def __new__(cls, *args, **kwargs):
        # TODO ~ Implement skyscraper builder.
        raise BuilderNotImplemented(cls)

    def global_component_preference(self) -> GlobalComponentsPreference:
        return {
            'StairType': (StairType.DOUBLE, StairType.DOUBLE_SLAB),
            'RoofType': tuple(RoofType.FLAT),
            'WindowType': tuple(WindowType.FULL),
            'PoolStructureType': None,
        }

    def _generate_blueprint(self) -> Blueprint:
        blueprint: Blueprint = BlueprintFactory().create(
            BlueprintType.SKYSCRAPER,
            self._size,
            entrance=self._entrance,
            center=self._structure_center,
        )
        blueprint.run_engine()
        return blueprint

    def create_structure(self) -> NoReturn: ...
    def create_stairs(self) -> NoReturn: ...
    def create_doors(self) -> NoReturn: ...
    def create_roof(self) -> NoReturn: ...
    def create_pool(self) -> NoReturn: ...
    def create_windows(self) -> NoReturn: ...
    def _add_external_obj(self) -> NoReturn: ...
