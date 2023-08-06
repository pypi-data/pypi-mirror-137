"""Pod communication protocols.

These classes take an algorithm and are responsible for organising the communication
between Pods and Modeller.

Attributes:
    registry: A read-only dictionary of protocol factory names to their
        implementation classes.
"""
from __future__ import annotations

from abc import ABC, abstractmethod
import inspect
import os
from pathlib import Path
from types import MappingProxyType
from typing import (
    TYPE_CHECKING,
    Any,
    Dict,
    Generic,
    Iterable,
    List,
    Mapping,
    Optional,
    Protocol,
    Type,
    TypeVar,
    Union,
    cast,
)

from cryptography.hazmat.primitives.asymmetric.rsa import RSAPrivateKey
from marshmallow import Schema as MarshmallowSchema
from marshmallow import fields

from bitfount.data import DataSource
from bitfount.federated.authorisation_checkers import IdentityVerificationMethod
from bitfount.federated.helper import _create_message_service
from bitfount.federated.logging import _get_federated_logger
from bitfount.federated.modeller import Modeller
from bitfount.federated.pod_vitals import _PodVitals
from bitfount.federated.privacy.differential import DPPodConfig
from bitfount.federated.roles import _RolesMixIn
from bitfount.federated.transport.base_transport import _BaseMailbox
from bitfount.federated.transport.config import MessageServiceConfig
from bitfount.federated.transport.message_service import _MessageService
from bitfount.federated.transport.modeller_transport import _ModellerMailbox
from bitfount.federated.transport.worker_transport import _WorkerMailbox
from bitfount.hub.api import _PRODUCTION_IDP_URL
from bitfount.hub.helper import _default_bitfounthub
from bitfount.types import _JSONDict

if TYPE_CHECKING:
    from bitfount.hub.api import BitfountHub
    from bitfount.hub.authentication_flow import BitfountSession

logger = _get_federated_logger(__name__)

MB = TypeVar("MB", bound=_BaseMailbox)


class _BaseProtocol(Generic[MB], ABC):
    """Blueprint for modeller side or the worker side of BaseProtocolFactory."""

    def __init__(
        self,
        *,
        algorithm: Union[_BaseCompatibleModeller, _BaseCompatibleWorker],
        mailbox: MB,
        **kwargs: Any,
    ):
        self.algorithm = algorithm
        self.mailbox = mailbox

        super().__init__(**kwargs)


class _BaseCompatibleModeller(Protocol):
    """Protocol defining base modeller-side compatibility."""

    pass


class _BaseModellerProtocol(_BaseProtocol[_ModellerMailbox], ABC):
    """Modeller side of the protocol.

    Calls the modeller side of the algorithm.
    """

    def __init__(
        self,
        *,
        algorithm: _BaseCompatibleModeller,
        mailbox: _ModellerMailbox,
        **kwargs: Any,
    ):
        super().__init__(algorithm=algorithm, mailbox=mailbox, **kwargs)

    @abstractmethod
    async def run(
        self,
        pretrained_file: Optional[Union[str, os.PathLike]] = None,
        **kwargs: Any,
    ) -> List[Any]:
        """Runs Modeller side of the protocol."""
        pass


class _BaseCompatibleWorker(Protocol):
    """Protocol defining base worker-side compatibility."""

    pass


class _BaseWorkerProtocol(_BaseProtocol[_WorkerMailbox], ABC):
    """Worker side of the protocol.

    Calls the worker side of the algorithm.
    """

    def __init__(
        self,
        *,
        algorithm: _BaseCompatibleWorker,
        mailbox: _WorkerMailbox,
        **kwargs: Any,
    ):
        super().__init__(algorithm=algorithm, mailbox=mailbox, **kwargs)

    @abstractmethod
    async def run(
        self,
        datasource: DataSource,
        pod_dp: Optional[DPPodConfig] = None,
        pod_vitals: Optional[_PodVitals] = None,
        **kwargs: Any,
    ) -> None:
        """Runs the worker-side of the algorithm."""
        pass


# The mutable underlying dict that holds the registry information
_registry: Dict[str, Type[_BaseProtocolFactory]] = {}
# The read-only version of the registry that is allowed to be imported
registry: Mapping[str, Type[_BaseProtocolFactory]] = MappingProxyType(_registry)


class _ProtocolSchema(ABC):
    """For protocols with algorithms in their schema generation."""

    @staticmethod
    @abstractmethod
    def get_schema(
        algorithm_schema: Type[MarshmallowSchema],
        **kwargs: Any,
    ) -> MarshmallowSchema:
        """Returns protocol factory schema."""
        raise NotImplementedError


class _ProtocolAggregatorSchema(ABC):
    """For protocols with algorithms and aggregators in schema generation."""

    @staticmethod
    @abstractmethod
    def get_schema(
        algorithm_schema: Type[MarshmallowSchema],
        aggregator_schema: Type[MarshmallowSchema],
        **kwargs: Any,
    ) -> MarshmallowSchema:
        """Get a schema instance for the protocol."""
        pass


class _BaseCompatibleAlgoFactory(Protocol):
    """Protocol defining base algorithm factory compatibility."""

    name: str


class _BaseProtocolFactory(ABC, _RolesMixIn):
    """Base Protocol from which all other protocols must inherit."""

    def __init__(
        self,
        *,
        algorithm: _BaseCompatibleAlgoFactory,
        **kwargs: Any,
    ) -> None:
        super().__init__(**kwargs)
        self.name = type(self).__name__
        self._validate_algorithm(algorithm)
        self.algorithm = algorithm

    @classmethod
    def __init_subclass__(cls, **kwargs: Any):
        if not inspect.isabstract(cls):
            logger.debug(f"Adding {cls.__name__}: {cls} to Protocol registry")
            _registry[cls.__name__] = cls

    @classmethod
    @abstractmethod
    def _validate_algorithm(cls, algorithm: _BaseCompatibleAlgoFactory) -> None:
        """Checks that `algorithm` is compatible with the protocol.

        Raises TypeError if `algorithm` is not compatible with the protocol.
        """
        pass

    @abstractmethod
    def modeller(
        self, mailbox: _ModellerMailbox, **kwargs: Any
    ) -> _BaseModellerProtocol:
        """Creates an instance of the modeller-side for this protocol."""
        raise NotImplementedError

    @abstractmethod
    def worker(
        self, mailbox: _WorkerMailbox, hub: BitfountHub, **kwargs: Any
    ) -> _BaseWorkerProtocol:
        """Creates an instance of the worker-side for this protocol."""
        raise NotImplementedError

    @abstractmethod
    def dump(self) -> _JSONDict:
        """Serialize object, returns as JSON dict."""
        raise NotImplementedError

    class _Schema(MarshmallowSchema):
        """Marshmallow schema."""

        name = fields.Str()

        @abstractmethod
        def recreate_factory(self, data: dict, **kwargs: Any) -> _BaseProtocolFactory:
            """Recreates protocol factory."""
            raise NotImplementedError

    @classmethod
    def load(
        cls, serialized_protocol: _JSONDict, **kwargs: Any
    ) -> _BaseProtocolFactory:
        """Deserializes the protocol instance."""
        if hasattr(cls, "get_schema"):
            schema = cls.get_schema(**kwargs)  # type: ignore[attr-defined] # Reason: hasattr check # noqa: B950
            return cast(_BaseProtocolFactory, schema.load(serialized_protocol))
        else:
            raise AttributeError("Chosen protocol class does not implement get_schema")


def _run_protocol(
    protocol: _BaseProtocolFactory,
    pod_identifiers: Iterable[str],
    session: Optional[BitfountSession] = None,
    username: Optional[str] = None,
    hub: Optional[BitfountHub] = None,
    ms_config: Optional[MessageServiceConfig] = None,
    message_service: Optional[_MessageService] = None,
    pod_public_key_paths: Optional[Mapping[str, Path]] = None,
    pretrained_file: Optional[Union[str, os.PathLike]] = None,
    identity_verification_method: IdentityVerificationMethod = IdentityVerificationMethod.DEFAULT,  # noqa: B950
    private_key_or_file: Optional[Union[RSAPrivateKey, Path]] = None,
    idp_url: str = _PRODUCTION_IDP_URL,
) -> Optional[Any]:
    """Sets up a local Modeller instance and runs the protocol.

    Args:
        protocol: The protocol to run.
        pod_identifiers: The BitfountHub pod identifiers to run against.
        session: Optional. Session to use for authenticated requests. Created if needed.
        username: Username to run as. Defaults to logged in user.
        hub: BitfountHub instance. Default: hub.bitfount.com.
        ms_config: Message service config. Default: messaging.bitfount.com.
        message_service: Message service instance, created from ms_config if not
            provided. Defaults to "messaging.bitfount.com".
        pod_public_key_paths: Public keys of pods to be checked against.
        pretrained_file: File for setting as pre-trained value of model.
        identity_verification_method: The identity verification method to use.
        private_key_or_file: Private key (to be removed).
        idp_url: The IDP URL.

    Returns:
        Results of the protocol.
    """
    hub = _default_bitfounthub(hub=hub, username=username)

    if not session:
        session = hub.session

    if not message_service:
        message_service = _create_message_service(
            session=session,
            ms_config=ms_config,
        )

    modeller = Modeller(
        protocol=protocol,
        message_service=message_service,
        bitfounthub=hub,
        pod_public_key_paths=pod_public_key_paths,
        pretrained_file=pretrained_file,
        identity_verification_method=identity_verification_method,
        private_key=private_key_or_file,
        idp_url=idp_url,
    )
    name = type(protocol).__name__

    logger.info(f"Starting {name} Job...")

    result = modeller.run(pod_identifiers)
    logger.info(f"Completed {name} Job...")
    return result
