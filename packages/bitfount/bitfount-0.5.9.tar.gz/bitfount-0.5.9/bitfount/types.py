"""Type hints, enums and protocols for the Bitfount libraries."""
from __future__ import annotations

from enum import Enum, auto
import os
from pathlib import Path
from typing import (
    TYPE_CHECKING,
    Any,
    Dict,
    Iterable,
    List,
    Mapping,
    NewType,
    Optional,
    Protocol,
    Sequence,
    Tuple,
    Type,
    TypeVar,
    Union,
    runtime_checkable,
)

from cryptography.hazmat.primitives.asymmetric.rsa import RSAPrivateKey
from databricks import koalas as ks
import numpy as np
import pandas as pd

if TYPE_CHECKING:
    from bitfount.data.dataloader import _BitfountDataLoader
    from bitfount.data.datasource import DataSource
    from bitfount.data.datastructure import DataStructure
    from bitfount.federated.model_reference import BitfountModelReference
    from bitfount.federated.shim import BackendTensorShim
    from bitfount.metrics import Metric
    from bitfount.models.base_models import ModelContext, _BaseModel

__all__: List[str] = ["DistributedModelProtocol"]

# Tensor dtype type variable
T_DTYPE = TypeVar("T_DTYPE", covariant=True)


# TensorLike protocol and TensorLike composite types
class _TensorLike(Protocol):
    """Protocol defining what methods and operations a Generic Tensor can perform."""

    def __mul__(self: _TensorLike, other: Any) -> _TensorLike:
        ...

    def __sub__(self: _TensorLike, other: Any) -> _TensorLike:
        ...

    def squeeze(self: _TensorLike, axis: Optional[Any] = None) -> _TensorLike:
        """Returns a tensor with all the dimensions of input of size 1 removed."""
        ...


# Weight update types
_SerializedWeights = Dict[str, Union[List[float], _TensorLike]]
_WeightDict = Dict[str, _TensorLike]
_WeightMapping = Mapping[str, _TensorLike]


# Pandas/Koalas related types
_DataFrameType = Union[pd.DataFrame, ks.DataFrame]
_SeriesType = Union[pd.Series, ks.Series]


class _PandasLikeModule(Protocol):
    """A protocol that matches the needed functions/classes from the pandas module."""

    # These are the actual classes in the module; i.e. they can be instantiated, etc.
    DataFrame: Type[_DataFrameType]
    Series: Type[_SeriesType]

    # pandas is not fully type-hinted. This signature was extracted and modified
    # from inspect.signature(pd.read_csv). It is not the full signature, but only
    # the elements we need and care about. Add more details if needed.
    def read_csv(
        self,
        filepath_or_buffer: Union[str, os.PathLike],
        *args: Any,
        **kwargs: Any,
    ) -> _DataFrameType:
        """See pandas.read_csv() for details."""  # noqa: B950, D402; wrapper around other method
        ...

    # pandas is not fully type-hinted. This signature was extracted and modified
    # from inspect.signature(pd.read_sql_table). It is not the full signature, but
    # only the elements we need and care about. Add more details if needed.
    def read_sql_table(
        self,
        table_name: str,
        con: str,
        schema: Optional[str] = None,
        index_col: Optional[Union[str, Sequence[str]]] = None,
        *args: Any,
        columns: Optional[Sequence[str]] = None,
        **kwargs: Any,
    ) -> _DataFrameType:
        """See pandas.read_sql_table() for details."""  # noqa: B950, D402; wrapper around other method
        ...

    # pandas is not fully type-hinted. This signature was extracted and modified
    # from inspect.signature(pd.to_datetime). It is not the full signature, but
    # only the elements we need and care about. Add more details if needed.
    def to_datetime(
        self,
        arg: _SeriesType,
        *args: Any,
        infer_datetime_format: bool = False,
        **kwargs: Any,
    ) -> _SeriesType:
        """See pandas.to_datetime() for details."""  # noqa: B950, D402; wrapper around other method
        ...

    # pandas is not fully type-hinted. This signature was extracted and modified
    # from inspect.signature(pd.to_datetime). It is not the full signature, but
    # only the elements we need and care about. Add more details if needed.
    def concat(
        self, objs: Iterable[_DataFrameType], axis: int = 0, *args: Any, **kwargs: Any
    ) -> _DataFrameType:
        """See pandas.concat() for details."""  # noqa: B950, D402; wrapper around other method
        ...


class _DataFrameLib(Enum):
    """An enum representing dataframe libraries."""

    PANDAS = auto()
    KOALAS = auto()


# DistributedModel protocol and types
@runtime_checkable
class DistributedModelProtocol(Protocol):
    """Federated Model structural type.

    This protocol should be implemented by classes that inherit from either
    `BitfountModel`, or both of `_BaseModel` and `DistributedModelMixIn`.
    """

    name: str
    datastructure: DataStructure
    # Type hints below indicate that one of either `epochs` or `steps` needs to be
    # supplied by the mixed-in class or other classes in the inheritance hierarchy
    epochs: Optional[int]
    steps: Optional[int]
    _total_num_batches_trained: int

    @staticmethod
    def backend_tensor_shim() -> BackendTensorShim:
        """Defined in DistributedModelMixIn."""

    def tensor_precision(self) -> T_DTYPE:
        """Defined in DistributedModelMixIn."""

    def get_param_states(self) -> _WeightDict:
        """Defined in DistributedModelMixIn."""

    def apply_weight_updates(
        self, weight_updates: Sequence[_WeightMapping]
    ) -> _WeightDict:
        """Defined in DistributedModelMixIn."""

    def update_params(self, new_model_params: _WeightMapping) -> None:
        """Defined in DistributedModelMixIn."""

    def diff_params(
        self, old_params: _WeightMapping, new_params: _WeightMapping
    ) -> _WeightDict:
        """Defined in DistributedModelMixIn."""

    def set_model_training_iterations(self, iterations: int) -> None:
        """Defined in DistributedModelMixIn."""

    def reset_trainer(self) -> None:
        """Defined in DistributedModelMixIn."""

    def fit(
        self,
        data: Optional[DataSource] = None,
        metrics: Optional[Dict[str, Metric]] = None,
        pod_identifiers: Optional[List[str]] = None,
        private_key_or_file: Optional[Union[RSAPrivateKey, Path]] = None,
        **kwargs: Any,
    ) -> Optional[Dict[str, str]]:
        """Defined in DistributedModelMixIn."""

    def log_(self, name: str, value: Any, **kwargs: Any) -> Any:
        """Defined in DistributedModelMixIn."""

    def initialise_model(
        self,
        data: Optional[DataSource] = None,
        context: Optional[ModelContext] = None,
    ) -> None:
        """Defined in _BaseModel."""

    def evaluate(
        self, test_dl: Optional[_BitfountDataLoader] = None, **kwargs: Any
    ) -> Tuple[np.ndarray, np.ndarray]:
        """Defined in _BaseModel."""

    def serialize(self, filename: Union[str, os.PathLike]) -> None:
        """Defined in _BaseModel."""

    def deserialize(self, filename: Union[str, os.PathLike]) -> None:
        """Defined in _BaseModel."""

    @classmethod
    def get_schema(cls) -> Type[_BaseModel._Schema]:
        """Defined in the pytorch models."""


if TYPE_CHECKING:
    _DistributedModelTypeOrReference = Union[
        DistributedModelProtocol, BitfountModelReference
    ]

# Serialization Types
_JSONDict = Dict[str, Any]

# s3 interaction types
_S3PresignedPOSTURL = NewType("_S3PresignedPOSTURL", str)
_S3PresignedPOSTFields = NewType("_S3PresignedPOSTFields", Mapping[str, str])
_S3PresignedURL = NewType("_S3PresignedURL", str)  # for GET requests

# SAML Types
_SAMLResponse = Mapping[str, Any]
