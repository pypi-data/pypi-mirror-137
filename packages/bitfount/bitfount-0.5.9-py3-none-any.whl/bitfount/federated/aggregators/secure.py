"""Secure model parameter aggregators for Federated Averaging."""
from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any, Callable, Dict, List, Optional, Type, cast

from marshmallow import Schema as MarshmallowSchema
from marshmallow import fields, post_load
import numpy as np

from bitfount.federated.aggregators.aggregator import _ModellerSide as ModellerSide_
from bitfount.federated.aggregators.aggregator import _WorkerSide as WorkerSide_
from bitfount.federated.aggregators.base import _BaseAggregatorFactory
from bitfount.federated.secure import SecureShare
from bitfount.federated.shim import BackendTensorShim
from bitfount.federated.transport.worker_transport import _WorkerMailbox
from bitfount.types import T_DTYPE, _SerializedWeights, _WeightDict, _WeightMapping


class _BaseSecureAggregator:
    """Shared behaviour and attributes for SecureAggregator classes."""

    def __init__(self, *, secure_share: SecureShare, **kwargs: Any):
        self.secure_share = secure_share
        super().__init__(**kwargs)


class _ModellerSide(_BaseSecureAggregator, ModellerSide_):
    """Modeller-side of the secure aggregator."""

    def __init__(
        self,
        *,
        secure_share: SecureShare,
        tensor_shim: BackendTensorShim,
        **kwargs: Any,
    ):
        super().__init__(secure_share=secure_share, tensor_shim=tensor_shim, **kwargs)

    def run(
        self,
        parameter_updates: List[_SerializedWeights],
        tensor_dtype: Optional[T_DTYPE] = None,
        **kwargs: Any,
    ) -> _WeightDict:
        """Averages parameters, decodes and returns them."""
        new_parameter_updates: List[Dict[str, np.ndarray]] = []

        for update in parameter_updates:
            new_update: Dict[str, np.ndarray] = {}
            for name, param in update.items():
                new_update[name] = self._tensor_shim.to_numpy(param)
            new_parameter_updates.append(new_update)

        return self.secure_share.average_and_decode_state_dicts(
            new_parameter_updates, tensor_dtype
        )


class _WorkerSide(_BaseSecureAggregator, WorkerSide_):
    """Worker-side of the secure aggregator."""

    def __init__(
        self,
        *,
        secure_share: SecureShare,
        mailbox: _WorkerMailbox,
        tensor_shim: BackendTensorShim,
        **kwargs: Any,
    ):
        super().__init__(secure_share=secure_share, tensor_shim=tensor_shim, **kwargs)
        self.mailbox = mailbox

    async def run(
        self, parameter_update: _WeightMapping, **kwargs: Any
    ) -> _SerializedWeights:
        """Encodes update, converts tensors to list of floats and returns them."""
        secure_parameter_update = await self.secure_share.do_secure_aggregation(
            parameter_update, self.mailbox
        )
        # We are reusing secure_parameter_update and changing it to
        # SerializedWeights which is why we ignore the assignment issue.
        for name, param in secure_parameter_update.items():
            secure_parameter_update[name] = self._tensor_shim.to_list(param)  # type: ignore[assignment] # Reason: see comment # noqa: B950

        return cast(_SerializedWeights, secure_parameter_update)


class _InterPodAggregatorWorkerFactory(ABC):
    """Defines the worker() factory method for inter-pod aggregation."""

    @abstractmethod
    def worker(self, mailbox: _WorkerMailbox, **kwargs: Any) -> _WorkerSide:
        """Returns worker side of the SecureAggregator."""
        pass


class SecureAggregator(_BaseAggregatorFactory, _InterPodAggregatorWorkerFactory):
    """Secure aggregation of encrypted model parameters.

    This aggregator is used to aggregate model parameter updates from multiple workers
    without revealing the individual updates to any worker or the modeller. This is
    known as Secure Multi-Party Computation (SMPC).

    Args:
        secure_share: The `SecureShare` object used to encrypt and decrypt model
            parameters and communicate with the other workers.
        tensor_shim: The tensor shim to use to perform operations on backend tensors
            of the appropriate type. The `backend_tensor_shim` method on the model
            can be called to get this shim.

    Attributes:
        name: The name of the aggregator.
    """

    def __init__(
        self,
        *,
        secure_share: SecureShare,
        tensor_shim: BackendTensorShim,
        **kwargs: Any,
    ):
        super().__init__(**kwargs)
        self.name = type(self).__name__
        self._tensor_shim = tensor_shim
        self._secure_share = secure_share

    @staticmethod
    def get_schema(
        tensor_shim_factory: Callable[[], BackendTensorShim],
        **kwargs: Any,
    ) -> Type[MarshmallowSchema]:
        """Returns the schema for SecureAggregator.

        Args:
            tensor_shim_factory: A factory function that returns a tensor shim.
        """
        secure_share_schema = SecureShare.get_schema(
            tensor_shim_factory=tensor_shim_factory,
        )

        class Schema(MarshmallowSchema):
            name = fields.Str()
            _secure_share = fields.Nested(secure_share_schema)

            @post_load
            def recreate_factory(self, data: dict, **_kwargs: Any) -> SecureAggregator:
                secure_share = data.pop("_secure_share")
                return SecureAggregator(
                    tensor_shim=tensor_shim_factory(), secure_share=secure_share, **data
                )

        return Schema

    def modeller(self, **kwargs: Any) -> _ModellerSide:
        """Returns the modeller side of the SecureAggregator."""
        return _ModellerSide(
            tensor_shim=self._tensor_shim, secure_share=self._secure_share, **kwargs
        )

    def worker(self, mailbox: _WorkerMailbox, **kwargs: Any) -> _WorkerSide:
        """Returns the worker side of the SecureAggregator.

        Args:
            mailbox: The mailbox to use for receiving messages.
        """
        return _WorkerSide(
            tensor_shim=self._tensor_shim,
            secure_share=self._secure_share,
            mailbox=mailbox,
            **kwargs,
        )
