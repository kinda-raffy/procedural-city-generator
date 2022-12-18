# FIXME ~ Narrow
from generation.structure.cell import Cell
from generation.structure.components.stairs import *
from generation.structure.components.door import *
from generation.structure.components.pool import *
from generation.structure.components.roof import *
from generation.structure.components.windows import *
from abc import ABCMeta, abstractmethod
from generation.biome import Biome
from mcpi.vec3 import Vec3
from typing import *
from env import *
from blueprint import *
from collections import *


class ComponentSpecification(TypedDict):
    """
    Specifies what component type may
    be used during build.
    If no type is specified, the
    component is not bound to
    any types, and all types
    will be allowed.
    If a tuple is provided where it is
    allowed, a type will be chosen at random.
    """
    StairType: Optional[Tuple[StairType]]
    RoofType: Optional[Tuple[RoofType]]
    WindowType: Optional[Tuple[WindowType]]
    PoolStructureType: Optional[PoolStructureType]


class Builder(metaclass=ABCMeta):
    # TODO ~ Add Documentation.
    def __init__(
            self,
            biome: Biome,
            /, *,
            dimensions: Vec3,
            entry: Vec3,
    ):
        self._biome: Final = biome,
        self._size: Final = dimensions
        self._entrance: Final = entry
        self._blueprint: Optional[Blueprint] = None
        self._materials: Optional[MaterialPack] = None
        self._component_spec: Optional[
            ComponentSpecification
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

    def _select_components(self) -> ComponentSpecification:
        """
        Decide what component to use
        based on the component specification.
        """
        spec: ComponentSpecification = ComponentSpecification(
            StairType=None,
            RoofType=None,
            WindowType=None,
            PoolStructureType=None
        )
        for component, value in spec.items():
            if value is None:
                # FIXME ~ Switch to a file.
                loaded_component: Enum = eval(component)
                component_types: List[str] =\
                    loaded_component.__dict__['_member_names_']
                assert len(component_types) > 0, \
                    f'No component types found for {component}'
                selected_type: str = random.choice(component_types)
                spec[component] = loaded_component[selected_type]
            else:
                spec[component] = random.choice(value)

    def _parse_component_spec(self) -> NoReturn:
        """
        Load the component specification.
        """
        pass

    def __enter__(self) -> Self:
        """
        Perform required initialization before
        building and logging.
        """
        self._blueprint = self._generate_blueprint()
        env = Environment(
            biome=self._biome,
            builder=type(self)
        )
        env.clear_block(self._size, ground=self._entrance.y)
        self._materials = env.get_material_pack()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> NoReturn:
        """
        Perform clean up, add external decorative
        items and logging.
        """
        self._add_external_obj()

    @final
    def __len__(self) -> int:
        assert self._blueprint is not None
        return len(self._blueprint)

    @final
    def __iter__(
            self,
            start: Cell,
            predicate: Callable[
                [str, Cell], bool
            ] = lambda k, c: True
    ) -> Iterator[Cell]:
        assert self._blueprint is not None
        yield from self._blueprint.breadth_traversal(
            start, _predicate=predicate
        )  # Breadth First Search.

    @property
    def biome(self) -> Biome:
        return self._biome

    @property
    def blueprint(self) -> Blueprint:
        return self._blueprint


class ResidentialBuilder(Builder, metaclass=ABCMeta):
    def _generate_blueprint(self) -> Blueprint: ...

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
    def _generate_blueprint(self) -> Blueprint:
        blueprint: Blueprint = BlueprintFactory().create(
            BlueprintType.HOUSE,
            self._size,
            entrance=self._entrance,
        )
        blueprint.run_engine()
        return blueprint

    def create_structure(self) -> NoReturn: ...

    def create_stairs(self) -> NoReturn:
        stair: Stair = StairFactory().create(
            StairType.,
            self._size,
            entrance=self._entrance,
        )

    def create_doors(self) -> NoReturn: ...

    def create_roof(self) -> NoReturn: ...

    def create_pool(self) -> NoReturn: ...

    def create_windows(self) -> NoReturn: ...

    def _add_external_obj(self) -> NoReturn:
        pass


@final
class ApartmentBuilder(ResidentialBuilder):
    def _generate_blueprint(self) -> Blueprint:
        blueprint: Blueprint = BlueprintFactory().create(
            BlueprintType.APARTMENT,
            self._size,
            entrance=self._entrance,
        )
        blueprint.run_engine()
        return blueprint

    def create_structure(self) -> NoReturn: ...

    def create_stairs(self) -> NoReturn: ...

    def create_doors(self) -> NoReturn: ...

    def create_roof(self) -> NoReturn: ...

    def create_pool(self) -> NoReturn: ...

    def create_windows(self) -> NoReturn: ...

    def _add_external_obj(self) -> NoReturn:
        pass


@final
class SkyscraperBuilder(ResidentialBuilder):
    def _generate_blueprint(self) -> Blueprint:
        blueprint: Blueprint = BlueprintFactory().create(
            BlueprintType.SKYSCRAPER,
            self._size,
            entrance=self._entrance,
        )
        blueprint.run_engine()
        return blueprint

    def create_structure(self) -> NoReturn:
        ...

    def create_stairs(self) -> NoReturn:
        ...

    def create_doors(self) -> NoReturn:
        ...

    def create_roof(self) -> NoReturn:
        ...

    def create_pool(self) -> NoReturn:
        ...

    def create_windows(self) -> NoReturn:
        ...

    def _add_external_obj(self) -> NoReturn:
        pass
