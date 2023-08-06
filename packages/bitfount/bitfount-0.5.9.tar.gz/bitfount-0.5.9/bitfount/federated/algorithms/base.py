"""Base classes for all algorithms.

Each module in this package defines a single algorithm.

Attributes:
    registry: A read-only dictionary of algorithm factory names to their
              implementation classes.
"""
from __future__ import annotations

from abc import ABC, abstractmethod
import inspect
from types import MappingProxyType
from typing import Any, Dict, Mapping, Optional, Type

from marshmallow import Schema as MarshmallowSchema
from marshmallow import fields

from bitfount.federated.logging import _get_federated_logger
from bitfount.federated.privacy.differential import DPPodConfig
from bitfount.federated.roles import _RolesMixIn

logger = _get_federated_logger(__name__)


class _BaseAlgorithm(ABC):
    """Blueprint for either the modeller side or the worker side of BaseAlgorithm."""

    def __init__(self, **kwargs: Any):
        super().__init__()


class _BaseModellerAlgorithm(_BaseAlgorithm, ABC):
    """Modeller side of the algorithm."""

    def __init__(self, **kwargs: Any):
        super().__init__(**kwargs)


class _BaseWorkerAlgorithm(_BaseAlgorithm, ABC):
    """Worker side of the algorithm."""

    def __init__(self, **kwargs: Any):
        super().__init__(**kwargs)

    def _apply_pod_dp(self, pod_dp: Optional[DPPodConfig]) -> None:
        """Applies pod-level Differential Privacy constraints.

        Subclasses should override this method if DP is supported.

        Args:
            pod_dp: The pod DP constraints to apply or None if no constraints.
        """
        pass


# The mutable underlying dict that holds the registry information
_registry: Dict[str, Type[_BaseAlgorithmFactory]] = {}
# The read-only version of the registry that is allowed to be imported
registry: Mapping[str, Type[_BaseAlgorithmFactory]] = MappingProxyType(_registry)


class _BaseAlgorithmSchema(ABC):
    """Mixin for normal algorithm get_schema calls."""

    @staticmethod
    @abstractmethod
    def get_schema(**kwargs: Any) -> Type[MarshmallowSchema]:
        """Get a schema for BaseAlgorithmFactory subclass."""
        raise NotImplementedError


class _BaseAlgorithmFactory(ABC, _RolesMixIn):
    """Base algorithm factory from which all other algorithms must inherit."""

    def __init__(self, **kwargs: Any):
        self.name = type(self).__name__
        super().__init__(**kwargs)

    @classmethod
    def __init_subclass__(cls, **kwargs: Any):
        if not inspect.isabstract(cls):
            logger.debug(f"Adding {cls.__name__}: {cls} to Algorithm registry")
            _registry[cls.__name__] = cls

    class _Schema(MarshmallowSchema):
        """Marshmallow schema."""

        name = fields.Str()

        @abstractmethod
        def recreate_factory(self, data: dict, **kwargs: Any) -> _BaseAlgorithmFactory:
            """Recreates protocol factory."""
            raise NotImplementedError
