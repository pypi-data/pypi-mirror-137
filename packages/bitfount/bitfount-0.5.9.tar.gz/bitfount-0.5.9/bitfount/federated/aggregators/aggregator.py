"""Vanilla model parameter aggregators for Federated Averaging."""
from __future__ import annotations

from typing import Any, Callable, List, Optional, Type, cast

from marshmallow import Schema as MarshmallowSchema
from marshmallow import fields, post_load
import numpy as np

from bitfount.federated.aggregators.base import (
    _AggregatorWorkerFactory,
    _BaseAggregatorFactory,
    _BaseModellerAggregator,
    _BaseWorkerAggregator,
)
from bitfount.federated.shim import BackendTensorShim
from bitfount.types import T_DTYPE, _SerializedWeights, _WeightDict


class _ModellerSide(_BaseModellerAggregator[T_DTYPE]):
    """Modeller-side of the vanilla aggregator."""

    def __init__(self, *, tensor_shim: BackendTensorShim, **kwargs: Any):
        super().__init__(tensor_shim=tensor_shim, **kwargs)

    def run(
        self,
        parameter_updates: List[_SerializedWeights],
        tensor_dtype: Optional[T_DTYPE] = None,
        **kwargs: Any,
    ) -> _WeightDict:
        """Averages parameters, converts to tensors and return them."""
        weight = 1 / len(parameter_updates)
        average_update = {}
        for name in parameter_updates[0]:
            average_update[name] = self._tensor_shim.to_tensor(
                np.stack(
                    [weight * np.asarray(params[name]) for params in parameter_updates],
                    axis=0,
                ).sum(axis=0),
                dtype=tensor_dtype,
            )

        return average_update


class _WorkerSide(_BaseWorkerAggregator):
    """Worker-side of the vanilla aggregator."""

    def __init__(self, *, tensor_shim: BackendTensorShim, **kwargs: Any):
        super().__init__(tensor_shim=tensor_shim, **kwargs)

    async def run(
        self, parameter_update: _WeightDict, **kwargs: Any
    ) -> _SerializedWeights:
        """Converts tensors to list of floats and returns them."""
        for name, param in parameter_update.items():
            # We are reusing parameter_update and changing it to SerializedWeights
            # which is why we ignore the assignment issue.
            parameter_update[name] = self._tensor_shim.to_list(param)  # type: ignore[assignment] # Reason: see comment # noqa: B950

        return cast(_SerializedWeights, parameter_update)


class Aggregator(_BaseAggregatorFactory, _AggregatorWorkerFactory):
    """Vanilla model parameter aggregator for Federated Averaging.

    Performs simple arithmetic mean of unencrypted model parameters.

    Args:
        tensor_shim: The tensor shim to use to perform operations on backend tensors
            of the appropriate type. The `backend_tensor_shim` method on the model
            can be called to get this shim.

    Attributes:
        name: The name of the aggregator.

    :::danger

    This aggregator is not secure. Parameter updates are shared with participants in an
    unencrypted manner. It is not recommended to use this aggregator in a zero-trust
    setting.

    :::
    """

    def __init__(self, *, tensor_shim: BackendTensorShim, **kwargs: Any):
        super().__init__(**kwargs)
        self.name = type(self).__name__
        self._tensor_shim = tensor_shim

    @staticmethod
    def get_schema(
        tensor_shim_factory: Callable[[], BackendTensorShim], **kwargs: Any
    ) -> Type[MarshmallowSchema]:
        """Returns the schema for Aggregator.

        Args:
            tensor_shim_factory: A factory function that returns a tensor shim.
        """

        class Schema(MarshmallowSchema):
            name = fields.Str()

            @post_load
            def recreate_factory(self, data: dict, **_kwargs: Any) -> Aggregator:
                return Aggregator(tensor_shim=tensor_shim_factory(), **data)

        return Schema

    def modeller(self, **kwargs: Any) -> _ModellerSide:
        """Returns the modeller side of the Aggregator."""
        return _ModellerSide(tensor_shim=self._tensor_shim, **kwargs)

    def worker(self, **kwargs: Any) -> _WorkerSide:
        """Returns the worker side of the Aggregator."""
        return _WorkerSide(tensor_shim=self._tensor_shim, **kwargs)
