from dataclasses import dataclass, fields
from typing import ClassVar, Dict, List, Literal, Tuple, Type, Union
import numpy as np

from slxpy.common.mapping import dtype_mapping

def check_shape(array_like, shape: List[int]):        
    size = np.prod(shape).item()
    array = np.array(array_like)
    if array.size != 1:
        assert array.ndim == 1, "Currently only support one dimensional vector."
        assert array.size == size, f"Size inconsistency, broadcast is currently unsupported."

format_list = lambda x: f"{{ {', '.join(str(y) for y in x)} }}"
format_list_like = lambda x: format_list(x) if isinstance(x, (list, tuple)) else f"{x}"

@dataclass
class SpaceConfig:
    type: Literal["Box", "Discrete", "MultiDiscrete", "MultiBinary"]
    
    init_name: ClassVar[str] = ""
    mapping: ClassVar[Dict[str, Type['SpaceConfig']]] = {}
    def __init_subclass__(cls):
        SpaceConfig.mapping[cls.init_name] = cls

    @staticmethod
    def reconstruct(d: dict):
        type = d["type"]
        cls = SpaceConfig.mapping[type]
        return cls.reconstruct(d)

    def asdict(self, dict_filter):
        d = {
            "type": self.type
        }
        assert len(d) == len(fields(self))  # Ensure no left-out
        return dict_filter(d)

    @staticmethod
    def unique(inits: List['SpaceConfig']):
        return list(set(type(init) for init in inits))

    @staticmethod
    def default():
        return BoxSpaceConfig("Box", 0.0, 1.0, (2, 2), np.dtype("float64"))

@dataclass
class BoxSpaceConfig(SpaceConfig):
    low: Union[List[float], float]
    high: Union[List[float], float]
    shape: Tuple[int, ...]
    dtype: np.dtype
    init_name: ClassVar[str] = "Box"

    @staticmethod
    def reconstruct(d: dict):
        return BoxSpaceConfig(
            type=d["type"],
            low=d["low"],
            high=d["high"],
            shape=tuple(d["shape"]),
            dtype=np.dtype(d["dtype"])
        )

    def asdict(self, dict_filter):
        d = {
            "type": self.type,
            "low": self.low,
            "high": self.high,
            "shape": self.shape,
            "dtype": self.dtype.name
        }
        assert len(d) == len(fields(self))  # Ensure no left-out
        return dict_filter(d)

    @property
    def initializer(self):
        return f"{format_list_like(self.low)}, {format_list_like(self.high)}, {format_list(self.shape)}"

    @property
    def cls(self):
        return f"Box<{dtype_mapping[self.dtype.name]}>"

@dataclass
class DiscreteSpaceConfig(SpaceConfig):
    n: int
    init_name: ClassVar[str] = "Discrete"
    cls: ClassVar[str] = "Discrete"

    @staticmethod
    def reconstruct(d: dict):
        return DiscreteSpaceConfig(type=d["type"], n=d["n"])

    def asdict(self, dict_filter):
        d = { "type": self.type, "n": self.n }
        assert len(d) == len(fields(self))  # Ensure no left-out
        return dict_filter(d)

    @property
    def initializer(self):
        return f"{self.n}"

@dataclass
class MultiDiscreteSpaceConfig(SpaceConfig):
    nvec: List[int]
    init_name: ClassVar[str] = "MultiDiscrete"
    cls: ClassVar[str] = "MultiDiscrete"

    @staticmethod
    def reconstruct(d: dict):
        return MultiDiscreteSpaceConfig(type=d["type"], nvec=d["nvec"])

    def asdict(self, dict_filter):
        d = { "type": self.type, "nvec": self.nvec }
        assert len(d) == len(fields(self))  # Ensure no left-out
        return dict_filter(d)

    @property
    def initializer(self):
        return format_list(self.nvec)

@dataclass
class MultiBinarySpaceConfig(SpaceConfig):
    n: int
    init_name: ClassVar[str] = "MultiBinary"
    cls: ClassVar[str] = "MultiBinary"

    @staticmethod
    def reconstruct(d: dict):
        return MultiBinarySpaceConfig(type=d["type"], n=d["n"])

    def asdict(self, dict_filter):
        d = { "type": self.type, "n": self.n }
        assert len(d) == len(fields(self))  # Ensure no left-out
        return dict_filter(d)

    @property
    def initializer(self):
        return f"{self.n}"
