from __future__ import annotations

from contextlib import nullcontext
import os
from typing import Callable, ClassVar, ContextManager, Generic, List, Sequence, Tuple, Type, TypeVar, Union
from typing_extensions import Protocol, TypeAlias

import numpy as np
import torch


__all__ = ['Backend', 'PyTorch', 'Numpy', 'F']


def __getattr__(name):
    if name == 'F':
        return backend.functions
    else:
        try:
            return globals()[name]
        except KeyError:
            raise AttributeError(f'module {__name__!r} has no attribute {name!r}')


FloatArray: TypeAlias = Sequence[
    Union[
        float,
        Sequence[
            Union[
                float,
                Sequence[float],
            ]
        ],
    ]
]
IntOrTuple: TypeAlias = Union[int, Tuple[int, ...]]
T = TypeVar('T')
ListOrTuple: TypeAlias = Union[List[T], Tuple[T, ...]]

_TensorType = TypeVar('_TensorType', np.ndarray, torch.Tensor)
_ParameterType = TypeVar('_ParameterType', np.ndarray, torch.nn.Parameter)


class ModuleType(Protocol):
    def __call__(self, x: _TensorType) -> _TensorType: ...
    def forward(self, x: _TensorType) -> _TensorType: ...


class ModuleProxy:
    """Proxy for torch.nn.Module."""

    def __init__(self):
        self._children = {}
        self._modules = ()

    def __call__(self, x: _TensorType, **kwargs) -> _TensorType:
        return self.forward(x, **kwargs)

    def __setattr__(self, key, value):
        super().__setattr__(key, value)
        if isinstance(value, ModuleProxy):
            self._children[key] = value

    def children(self):
        return iter(self._children.values())

    # noinspection PyMethodMayBeStatic,PyUnusedLocal
    def forward(self, x: _TensorType, **kwargs) -> _TensorType:
        return x

    # noinspection PyMethodMayBeStatic
    def parameters(self):
        return iter([])


class _Functions(Generic[_TensorType]):
    @staticmethod
    def abs(x: _TensorType) -> _TensorType:
        raise NotImplementedError

    @staticmethod
    def all(x: _TensorType, *, dim: int = None) -> Union[_TensorType, bool]:
        raise NotImplementedError

    @staticmethod
    def any(x: _TensorType, *, dim: int = None) -> Union[_TensorType, bool]:
        raise NotImplementedError

    @staticmethod
    def arctan2(x: _TensorType, y: _TensorType) -> _TensorType:
        raise NotImplementedError

    @staticmethod
    def cos(x: _TensorType) -> _TensorType:
        raise NotImplementedError

    @staticmethod
    def cosh(x: _TensorType) -> _TensorType:
        raise NotImplementedError

    @staticmethod
    def einsum(pattern: str, *xs: _TensorType) -> _TensorType:
        raise NotImplementedError

    @staticmethod
    def isfinite(x: _TensorType) -> _TensorType:
        raise NotImplementedError

    @staticmethod
    def isnan(x: _TensorType) -> _TensorType:
        raise NotImplementedError

    @staticmethod
    def relu(x: _TensorType) -> _TensorType:
        raise NotImplementedError

    @staticmethod
    def sin(x: _TensorType) -> _TensorType:
        raise NotImplementedError

    @staticmethod
    def sinh(x: _TensorType) -> _TensorType:
        raise NotImplementedError

    @staticmethod
    def sqrt(x: _TensorType) -> _TensorType:
        raise NotImplementedError

    @staticmethod
    def sum(x: _TensorType, *, dim: IntOrTuple = None) -> _TensorType:
        raise NotImplementedError

    @staticmethod
    def tan(x: _TensorType) -> _TensorType:
        raise NotImplementedError

    @staticmethod
    def tanh(x: _TensorType) -> _TensorType:
        raise NotImplementedError


class _Linalg(Generic[_TensorType]):
    @staticmethod
    def det(matrix: _TensorType) -> _TensorType:
        raise NotImplementedError

    @staticmethod
    def invert(matrix: _TensorType) -> _TensorType:
        raise NotImplementedError

    @staticmethod
    def solve(matrix: _TensorType, vector: _TensorType) -> _TensorType:
        raise NotImplementedError

    @staticmethod
    def trace(matrix: _TensorType) -> _TensorType:
        raise NotImplementedError


class _Random(Generic[_TensorType]):
    def normal(self, *, mean: float, std: float, size: IntOrTuple) -> _TensorType:
        raise NotImplementedError


class Backend(Generic[_TensorType, _ParameterType]):
    TensorType: ClassVar[Type]
    ParameterType: ClassVar[Type]
    ModuleType: ClassVar[Type]
    functions: _Functions[_TensorType]
    linalg: _Linalg[_TensorType]
    random: _Random[_TensorType]
    ignore_gradient: Callable[[], ContextManager]

    def as_float64(self, x: _TensorType) -> _TensorType:
        """Convert the given tensor's data representation to float64."""
        raise NotImplementedError

    def as_parameter(self, x: _TensorType) -> _ParameterType:
        """Transform the given tensor to a parameter."""
        raise NotImplementedError

    def concatenate(self, xs: ListOrTuple[_TensorType], *, dim: int = 0) -> _TensorType:
        """Concatenate multiple tensors along one of their dimensions."""
        raise NotImplementedError

    def from_numbers(self, value: Union[float, FloatArray]) -> _TensorType:
        """Create a new tensor from the given number(s)."""
        raise NotImplementedError

    def from_numpy(self, array: np.ndarray) -> _TensorType:
        """Create a new tensor from the given numpy array."""
        raise NotImplementedError

    def make_id_matrix(self, n: int) -> _TensorType:
        """Create a new tensor representing the nxn identity matrix."""
        raise NotImplementedError

    def make_zeros(self, *shape: int) -> _TensorType:
        """Create a new tensor of the given shape, filled with zeros."""
        raise NotImplementedError

    def requires_grad(self, x: _TensorType) -> bool:
        """Check whether the given tensor requires gradient tracking."""
        raise NotImplementedError

    def stack(self, xs: ListOrTuple[_TensorType], *, dim: int = 0) -> _TensorType:
        """Stack multiple tensors along a new dimension."""
        raise NotImplementedError

    def to_number(self, x: _TensorType) -> float:
        """Convert the given 0-dim tensor to a float object."""
        raise NotImplementedError

    def to_numpy(self, x: _TensorType) -> np.ndarray:
        """Convert the given tensor to a numpy array."""
        raise NotImplementedError

    def transpose(self, x: _TensorType) -> _TensorType:
        """Transpose the given tensor by swapping the (0,1) dimensions."""
        raise NotImplementedError

    def update_tensor_data(self, x: _TensorType, new_value: _TensorType) -> None:
        """Update the underlying tensor data while ignoring any gradient tracking."""
        raise NotImplementedError

    def zeros_like(self, x: _TensorType) -> _TensorType:
        """Create a new tensor of same shape as the given tensor, filled will zeros."""
        raise NotImplementedError


class _PyTorchFunctions(_Functions[torch.Tensor]):
    @staticmethod
    def abs(x: torch.Tensor) -> torch.Tensor:
        return torch.abs(x)

    @staticmethod
    def all(x: torch.Tensor, *, dim: int = None) -> Union[torch.Tensor, bool]:
        if dim is not None:
            return torch.all(x, dim=dim)
        else:
            return torch.all(x)

    @staticmethod
    def any(x: torch.Tensor, *, dim: int = None) -> Union[torch.Tensor, bool]:
        if dim is not None:
            return torch.any(x, dim=dim)
        else:
            return torch.any(x)

    @staticmethod
    def arctan2(x: torch.Tensor, y: torch.Tensor) -> torch.Tensor:
        return torch.atan2(x, y)

    @staticmethod
    def cos(x: torch.Tensor) -> torch.Tensor:
        return torch.cos(x)

    @staticmethod
    def cosh(x: torch.Tensor) -> torch.Tensor:
        return torch.cosh(x)

    @staticmethod
    def einsum(pattern: str, *xs: torch.Tensor) -> torch.Tensor:
        return torch.einsum(pattern, *xs)

    @staticmethod
    def isfinite(x: torch.Tensor) -> torch.Tensor:
        return torch.isfinite(x)

    @staticmethod
    def isnan(x: torch.Tensor) -> torch.Tensor:
        return torch.isnan(x)

    @staticmethod
    def relu(x: torch.Tensor) -> torch.Tensor:
        return torch.nn.functional.relu(x)

    @staticmethod
    def sin(x: torch.Tensor) -> torch.Tensor:
        return torch.sin(x)

    @staticmethod
    def sinh(x: torch.Tensor) -> torch.Tensor:
        return torch.sinh(x)

    @staticmethod
    def sqrt(x: torch.Tensor) -> torch.Tensor:
        return torch.sqrt(x)

    @staticmethod
    def sum(x: torch.Tensor, *, dim: IntOrTuple = None) -> torch.Tensor:
        if dim is not None:
            return torch.sum(x, dim=dim)
        else:
            return torch.sum(x)

    @staticmethod
    def tan(x: torch.Tensor) -> torch.Tensor:
        return torch.tan(x)

    @staticmethod
    def tanh(x: torch.Tensor) -> torch.Tensor:
        return torch.tanh(x)


class _PyTorchLinalg(_Linalg[torch.Tensor]):
    @staticmethod
    def det(matrix: torch.Tensor) -> torch.Tensor:
        return torch.linalg.det(matrix)

    @staticmethod
    def invert(matrix: torch.Tensor) -> torch.Tensor:
        return torch.linalg.inv(matrix)

    @staticmethod
    def solve(matrix: torch.Tensor, vector: torch.Tensor) -> torch.Tensor:
        return torch.linalg.solve(matrix, vector)
    
    @staticmethod
    def trace(matrix: torch.Tensor) -> torch.Tensor:
        return torch.trace(matrix)


class _PyTorchRandom(_Random[torch.Tensor]):
    def normal(self, *, mean: float, std: float, size: IntOrTuple) -> torch.Tensor:
        if isinstance(size, int):
            size = (size,)
        return torch.normal(mean=mean, std=std, size=size)


class PyTorch(Backend[torch.Tensor, torch.nn.Parameter]):
    TensorType = torch.Tensor
    ParameterType = torch.nn.Parameter
    ModuleType = torch.nn.Module

    def __init__(self):
        torch.set_default_dtype(torch.float64)
        self.functions = _PyTorchFunctions()
        self.linalg = _PyTorchLinalg()
        self.random = _PyTorchRandom()
        self.ignore_gradient = torch.no_grad

    def as_float64(self, x: torch.Tensor) -> torch.Tensor:
        return x.to(torch.float64)

    def as_parameter(self, x: torch.Tensor) -> torch.nn.Parameter:
        return torch.nn.Parameter(x)

    def concatenate(self, xs: ListOrTuple[torch.Tensor], *, dim: int = 0) -> torch.Tensor:
        return torch.cat(xs, dim=dim)

    def from_numbers(self, value: Union[float, FloatArray]) -> torch.Tensor:
        return torch.tensor(value, dtype=torch.float64)

    def from_numpy(self, array: np.ndarray) -> torch.Tensor:
        return torch.from_numpy(array)

    def make_id_matrix(self, n: int) -> torch.Tensor:
        return torch.eye(n)

    def make_zeros(self, *shape: int) -> torch.Tensor:
        return torch.zeros(*shape)

    def requires_grad(self, x: torch.Tensor) -> bool:
        return x.requires_grad

    def stack(self, xs: ListOrTuple[torch.Tensor], *, dim: int = 0) -> torch.Tensor:
        return torch.stack(xs, dim=dim)

    def to_number(self, x: torch.Tensor) -> float:
        if x.requires_grad:
            x = x.detach()
        return x.item()

    def to_numpy(self, x: torch.Tensor) -> np.ndarray:
        if x.requires_grad:
            x = x.detach()
        return x.numpy()

    def transpose(self, x: torch.Tensor) -> torch.Tensor:
        return torch.t(x)

    def update_tensor_data(self, x: torch.Tensor, new_value: torch.Tensor) -> None:
        with self.ignore_gradient():
            x.data = new_value

    def zeros_like(self, x: torch.Tensor) -> torch.Tensor:
        return torch.zeros_like(x)


class _NumpyFunctions(_Functions[np.ndarray]):
    @staticmethod
    def abs(x: np.ndarray) -> np.ndarray:
        return np.abs(x)

    @staticmethod
    def all(x: np.ndarray, *, dim: int = None) -> Union[np.ndarray, bool]:
        return np.all(x, axis=dim)  # type: ignore

    @staticmethod
    def any(x: np.ndarray, *, dim: int = None) -> Union[np.ndarray, bool]:
        return np.any(x, axis=dim)  # type: ignore

    @staticmethod
    def arctan2(x: np.ndarray, y: np.ndarray) -> np.ndarray:
        return np.arctan2(x, y)

    @staticmethod
    def cos(x: np.ndarray) -> np.ndarray:
        return np.cos(x)

    @staticmethod
    def cosh(x: np.ndarray) -> np.ndarray:
        return np.cosh(x)

    @staticmethod
    def einsum(pattern: str, *xs: np.ndarray) -> np.ndarray:
        return np.einsum(pattern, *xs)

    @staticmethod
    def isfinite(x: np.ndarray) -> np.ndarray:
        return np.isfinite(x)

    @staticmethod
    def isnan(x: np.ndarray) -> np.ndarray:
        return np.isnan(x)

    @staticmethod
    def relu(x: np.ndarray) -> np.ndarray:
        return np.maximum(x, 0)

    @staticmethod
    def sin(x: np.ndarray) -> np.ndarray:
        return np.sin(x)

    @staticmethod
    def sinh(x: np.ndarray) -> np.ndarray:
        return np.sinh(x)

    @staticmethod
    def sqrt(x: np.ndarray) -> np.ndarray:
        return np.sqrt(x)

    @staticmethod
    def sum(x: np.ndarray, *, dim: IntOrTuple = None) -> np.ndarray:
        if dim is not None:
            return np.sum(x, axis=dim)
        else:
            return np.sum(x)

    @staticmethod
    def tan(x: np.ndarray) -> np.ndarray:
        return np.tan(x)

    @staticmethod
    def tanh(x: np.ndarray) -> np.ndarray:
        return np.tanh(x)


class _NumpyLinalg(_Linalg[np.ndarray]):
    @staticmethod
    def det(matrix: np.ndarray) -> np.ndarray:
        return np.linalg.det(matrix)

    @staticmethod
    def invert(matrix: np.ndarray) -> np.ndarray:
        return np.linalg.inv(matrix)

    @staticmethod
    def solve(matrix: np.ndarray, vector: np.ndarray) -> np.ndarray:
        return np.linalg.solve(matrix, vector)

    @staticmethod
    def trace(matrix: np.ndarray) -> np.ndarray:
        return np.trace(matrix)


class _NumpyRandom(_Random[np.ndarray]):
    def __init__(self):
        self._rng = np.random.default_rng()

    def normal(self, *, mean: float, std: float, size: IntOrTuple) -> np.ndarray:
        return self._rng.normal(loc=mean, scale=std, size=size)


class Numpy(Backend[np.ndarray, np.ndarray]):
    TensorType = np.ndarray
    ParameterType = np.ndarray
    ModuleType = ModuleProxy

    def __init__(self):
        np.seterr(invalid='raise')
        self.functions = _NumpyFunctions()
        self.linalg = _NumpyLinalg()
        self.random = _NumpyRandom()
        self.ignore_gradient = nullcontext

    def as_float64(self, x: np.ndarray) -> np.ndarray:
        return x.astype(np.float64)

    def as_parameter(self, x: np.ndarray) -> np.ndarray:
        return x

    def concatenate(self, xs: ListOrTuple[np.ndarray], *, dim: int = 0) -> np.ndarray:
        return np.concatenate(xs, axis=dim)

    def from_numbers(self, value: Union[float, FloatArray]) -> np.ndarray:
        return np.array(value, dtype=np.float64)

    def from_numpy(self, array: np.ndarray) -> np.ndarray:
        return array.copy()

    def make_id_matrix(self, n: int) -> np.ndarray:
        return np.eye(n)

    def make_zeros(self, *shape: int) -> np.ndarray:
        return np.zeros(shape)

    def requires_grad(self, x: np.ndarray) -> bool:
        return False

    def stack(self, xs: ListOrTuple[np.ndarray], *, dim: int = 0) -> np.ndarray:
        return np.stack(xs, axis=dim)

    def to_number(self, x: np.ndarray) -> float:
        return x.item()

    def to_numpy(self, x: np.ndarray) -> np.ndarray:
        return x

    def transpose(self, x: np.ndarray) -> np.ndarray:
        return np.transpose(x)

    def update_tensor_data(self, x: np.ndarray, new_value: np.ndarray) -> None:
        x[...] = new_value

    def zeros_like(self, x: np.ndarray) -> np.ndarray:
        return np.zeros_like(x)


backend: Backend
_spec = os.environ.get('DIPAS_BACKEND')
if _spec is None or _spec.lower() in ('pytorch', 'torch'):
    backend = PyTorch()
elif _spec.lower() == 'numpy':
    backend = Numpy()
else:
    raise RuntimeError(f'Unknown backend: {_spec}')
del _spec
