"""Federated Averaging protocol."""
from __future__ import annotations

import asyncio
import os
from pathlib import Path
import time
from typing import (
    TYPE_CHECKING,
    Any,
    Dict,
    Iterable,
    List,
    Mapping,
    Optional,
    Protocol,
    Tuple,
    Type,
    Union,
    cast,
    runtime_checkable,
)

from cryptography.hazmat.primitives.asymmetric.rsa import RSAPrivateKey
from marshmallow import Schema as MarshmallowSchema
from marshmallow import fields, post_load

from bitfount.data.datasource import DataSource
from bitfount.federated.aggregators.base import (
    _AggregatorWorkerFactory,
    _BaseAggregator,
    _BaseAggregatorFactory,
    _BaseModellerAggregator,
    _BaseWorkerAggregator,
)
from bitfount.federated.aggregators.secure import _InterPodAggregatorWorkerFactory
from bitfount.federated.algorithms.model_algorithms.federated_training import (
    FederatedModelTraining,
)
from bitfount.federated.authorisation_checkers import (
    IdentityVerificationMethod,
    check_identity_verification_method,
)
from bitfount.federated.early_stopping import FederatedEarlyStopping
from bitfount.federated.helper import (
    _create_aggregator,
    _create_federated_averaging_protocol_factory,
    _create_message_service,
)
from bitfount.federated.logging import _get_federated_logger
from bitfount.federated.pod_vitals import _PodVitals
from bitfount.federated.privacy.differential import DPPodConfig
from bitfount.federated.protocols.base import (
    _BaseCompatibleAlgoFactory,
    _BaseModellerProtocol,
    _BaseProtocolFactory,
    _BaseWorkerProtocol,
    _ProtocolAggregatorSchema,
    _run_protocol,
)
from bitfount.federated.transport.config import MessageServiceConfig
from bitfount.federated.transport.message_service import _MessageService
from bitfount.federated.transport.modeller_transport import (
    _get_parameter_updates_from_workers,
    _get_training_metrics_from_workers,
    _ModellerMailbox,
    _send_model_parameters,
)
from bitfount.federated.transport.worker_transport import (
    _get_model_parameters,
    _send_parameter_update,
    _send_training_metrics,
    _WorkerMailbox,
)
from bitfount.hub.api import _PRODUCTION_IDP_URL, BitfountHub
from bitfount.hub.helper import _create_bitfounthub
from bitfount.types import T_DTYPE, _JSONDict, _SerializedWeights, _WeightDict

if TYPE_CHECKING:
    from bitfount.types import _DistributedModelTypeOrReference

logger = _get_federated_logger(__name__)


@runtime_checkable
class _FederatedAveragingCompatibleAlgo(Protocol[T_DTYPE]):
    @property
    def epochs(self) -> Optional[int]:
        ...

    @property
    def steps(self) -> Optional[int]:
        ...

    @property
    def tensor_precision(self) -> T_DTYPE:
        ...


@runtime_checkable
class _FederatedAveragingCompatibleWorker(_FederatedAveragingCompatibleAlgo, Protocol):
    """Defines worker-side algorithm compatibility."""

    def initialise(
        self,
        datasource: DataSource,
        pod_dp: Optional[DPPodConfig] = None,
        **kwargs: Any,
    ) -> None:
        """Initialise the worker-side algorithm."""
        ...

    def run(
        self,
        data: DataSource,
        model_params: _SerializedWeights,
        iterations: int,
    ) -> Tuple[_WeightDict, Optional[Dict[str, str]]]:
        """Run the worker-side algorithm."""
        ...

    def save_final_parameters(self, model_params: _SerializedWeights) -> None:
        """Save the weights from the worker-side algorithm."""
        ...


@runtime_checkable
class _FederatedAveragingCompatibleModeller(
    _FederatedAveragingCompatibleAlgo, Protocol
):
    """Defines modeller-side algorithm compatibility."""

    def initialise(
        self,
        pretrained_file: Optional[Union[str, os.PathLike]] = None,
        **kwargs: Any,
    ) -> None:
        """Initialise the modeller-side algorithm."""
        ...

    def run(
        self,
        update: Optional[_WeightDict] = None,
        validation_metrics: Optional[Mapping[str, float]] = None,
    ) -> _SerializedWeights:
        """Run the modeller-side algorithm."""
        ...


@runtime_checkable
class _FederatedAveragingCompatibleAlgoFactory(_BaseCompatibleAlgoFactory, Protocol):
    """Defines algorithm factory compatibility."""

    model: _DistributedModelTypeOrReference

    @property
    def model_schema(self) -> Type[MarshmallowSchema]:
        """Returns the schema of the underlying model."""
        ...

    def modeller(self, **kwargs: Any) -> _FederatedAveragingCompatibleModeller:
        """Returns a modeller-side algorithm."""
        ...

    def worker(
        self, hub: BitfountHub, **kwargs: Any
    ) -> _FederatedAveragingCompatibleWorker:
        """Returns a worker-side algorithm."""
        ...

    @staticmethod
    def get_schema(
        model_schema: Type[MarshmallowSchema], **kwargs: Any
    ) -> Type[MarshmallowSchema]:
        """Returns the schema for this algorithm."""
        ...


class _BaseFederatedAveragingMixIn:
    """Shared behaviour for the `FederatedAveraging` classes."""

    # This is set in the base protocol
    algorithm: _FederatedAveragingCompatibleAlgo

    def __init__(
        self,
        *,
        aggregator: _BaseAggregator,
        steps_between_parameter_updates: Optional[int] = None,
        epochs_between_parameter_updates: Optional[int] = None,
        **_kwargs: Any,
    ):
        self.aggregator = aggregator
        self.steps_between_parameter_updates = steps_between_parameter_updates
        self.epochs_between_parameter_updates = epochs_between_parameter_updates

    def perform_iterations_checks(self) -> None:
        """Perform checks on iterations to ensure training configuration is correct.

        Raises:
            ValueError: if there is a mismatch between model iterations and
                algorithm iterations.
        """
        if bool(self.steps_between_parameter_updates) == bool(
            self.epochs_between_parameter_updates
        ):
            raise ValueError("You must specify one (and only one) of steps or epochs.")
        if not (
            bool(self.steps_between_parameter_updates) == bool(self.algorithm.steps)
        ):
            raise ValueError(
                "Parameter update method must match model training method"
                + " i.e. steps or epochs."
            )
        if (
            # If steps_between_parameter_updates then algorithm.steps is not None
            self.steps_between_parameter_updates
            and self.steps_between_parameter_updates > self.algorithm.steps  # type: ignore[operator] # Reason: see comment # noqa: B950
        ) or (
            # If epochs_between_parameter_updates then algorithm.epochs is not None
            self.epochs_between_parameter_updates
            and self.epochs_between_parameter_updates > self.algorithm.epochs  # type: ignore[operator] # Reason: see comment # noqa: B950
        ):
            raise ValueError(
                "Number of iterations between sharing updates must not be "
                "greater than total number of model iterations."
            )

    def get_num_federated_iterations(self) -> int:
        """Returns number of rounds of federated training to be done.

        This is rounded down to the nearest whole number.
        """
        num_iterations_between_updates = cast(
            int,
            self.epochs_between_parameter_updates
            or self.steps_between_parameter_updates,
        )
        num_iterations = cast(int, self.algorithm.epochs or self.algorithm.steps)

        # floor division rounds the result down to the nearest whole number
        return num_iterations // num_iterations_between_updates


class _ModellerSide(_BaseModellerProtocol, _BaseFederatedAveragingMixIn):
    """Modeller side of the FederatedAveraging protocol."""

    aggregator: _BaseModellerAggregator
    algorithm: _FederatedAveragingCompatibleModeller

    def __init__(
        self,
        *,
        algorithm: _FederatedAveragingCompatibleModeller,
        mailbox: _ModellerMailbox,
        aggregator: _BaseModellerAggregator,
        steps_between_parameter_updates: Optional[int],
        epochs_between_parameter_updates: Optional[int],
        early_stopping: Optional[FederatedEarlyStopping],
        auto_eval: bool = True,
        **kwargs: Any,
    ):
        super().__init__(
            algorithm=algorithm,
            mailbox=mailbox,
            aggregator=aggregator,
            steps_between_parameter_updates=steps_between_parameter_updates,
            epochs_between_parameter_updates=epochs_between_parameter_updates,
            **kwargs,
        )

        self.early_stopping = early_stopping
        self.auto_eval = auto_eval
        self.validation_results: List[Dict[str, float]] = []

    async def _send_parameters(self, new_parameters: _SerializedWeights) -> None:
        """Sends central model parameters to workers."""
        logger.debug("Sending global parameters to workers")
        await _send_model_parameters(new_parameters, self.mailbox)

    async def _receive_parameter_updates(
        self,
    ) -> List[_SerializedWeights]:
        """Receives parameter updates from every worker."""
        return await _get_parameter_updates_from_workers(self.mailbox)

    async def _get_training_metrics_updates(
        self,
    ) -> Dict[str, float]:
        return await _get_training_metrics_from_workers(self.mailbox)

    async def run(
        self,
        pretrained_file: Optional[Union[str, os.PathLike]] = None,
        **kwargs: Any,
    ) -> List[Dict[str, float]]:
        """Receives updates and sends new parameters in a loop."""
        self.algorithm.initialise(pretrained_file=pretrained_file)
        self.perform_iterations_checks()
        initial_parameters = self.algorithm.run(update=None)
        await self._send_parameters(initial_parameters)
        num_federated_iterations = self.get_num_federated_iterations()
        for i in range(1, num_federated_iterations + 1):
            if self.algorithm.epochs:
                logger.info(f"Federated Epoch {i}")
            else:
                logger.info(f"Federated Step {i}")

            logger.info("Sending model parameters to Pods")
            if self.auto_eval:
                # We create this as a task so that it can process TRAINING_METRICS
                # messages in the background without blocking TRAINING_UPDATE
                # messages.
                validation_metrics_task = asyncio.create_task(
                    self._get_training_metrics_updates()
                )

            weight_updates = await self._receive_parameter_updates()
            logger.federated_info("Aggregating parameter updates")
            parameter_update = self.aggregator.run(
                parameter_updates=weight_updates,
                tensor_dtype=self.algorithm.tensor_precision,
            )
            if self.auto_eval:
                # This is guaranteed to be bound as it's creation is also in a
                # `if self.auto_eval:` block.
                # noinspection PyUnboundLocalVariable
                await validation_metrics_task
                validation_metrics: Dict[str, float] = validation_metrics_task.result()
                logger.info(
                    f"Validation Metrics at iteration {i}: {validation_metrics}"
                )
                # Each item in the list is the average results from every worker
                # for a given iteration. New results are appended to the list
                # such that the final item is always the latest.
                self.validation_results.append(validation_metrics)

                new_parameters = self.algorithm.run(
                    update=parameter_update, validation_metrics=validation_metrics
                )
                # Send the latest averaged validation metrics only at each iteration
            else:
                new_parameters = self.algorithm.run(update=parameter_update)

            logger.federated_info("Sending updated parameters")
            await self._send_parameters(
                new_parameters
            )  # Workers end up with final model

            # TODO: [BIT-970] consider moving early stopping to be handled in a side
            #       channel as part of handler based approach
            training_complete = False
            if self.early_stopping is not None:
                training_complete = self.early_stopping.check(self.validation_results)
            await self.mailbox.send_training_iteration_complete_update(
                training_complete
            )
            if training_complete:
                logger.info("Early stopping criterion met. Stopping training.")
                break
        await self.mailbox.send_task_complete_message()
        modeller_results = self.validation_results
        return modeller_results


class _WorkerSide(_BaseWorkerProtocol, _BaseFederatedAveragingMixIn):
    """Worker side of the FederatedAveraging protocol."""

    aggregator: _BaseWorkerAggregator
    algorithm: _FederatedAveragingCompatibleWorker

    def __init__(
        self,
        *,
        algorithm: _FederatedAveragingCompatibleWorker,
        mailbox: _WorkerMailbox,
        aggregator: _BaseWorkerAggregator,
        steps_between_parameter_updates: Optional[int],
        epochs_between_parameter_updates: Optional[int],
        auto_eval: bool = True,
        **kwargs: Any,
    ):
        super().__init__(
            algorithm=algorithm,
            mailbox=mailbox,
            aggregator=aggregator,
            steps_between_parameter_updates=steps_between_parameter_updates,
            epochs_between_parameter_updates=epochs_between_parameter_updates,
            auto_eval=auto_eval,
            **kwargs,
        )
        self.auto_eval = auto_eval

    async def _receive_parameters(self) -> _SerializedWeights:
        """Receives new global model parameters."""
        logger.debug("Receiving global parameters")
        return await _get_model_parameters(self.mailbox)

    async def _send_training_metrics(
        self,
        validation_metrics: Optional[Mapping[str, str]] = None,
    ) -> None:
        """Sends training metrics update."""
        if validation_metrics:
            logger.debug("Sending validation metrics to modeller")
            await _send_training_metrics(validation_metrics, self.mailbox)

    async def _send_parameter_update(
        self, parameter_update: _SerializedWeights
    ) -> None:
        """Sends parameter update."""
        logger.debug("Sending parameter update to modeller")
        await _send_parameter_update(parameter_update, self.mailbox)

    async def run(
        self,
        datasource: DataSource,
        pod_dp: Optional[DPPodConfig] = None,
        pod_vitals: Optional[_PodVitals] = None,
        **kwargs: Any,
    ) -> None:
        """Receives parameters and sends updates in a loop."""
        self.algorithm.initialise(datasource=datasource, pod_dp=pod_dp)
        self.perform_iterations_checks()
        model_params = await self._receive_parameters()

        num_federated_iterations = self.get_num_federated_iterations()
        for i in range(1, num_federated_iterations + 1):
            if self.algorithm.epochs:
                logger.info(f"Federated Epoch {i}")
                iterations = self.epochs_between_parameter_updates
            else:
                logger.info(f"Federated Step {i}")
                iterations = self.steps_between_parameter_updates
            iterations = cast(int, iterations)
            logger.federated_info("Running algorithm")
            if pod_vitals:
                pod_vitals.last_task_execution_time = time.time()
            parameter_update, validation_metrics = self.algorithm.run(
                datasource, model_params, iterations
            )

            aggregated_parameter_update = await self.aggregator.run(
                parameter_update=parameter_update
            )
            if self.auto_eval:
                logger.info(
                    f"Validation Metrics at iteration {i}: {validation_metrics}"
                )
                await self._send_training_metrics(validation_metrics)
            await self._send_parameter_update(aggregated_parameter_update)
            model_params = await self._receive_parameters()

            # TODO: [BIT-970] consider moving early stopping to be handled in a side
            #       channel as part of handler based approach
            training_complete = (
                await self.mailbox.get_training_iteration_complete_update()
            )
            if training_complete:
                logger.info(
                    "Modeller reporting early stopping criterion met. "
                    + "Stopping training.",
                )
                break
        await self.mailbox.get_task_complete_update()
        self.algorithm.save_final_parameters(model_params)


class FederatedAveraging(_ProtocolAggregatorSchema, _BaseProtocolFactory):
    """Original Federated Averaging algorithm by McMahan et al. (2017).

    This protocol performs a predetermined number of epochs or steps of training on
    each remote Pod before sending the updated model parameters to the modeller. These
    parameters are then averaged and sent back to the Pods for as many federated
    iterations as the Modeller specifies.

    Args:
        algorithm: The algorithm to use for training. This must be compatible with the
            `FederatedAveraging` protocol.
        aggregator: The aggregator to use for updating the model parameters across all
            Pods participating in the task.
        steps_between_parameter_updates: The number of steps between parameter updates,
            i.e. the number of rounds of local training before parameters are updated.
            If `epochs_between_parameter_updates` is provided,
            `steps_between_parameter_updates` cannot be provided. Defaults to None.
        epochs_between_parameter_updates: The number of epochs between parameter
            updates, i.e. the number of rounds of local training before parameters are
            updated. If `steps_between_parameter_updates` is provided,
            `epochs_between_parameter_updates` cannot be provided. Defaults to None.
        auto_eval: Whether to automatically evaluate the model on the validation
            dataset. Defaults to True.

    Attributes:
        name: The name of the protocol.
        algorithm: The algorithm to use for training
        aggregator: The aggregator to use for updating the model parameters.
        steps_between_parameter_updates: The number of steps between parameter updates.
        epochs_between_parameter_updates: The number of epochs between parameter
            updates.
        auto_eval: Whether to automatically evaluate the model on the validation
            dataset.

    Raises:
        TypeError: If the `algorithm` is not compatible with the protocol.

    :::tip

    For more information, take a look at the seminal paper:
    https://arxiv.org/abs/1602.05629

    :::
    """

    algorithm: _FederatedAveragingCompatibleAlgoFactory

    def __init__(
        self,
        *,
        algorithm: _FederatedAveragingCompatibleAlgoFactory,
        aggregator: _BaseAggregatorFactory,
        steps_between_parameter_updates: Optional[int] = None,
        epochs_between_parameter_updates: Optional[int] = None,
        auto_eval: bool = True,
        **kwargs: Any,
    ) -> None:
        super().__init__(algorithm=algorithm, **kwargs)
        self.aggregator = aggregator
        self.steps_between_parameter_updates = steps_between_parameter_updates
        self.epochs_between_parameter_updates = epochs_between_parameter_updates
        self.auto_eval = auto_eval

    @classmethod
    def _validate_algorithm(cls, algorithm: _BaseCompatibleAlgoFactory) -> None:
        """Checks that `algorithm` is compatible with the protocol.

        Raises:
            TypeError: If the `algorithm` is not compatible with the protocol.
        """
        if not isinstance(algorithm, _FederatedAveragingCompatibleAlgoFactory):
            raise TypeError(
                f"The {cls.__name__} protocol does not support "
                + f"the {type(algorithm).__name__} algorithm.",
            )

    def modeller(
        self,
        mailbox: _ModellerMailbox,
        early_stopping: Optional[FederatedEarlyStopping] = None,
        **kwargs: Any,
    ) -> _ModellerSide:
        """Returns the modeller side of the FederatedAveraging protocol."""
        return _ModellerSide(
            algorithm=self.algorithm.modeller(),
            aggregator=self.aggregator.modeller(),
            steps_between_parameter_updates=self.steps_between_parameter_updates,
            epochs_between_parameter_updates=self.epochs_between_parameter_updates,
            auto_eval=self.auto_eval,
            mailbox=mailbox,
            early_stopping=early_stopping,
            **kwargs,
        )

    def worker(
        self,
        mailbox: _WorkerMailbox,
        hub: BitfountHub,
        **kwargs: Any,
    ) -> _WorkerSide:
        """Returns the worker side of the FederatedAveraging protocol."""
        if isinstance(self.aggregator, _AggregatorWorkerFactory):
            worker_agg = self.aggregator.worker()
        elif isinstance(self.aggregator, _InterPodAggregatorWorkerFactory):
            worker_agg = self.aggregator.worker(mailbox=mailbox)
        else:
            raise TypeError(
                f"Unrecognised aggregator factory ({type(self.aggregator)}); "
                f"unable to determine how to call .worker() factory method."
            )
        return _WorkerSide(
            algorithm=self.algorithm.worker(hub=hub),
            aggregator=worker_agg,
            steps_between_parameter_updates=self.steps_between_parameter_updates,
            epochs_between_parameter_updates=self.epochs_between_parameter_updates,
            auto_eval=self.auto_eval,
            mailbox=mailbox,
            **kwargs,
        )

    @classmethod
    def run(
        cls,
        pod_identifiers: Iterable[str],
        username: Optional[str] = None,
        model: Optional[_DistributedModelTypeOrReference] = None,
        algorithm: Optional[_FederatedAveragingCompatibleAlgoFactory] = None,
        aggregator: Optional[_BaseAggregatorFactory] = None,
        steps_between_parameter_updates: Optional[int] = None,
        epochs_between_parameter_updates: Optional[int] = None,
        hub: Optional[BitfountHub] = None,
        ms_config: Optional[MessageServiceConfig] = None,
        message_service: Optional[_MessageService] = None,
        pod_public_key_paths: Optional[Mapping[str, Path]] = None,
        pretrained_file: Optional[Union[str, os.PathLike]] = None,
        secure_aggregation: bool = False,
        auto_eval: bool = True,
        identity_verification_method: Union[
            str, IdentityVerificationMethod
        ] = IdentityVerificationMethod.DEFAULT,
        private_key_or_file: Optional[Union[RSAPrivateKey, Path]] = None,
        idp_url: Optional[str] = None,
    ) -> Optional[Any]:
        """Quickstart method for running the protocol as a `Modeller`.

        Running this method avoids the need to create a `Modeller` or any of the other
        instances required to run the protocol. However, these can still be provided
        to override the default values.

        ```python title="Example usage:"
        import bitfount as bf

        bf.FederatedAveraging.run(
            pod_identifiers=["bitfount/example-pod-1", "bitfount/example-pod-2"],
            algorithm=bf.FederatedModelTraining(
                model=bf.PyTorchTabularClassifier(...),
            ),
        )
        ```

        Args:
            pod_identifiers: The identifiers of the pods to participate in the
                task as a list of strings.
            username: The username of the Modeller. This is only necessary if you are
                switching between multiple accounts. Defaults to None.
            model: The model to train. If `algorithm` is provided, this `model` is
                ignored. Defaults to None.
            algorithm: The algorithm to use for training. If `model` is not provided,
                this must be provided. Defaults to None.
            aggregator: The aggregator to use for updating the model parameters.
                Defaults to None.
            steps_between_parameter_updates: The number of steps between parameter
                updates. If neither `steps_between_parameter_updates` nor
                `epochs_between_parameter_updates` are provided,
                `steps_between_parameter_updates` is set to 1. Defaults to None.
            epochs_between_parameter_updates: The number of epochs between parameter
                updates. If neither `steps_between_parameter_updates` nor
                `epochs_between_parameter_updates` are provided,
                `steps_between_parameter_updates` is set to 1. Defaults to None.
            hub: The `BitfountHub` object to use for communication with the hub.
                Defaults to None.
            ms_config: The `MessageServiceConfig` used to create an instance of
                `MessageService` if not provided. Defaults to None.
            message_service: The `MessageService` object to use for communication
                with other Pods and Modeller. Defaults to None.
            pod_public_key_paths: The paths to the public keys of the Pods involved in
                the task. Defaults to None.
            pretrained_file: The path to a file containing a pretrained model. Defaults
                to None.
            secure_aggregation: Whether to use secure aggregation. Defaults to False.
            auto_eval: Whether to automatically evaluate the model on the validation
                dataset. Defaults to True.
            identity_verification_method: The method used to verify the identity of
                the Modeller. Defaults to SAML.
            private_key_or_file: The private key used to sign the messages.
            idp_url: The URL of the Identity Provider. Defaults to Bitfount's identity
                provider.

        Raises:
            ValueError: If neither `model` nor `algorithm` are provided.

        :::tip

        The `pod_identifiers` and one of `model` or `algorithm` are the only arguments
        that are necessary. Everything else can be created on the fly.

        :::
        """
        if model is not None and algorithm is not None:
            logger.warning("Ignoring provided model. Algorithm already has a model.")
        elif model is not None:
            algorithm = FederatedModelTraining(model=model)
        elif model is None and algorithm is None:
            raise ValueError(
                "Must provide either the model or the algorithm containing the model."
            )

        if not hub:
            hub = _create_bitfounthub(username=username)

        if not message_service:
            message_service = _create_message_service(
                session=hub.session, ms_config=ms_config
            )
        if not aggregator:
            aggregator = _create_aggregator(
                model=algorithm.model, secure_aggregation=secure_aggregation
            )

        protocol = _create_federated_averaging_protocol_factory(
            protocol_cls=cls,
            algorithm=algorithm,
            aggregator=aggregator,
            steps_between_parameter_updates=steps_between_parameter_updates,
            epochs_between_parameter_updates=epochs_between_parameter_updates,
            auto_eval=auto_eval,
        )

        return _run_protocol(
            protocol=protocol,
            pod_identifiers=pod_identifiers,
            hub=hub,
            message_service=message_service,
            pod_public_key_paths=pod_public_key_paths,
            pretrained_file=pretrained_file,
            identity_verification_method=check_identity_verification_method(
                identity_verification_method
            ),
            private_key_or_file=private_key_or_file,
            idp_url=idp_url if idp_url is not None else _PRODUCTION_IDP_URL,
        )

    @staticmethod
    def get_schema(
        algorithm_schema: Type[MarshmallowSchema],
        aggregator_schema: Type[MarshmallowSchema],
        **kwargs: Any,
    ) -> MarshmallowSchema:
        """Returns the schema for FederatedAveraging."""

        class Schema(_BaseProtocolFactory._Schema):
            algorithm = fields.Nested(algorithm_schema)
            aggregator = fields.Nested(aggregator_schema)
            steps_between_parameter_updates = fields.Integer(allow_none=True)
            epochs_between_parameter_updates = fields.Integer(allow_none=True)
            auto_eval = fields.Boolean()

            @post_load
            def recreate_factory(
                self, data: dict, **_kwargs: Any
            ) -> FederatedAveraging:
                return FederatedAveraging(**data)

        return Schema()

    def dump(self) -> _JSONDict:
        """Returns the JSON-serializable representation of the protocol."""
        # TODO: [BIT-889] Getting schemas should not be the responsibility of
        #       this method.
        algorithm_schema = self.algorithm.get_schema(self.algorithm.model_schema)
        aggregator_schema = self.aggregator.get_schema(
            tensor_shim_factory=self.algorithm.model.backend_tensor_shim
        )
        schema = self.get_schema(algorithm_schema, aggregator_schema)
        return cast(_JSONDict, schema.dump(self))
