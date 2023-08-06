"""Helper functions."""
from __future__ import annotations

from typing import TYPE_CHECKING, Optional, Type

from bitfount.config import (
    _DEVELOPMENT_ENVIRONMENT,
    _STAGING_ENVIRONMENT,
    _get_environment,
)
from bitfount.federated.aggregators.aggregator import Aggregator
from bitfount.federated.aggregators.base import _BaseAggregatorFactory
from bitfount.federated.aggregators.secure import SecureAggregator
from bitfount.federated.logging import _get_federated_logger
from bitfount.federated.secure import SecureShare
from bitfount.federated.transport.config import (
    _DEV_MESSAGE_SERVICE_PORT,
    _DEV_MESSAGE_SERVICE_TLS,
    _DEV_MESSAGE_SERVICE_URL,
    _STAGING_MESSAGE_SERVICE_URL,
    MessageServiceConfig,
)
from bitfount.federated.transport.message_service import _MessageService
from bitfount.federated.transport.pod_transport import _PodMailbox

if TYPE_CHECKING:
    from bitfount.federated.protocols.fed_avg import (
        FederatedAveraging,
        _FederatedAveragingCompatibleAlgoFactory,
    )
    from bitfount.hub.authentication_flow import BitfountSession
    from bitfount.types import _DistributedModelTypeOrReference


logger = _get_federated_logger(__name__)


def _create_aggregator(
    model: _DistributedModelTypeOrReference, secure_aggregation: bool
) -> _BaseAggregatorFactory:
    """Creates aggregator for Federated Averaging.

    Args:
        model: The model used in aggregation.
        secure_aggregation: Boolean denoting whether aggregator should be secure.

    Raises:
        TypeError: If model is not compatible with Federated Averaging.

    Returns:
        The aggregator to be used.
    """
    if secure_aggregation:
        sec_share = SecureShare(
            tensor_shim=model.backend_tensor_shim(),
        )
        return SecureAggregator(
            secure_share=sec_share, tensor_shim=model.backend_tensor_shim()
        )
    return Aggregator(tensor_shim=model.backend_tensor_shim())


def _create_message_service(
    session: BitfountSession, ms_config: Optional[MessageServiceConfig] = None
) -> _MessageService:
    """Helper function to create MessageService object.

    Args:
        session (BitfountSession): bitfount session
        ms_config (Optional[MessageServiceConfig], optional): message service config.
            Defaults to None.

    Returns:
        MessageService object
    """
    if ms_config is None:
        ms_config = MessageServiceConfig()

        environment = _get_environment()
        if environment == _STAGING_ENVIRONMENT:
            ms_config.url = _STAGING_MESSAGE_SERVICE_URL
        elif environment == _DEVELOPMENT_ENVIRONMENT:
            ms_config.url = _DEV_MESSAGE_SERVICE_URL
            ms_config.port = _DEV_MESSAGE_SERVICE_PORT
            ms_config.tls = _DEV_MESSAGE_SERVICE_TLS

    if ms_config.use_local_storage:
        logger.warning(
            "Messages will contain local file references. "
            + "Ensure all pods have access to your local file system. "
            + "Otherwise your task will hang.",
        )

    return _MessageService(session, ms_config)


async def _create_and_connect_pod_mailbox(
    pod_name: str,
    session: BitfountSession,
    ms_config: Optional[MessageServiceConfig] = None,
) -> _PodMailbox:
    """Creates pod mailbox and connects it to the message service.

    Args:
        pod_name: Name of pod.
        session: Bitfount session.
        ms_config: Optional. Message service config, defaults to None.

    Returns:
        The created pod mailbox.
    """
    message_service = _create_message_service(session, ms_config)
    mailbox = await _PodMailbox.connect_pod(
        pod_name=pod_name, message_service=message_service
    )
    return mailbox


def _create_federated_averaging_protocol_factory(
    protocol_cls: Type[FederatedAveraging],
    algorithm: _FederatedAveragingCompatibleAlgoFactory,
    aggregator: _BaseAggregatorFactory,
    steps_between_parameter_updates: Optional[int],
    epochs_between_parameter_updates: Optional[int],
    auto_eval: bool = True,
) -> FederatedAveraging:
    """Creates and returns federated averaging protocol factory.

    Args:
        protocol_cls: The protocol class to use.
        algorithm: Algorithm to use.
        aggregator: Aggregator to use.
        steps_between_parameter_updates: Optional. Protocol hyperparam.
        epochs_between_parameter_updates: Optional. Protocol hyperparam.
        auto_eval: Whether to calculate validation metrics.

    Returns:
        Protocol factory instance.
    """
    if not steps_between_parameter_updates and not epochs_between_parameter_updates:
        steps_between_parameter_updates = 1

    return protocol_cls(
        algorithm=algorithm,
        aggregator=aggregator,
        auto_eval=auto_eval,
        steps_between_parameter_updates=steps_between_parameter_updates,
        epochs_between_parameter_updates=epochs_between_parameter_updates,
    )
