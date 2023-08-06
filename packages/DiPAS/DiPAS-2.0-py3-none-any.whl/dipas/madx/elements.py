from dataclasses import dataclass, is_dataclass, InitVar
import inspect
from typing import Dict, Sequence, Tuple, Type


class ElementSpecificationError(Exception):
    def __init__(self, type_: Type, spec: Dict, msg: str):
        super().__init__(f'({type_.__name__}) {msg} (initialized with: {spec})')
        self.type = type_
        self.spec = spec


@dataclass
class Element:
    @classmethod
    def from_attr_pool(cls, pool: dict):
        relevant = {k: pool[k] for k in pool.keys() & inspect.signature(cls).parameters.keys()}
        try:
            # noinspection PyArgumentList
            return cls(**relevant)
        except TypeError as err:
            raise ElementSpecificationError(cls, relevant, str(err)) from None


@dataclass
class Marker(Element):
    pass


@dataclass
class Drift(Element):
    l: float = 0


@dataclass
class SBend(Element):
    l: float
    angle: float = 0
    tilt: float = 0
    k0: float = 0
    k1: float = 0
    k2: float = 0
    k1s: float = 0
    e1: float = 0
    e2: float = 0
    fint: float = 0
    fintx: float = None
    hgap: float = 0
    h1: float = 0
    h2: float = 0
    thick: bool = False
    kill_ent_fringe: bool = False
    kill_exi_fringe: bool = False

    def __post_init__(self):
        if self.fintx is None:
            self.fintx = self.fint


@dataclass
class RBend(SBend):
    add_angle: Sequence[float] = (0, 0, 0, 0, 0)


@dataclass
class Dipedge(Element):
    h: float = 0
    e1: float = 0
    fint: float = 0
    hgap: float = 0
    tilt: float = 0


@dataclass
class Quadrupole(Element):
    l: float = 0
    k1: float = 0
    k1s: float = 0
    tilt: float = 0
    thick: bool = False


@dataclass
class Sextupole(Element):
    l: float = 0
    k2: float = 0
    k2s: float = 0
    tilt: float = 0


@dataclass
class Octupole(Element):
    l: float = 0
    k3: float = 0
    k3s: float = 0
    tilt: float = 0


@dataclass
class Multipole(Element):
    lrad: float = 0
    tilt: float = 0
    knl: Sequence[float] = (0,)
    ksl: Sequence[float] = (0,)


@dataclass
class Solenoid(Element):
    l: float = 0
    ks: float = 0
    ksi: float = 0


@dataclass
class HKicker(Element):
    l: float = 0
    kick: float = None
    tilt: float = 0
    hkick: InitVar[float] = None

    def __post_init__(self, hkick):
        if self.kick is None:
            self.kick = hkick or 0


@dataclass
class VKicker(Element):
    l: float = 0
    kick: float = None
    tilt: float = 0
    vkick: InitVar[float] = None

    def __post_init__(self, vkick):
        if self.kick is None:
            self.kick = vkick or 0


@dataclass
class Kicker(Element):
    l: float = 0
    hkick: float = 0
    vkick: float = 0
    tilt: float = 0


@dataclass
class TKicker(Element):
    l: float = 0
    hkick: float = 0
    vkick: float = 0
    tilt: float = 0


@dataclass
class RFCavity(Element):
    freq: float = None
    l: float = 0
    volt: float = 0
    lag: float = 0
    harmon: int = None
    n_bessel: int = 0
    no_cavity_totalpath: bool = False


@dataclass
class Monitor(Element):
    l: float = 0


@dataclass
class HMonitor(Monitor):
    pass


@dataclass
class VMonitor(Monitor):
    pass


@dataclass
class Instrument(Element):
    l: float = 0


@dataclass
class Placeholder(Element):
    l: float = 0


@dataclass
class Collimator(Element):
    l: float = 0


@dataclass
class ECollimator(Collimator):
    pass


@dataclass
class RCollimator(Collimator):
    pass


@dataclass
class _WithAperture:
    apertype: str = 'circle'
    aperture: Sequence[float] = (0,)
    aper_offset: Tuple[float] = (0, 0)
    aper_tol: Tuple[float] = (0, 0, 0)


elements: Dict[str, Type[Element]] = {
    k.lower(): v
    for k, v in globals().items()
    if is_dataclass(v) and not v.__name__.startswith('_')
}
elements_with_aperture: Dict[str, Type[Element]] = {
    k: type(v.__name__, (v, _WithAperture), {})
    for k, v in elements.items()
}
