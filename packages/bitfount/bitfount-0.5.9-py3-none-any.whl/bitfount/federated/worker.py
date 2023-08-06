"""Workers for handling task running on pods."""
from __future__ import annotations

import logging
from typing import Any, Optional, Type

from marshmallow import Schema as MarshmallowSchema

from bitfount.data.datasource import DataSource
from bitfount.federated.algorithms.base import _BaseAlgorithmSchema
from bitfount.federated.algorithms.model_algorithms.base import (
    _BaseModelAlgorithmSchema,
)
from bitfount.federated.authorisation_checkers import _AuthorisationChecker
from bitfount.federated.logging import _get_federated_logger
from bitfount.federated.model_reference import BitfountModelReference
from bitfount.federated.pod_vitals import _PodVitals
from bitfount.federated.privacy.differential import DPPodConfig
from bitfount.federated.protocols.base import _BaseProtocolFactory
from bitfount.federated.transport.message_service import _BitfountMessageType
from bitfount.federated.transport.worker_transport import _WorkerMailbox
from bitfount.federated.utils import (
    _AGGREGATORS,
    _ALGORITHMS,
    _DISTRIBUTED_MODELS,
    _MODELS,
    _PROTOCOLS,
)
from bitfount.hub.api import BitfountHub

logger = _get_federated_logger(__name__)


class _Worker:
    """Client worker which performs training locally.

    Trains model locally and sends optionally encrypted updates back to modeller.

    Args:
        data: DataSource object
        mailbox: relevant mailbox
        bitfounthub: BitfountHub object
    """

    def __init__(
        self,
        data: DataSource,
        mailbox: _WorkerMailbox,
        bitfounthub: BitfountHub,
        authorisation: _AuthorisationChecker,
        pod_vitals: Optional[_PodVitals] = None,
        pod_dp: Optional[DPPodConfig] = None,
        **_kwargs: Any,
    ):
        self.data = data
        self.mailbox = mailbox
        self.hub = bitfounthub
        self.authorisation: _AuthorisationChecker = authorisation
        self.pod_vitals = pod_vitals
        self._pod_dp = pod_dp

    def _deserialize_protocol(self, serialized_protocol: dict) -> _BaseProtocolFactory:
        """Takes a marshmallow serialized protocol, instantiates and returns it."""
        model_schema: Optional[Type[MarshmallowSchema]] = None
        aggregator_schema: Optional[Type[MarshmallowSchema]] = None

        if "model" in serialized_protocol["algorithm"]:
            model = None
            model_name = serialized_protocol["algorithm"]["model"].pop("name")
            # Currently, if there is an aggregator, it means there is necessarily also
            # a distributed model
            if model_name == "BitfountModelReference":
                schema = BitfountModelReference._Schema()
                model = schema.load(serialized_protocol["algorithm"]["model"])
                model.hub = self.hub

            if "aggregator" in serialized_protocol:
                if model is None:
                    try:
                        model = _DISTRIBUTED_MODELS[model_name]
                    except KeyError:
                        logging.error(
                            "Modeller has sent a model that is incompatible"
                            + " with their chosen algorithm/protocol.",
                        )
                        raise ValueError

                aggregator_cls = _AGGREGATORS[serialized_protocol["aggregator"]["name"]]
                aggregator_schema = aggregator_cls.get_schema(
                    tensor_shim_factory=model.backend_tensor_shim
                )
                model_schema = model.get_schema()
            else:
                if model is None:
                    model = _MODELS[model_name]
                model_schema = model.get_schema()

        algorithm_cls = _ALGORITHMS[serialized_protocol["algorithm"]["name"]]

        if issubclass(algorithm_cls, _BaseAlgorithmSchema):
            algorithm_schema = algorithm_cls.get_schema()
        elif issubclass(algorithm_cls, _BaseModelAlgorithmSchema):
            if model_schema is None:
                raise TypeError(
                    f"Chosen algorithm ({algorithm_cls}) is a model algorithm, "
                    f"but no model schema was specified"
                )
            algorithm_schema = algorithm_cls.get_schema(model_schema=model_schema)
        else:
            raise AttributeError(
                f"Algorithm class {algorithm_cls} does not implement get_schema()"
            )

        return _PROTOCOLS[serialized_protocol["name"]].load(
            serialized_protocol=serialized_protocol,
            algorithm_schema=algorithm_schema,
            aggregator_schema=aggregator_schema,
        )

    async def _get_protocol(self) -> _BaseProtocolFactory:
        """Retrieves the protocol."""
        serialized_protocol = await self.mailbox.get_task_details()
        return self._deserialize_protocol(serialized_protocol)

    async def run(self) -> None:
        """Calls relevant training procedure and sends back weights/results."""
        authorisation_errors = await self.authorisation.check_authorisation()

        if authorisation_errors.messages:
            # Reject task, as there were errors
            await self.mailbox.reject_task(
                authorisation_errors.messages,
            )
            return

        # Accept task and inform modeller
        logger.info("Task accepted, informing modeller.")
        await self.mailbox.accept_task()

        protocol = await self._get_protocol()
        verified = self.authorisation.verify_protocol(protocol)

        if not verified:
            logger.federated_error(
                "The protocol that has been received does not match "
                "the original protocol that was authorised and accepted. "
                "Aborting task."
            )
            self.mailbox.delete_handler(_BitfountMessageType.LOG_MESSAGE)
            return

        # Calling the `worker` method on the protocol also calls the `worker` method on
        # underlying objects such as the algorithm and aggregator. The algorithm
        # `worker` method will also download the model from the Hub if it is a
        # `BitfountModelReference`
        worker_protocol = protocol.worker(mailbox=self.mailbox, hub=self.hub)
        await worker_protocol.run(
            datasource=self.data, pod_dp=self._pod_dp, pod_vitals=self.pod_vitals
        )
        logger.info("Task complete")
        self.mailbox.delete_handler(_BitfountMessageType.LOG_MESSAGE)
