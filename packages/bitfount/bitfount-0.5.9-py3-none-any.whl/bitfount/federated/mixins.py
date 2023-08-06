"""MixIn classes for compatible models with the federated algorithms."""
from __future__ import annotations

from abc import ABC, abstractmethod
import os
from pathlib import Path
from typing import (
    TYPE_CHECKING,
    Any,
    Dict,
    List,
    Mapping,
    MutableMapping,
    Optional,
    Sequence,
    Union,
    cast,
)

from cryptography.hazmat.primitives.asymmetric.rsa import RSAPrivateKey

from bitfount.data.datasource import DataSource
from bitfount.federated.aggregators.base import _BaseAggregatorFactory
from bitfount.federated.algorithms.model_algorithms.federated_training import (
    FederatedModelTraining,
)
from bitfount.federated.authorisation_checkers import IdentityVerificationMethod
from bitfount.federated.helper import (
    _create_aggregator,
    _create_federated_averaging_protocol_factory,
    _create_message_service,
)
from bitfount.federated.modeller import Modeller
from bitfount.federated.protocols.fed_avg import FederatedAveraging
from bitfount.federated.transport.message_service import _MessageService
from bitfount.hub.api import _PRODUCTION_IDP_URL
from bitfount.hub.helper import _create_bitfounthub
from bitfount.types import DistributedModelProtocol

if TYPE_CHECKING:
    from bitfount.federated.shim import BackendTensorShim
    from bitfount.federated.transport.config import MessageServiceConfig
    from bitfount.hub.api import BitfountHub
    from bitfount.metrics import Metric
    from bitfount.types import (
        T_DTYPE,
        _WeightDict,
        _WeightMapping,
    )

from bitfount.federated.logging import _get_federated_logger

logger = _get_federated_logger(__name__)


class _DistributedModelMixIn(ABC):
    """A mixin for models used in federated mechanisms.

    An abstract base mixin for models that are compatible with the following
    distributed learning protocols:
        - FederatedAveraging
    """

    @abstractmethod
    def get_param_states(self) -> _WeightDict:
        """Gets the current states of the trainable parameters of the model.

        Returns:
            A dict of param names to tensors
        """
        raise NotImplementedError

    @abstractmethod
    def apply_weight_updates(
        self, weight_updates: Sequence[_WeightMapping]
    ) -> _WeightDict:
        """Applies weight updates to the weights of this model.

        Apply a sequence of parameter weight updates (mappings of parameter name
        to a tensor describing the weight update) to the parameters of this model.
        Used by Modeller to apply updates received from Workers.

        Args:
            weight_updates (Sequence[WeightMapping]): The sequence
                of weight updates

        Returns:
            The updated parameters as a dict of name to tensor.
        """
        raise NotImplementedError

    @abstractmethod
    def update_params(self, new_model_params: _WeightMapping) -> None:
        """Updates the current model parameters to the ones provided.

        Used by Worker to update new parameters received from Modeller.

        Args:
            new_model_params (WeightMapping)): The new model parameters
                to update to as a mapping of parameter names to tensors.
        """
        raise NotImplementedError

    @abstractmethod
    def diff_params(
        self, old_params: _WeightMapping, new_params: _WeightMapping
    ) -> _WeightDict:
        """Calculates the difference between two sets of model parameters."""
        raise NotImplementedError

    @abstractmethod
    def set_model_training_iterations(self, iterations: int) -> None:
        """Sets model steps or epochs to the appropriate number between updates."""
        raise NotImplementedError

    @abstractmethod
    def reset_trainer(self) -> None:
        """Resets the trainer to its initial state.

        :::note

        Importantly, calling this method in between `fit` calls allows the caller to
        repeatedly refit the model continuing from the batch after the one that was last
        fit. This only applies to step-wise training.

        :::
        """
        raise NotImplementedError

    @abstractmethod
    def log_(self, name: str, value: Any, **kwargs: Any) -> Any:
        """Logs a metric with a particular value to the user's configured model loggers.

        Args:
            name: The name of the metric to log
            value: The value of the metric to log
            **kwargs: Additional keyword arguments to pass to the logger
        """
        raise NotImplementedError

    @staticmethod
    @abstractmethod
    def backend_tensor_shim() -> BackendTensorShim:
        """Gets a backend shim that can be used for tensor conversion."""
        raise NotImplementedError

    @abstractmethod
    def tensor_precision(self) -> T_DTYPE:
        """Gets the floating point precision used by model tensors.

        Typically this will be 32 bits.
        """
        raise NotImplementedError

    @abstractmethod
    def _fit_local(
        self,
        data: DataSource,
        metrics: Optional[MutableMapping[str, Metric]] = None,
        **kwargs: Any,
    ) -> Dict[str, str]:
        """Fits model locally using data from `datasource`.

        Should be implemented in the final model class that subclasses
        DistributedModelMixIn.
        """
        raise NotImplementedError

    def _fit_federated(
        self,
        pod_identifiers: List[str],
        username: Optional[str] = None,
        aggregator: Optional[_BaseAggregatorFactory] = None,
        steps_between_parameter_updates: Optional[int] = None,
        epochs_between_parameter_updates: Optional[int] = None,
        bitfounthub: Optional[BitfountHub] = None,
        ms_config: Optional[MessageServiceConfig] = None,
        message_service: Optional[_MessageService] = None,
        pod_public_key_paths: Optional[Mapping[str, Path]] = None,
        pretrained_file: Optional[Union[str, os.PathLike]] = None,
        secure_aggregation: bool = False,
        auto_eval: bool = True,
        identity_verification_method: IdentityVerificationMethod = IdentityVerificationMethod.DEFAULT,  # noqa: B950
        private_key_or_file: Optional[Union[RSAPrivateKey, Path]] = None,
        idp_url: str = _PRODUCTION_IDP_URL,
    ) -> Optional[Dict[str, str]]:
        """Fits model federated-ly."""
        algorithm = FederatedModelTraining(model=cast(DistributedModelProtocol, self))

        if not bitfounthub:
            bitfounthub = _create_bitfounthub(username=username)

        if not message_service:
            message_service = _create_message_service(bitfounthub.session, ms_config)

        if not aggregator:
            aggregator = _create_aggregator(
                model=algorithm.model, secure_aggregation=secure_aggregation
            )
        # TODO: [BIT-1098] Manage pods with different schemas
        protocol = _create_federated_averaging_protocol_factory(
            protocol_cls=FederatedAveraging,
            algorithm=algorithm,
            aggregator=aggregator,
            steps_between_parameter_updates=steps_between_parameter_updates,
            epochs_between_parameter_updates=epochs_between_parameter_updates,
            auto_eval=auto_eval,
        )

        modeller = Modeller(
            protocol=protocol,
            message_service=message_service,
            bitfounthub=bitfounthub,
            pod_public_key_paths=pod_public_key_paths,
            pretrained_file=pretrained_file,
            identity_verification_method=identity_verification_method,
            private_key=private_key_or_file,
            idp_url=idp_url,
        )

        # Start task running
        result = modeller.run(pod_identifiers)
        if result is False:
            return None
        else:
            return result

    def fit(
        self,
        data: Optional[DataSource] = None,
        metrics: Optional[Dict[str, Metric]] = None,
        pod_identifiers: Optional[List[str]] = None,
        private_key_or_file: Optional[Union[RSAPrivateKey, Path]] = None,
        **kwargs: Any,
    ) -> Optional[Dict[str, str]]:
        """Fits model either locally or federated-ly.

        `pod_identifiers` and `private_key` must both be provided for federated
        training.

        Args:
            data: (Optional[DataSource])): datasource for training. Defaults to None.
            metrics (Optional[Dict[str, Metric]], optional): metrics to calculate for
                evaluation. Defaults to None.
            pod_identifiers (Optional[List[str]], optional): list of pod identifiers.
                Defaults to None.
            private_key_or_file (Optional[Union[RSAPrivateKey, Path]], optional): either
                private key or path to private key file. Defaults to None.
            kwargs (Any): passed to self._fit_federated

        """
        if pod_identifiers is not None:
            logger.info(f"Training federated with pods: {', '.join(pod_identifiers)}.")
            return self._fit_federated(
                pod_identifiers=pod_identifiers,
                private_key_or_file=private_key_or_file,
                **kwargs,
            )
        elif data is not None:
            logger.info("Training locally using `self.datasource`.")
            return self._fit_local(data=data, metrics=metrics)
        else:
            raise (
                ValueError(
                    "Please provide either pod identifiers "
                    "or a datasource for model training."
                )
            )
