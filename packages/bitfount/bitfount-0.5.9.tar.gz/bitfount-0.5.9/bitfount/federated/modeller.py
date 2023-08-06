"""Modeller for dispatching tasks."""
from __future__ import annotations

import asyncio
from functools import partial
import os
from pathlib import Path
from typing import (
    TYPE_CHECKING,
    Any,
    Dict,
    Iterable,
    Literal,
    Mapping,
    Optional,
    Type,
    Union,
    cast,
)

from cryptography.hazmat.primitives.asymmetric.rsa import RSAPrivateKey, RSAPublicKey

from bitfount.federated.algorithms.model_algorithms.base import (
    _BaseModelAlgorithmFactory,
)
from bitfount.federated.authorisation_checkers import (
    _IDENTITY_VERIFICATION_METHODS_MAP,
    IdentityVerificationMethod,
    _SignatureBasedAuthorisation,
    check_identity_verification_method,
)
from bitfount.federated.encryption import _RSAEncryption
from bitfount.federated.helper import _create_message_service
from bitfount.federated.logging import _get_federated_logger
from bitfount.federated.model_reference import BitfountModelReference
from bitfount.federated.task_requests import _ProtocolDetails
from bitfount.federated.transport.base_transport import _run_func_and_listen_to_mailbox
from bitfount.federated.transport.identity_verification.oidc import (
    _OIDCAuthFlowChallengeHandler,
    _OIDCDeviceCodeHandler,
)
from bitfount.federated.transport.identity_verification.saml import (
    _SAMLChallengeHandler,
)
from bitfount.federated.transport.message_service import (
    _BitfountMessageType,
    _MessageService,
)
from bitfount.federated.transport.modeller_transport import _ModellerMailbox
from bitfount.federated.types import (
    AggregatorType,
    AlgorithmType,
    ProtocolType,
    _ResponseHandler,
    _TaskRequestMessageGenerator,
)
from bitfount.hub.api import _PRODUCTION_IDP_URL, BitfountHub
from bitfount.hub.authentication_flow import _get_auth_environment
from bitfount.hub.helper import _default_bitfounthub, _get_pod_public_keys

if TYPE_CHECKING:
    from bitfount.federated.protocols.base import _BaseProtocolFactory


logger = _get_federated_logger(__name__)


class Modeller:
    """Dispatches tasks to pods and runs the modeller side of the provided protocol.

    ```python title="Example usage:"
    import bitfount as bf

    modeller=bf.Modeller(
        protocol=bf.FederatedAveraging(...),
    )
    modeller.run(pod_identifiers=["bitfount/example-pod-1", "bitfount/example-pod-2"])
    ```

    Args:
        protocol: The protocol to use for the task.
        message_service: The message service to use for communication with pods.
            Defaults to None, in which case a new message service will be created.
        bitfounthub: Hub instance for Bitfount Hub communication. Defaults to None,
            in which case a new `BitfountHub` instance will be created.
        pod_public_key_paths: Optional. Mapping of pod identifiers to public
            key files for existing pod public keys. Expired or non-existent
            keys will be downloaded from the Hub.
        pretrained_file: Path to a file containing pretrained model parameters.
            Defaults to None.
        identity_verification_method: The identity verification method to use.
            Defaults to SAML.
        private_key: This modeller's private key either as an `RSAPrivateKey`
            instance or a path to a private key file. If a non-key-based identity
            verification method is used, this is ignored. Defaults to None.
        idp_url: URL of identity provider. Defaults to production SAML URL.

    Attributes:
        protocol: The protocol to use for the task.

    Raises:
        ValueError: If key-based identity verification is selected but no
            private key is provided.
    """

    def __init__(
        self,
        protocol: _BaseProtocolFactory,
        message_service: Optional[_MessageService] = None,
        bitfounthub: Optional[BitfountHub] = None,
        pod_public_key_paths: Optional[Mapping[str, Path]] = None,
        pretrained_file: Optional[Union[str, os.PathLike]] = None,
        identity_verification_method: Union[
            str, IdentityVerificationMethod
        ] = IdentityVerificationMethod.DEFAULT,
        private_key: Optional[Union[RSAPrivateKey, Path]] = None,
        idp_url: Optional[str] = None,
    ):
        self.protocol = protocol
        self._hub = _default_bitfounthub(hub=bitfounthub)
        self._message_service = (
            message_service
            if message_service is not None
            else _create_message_service(session=self._hub.session)
        )

        self._pod_public_key_paths: Mapping[str, Path] = pod_public_key_paths or dict()

        # TODO: [BIT-1252] pretrained file should not be passed here
        self._pretrained_file = pretrained_file

        self._identity_verification_method: IdentityVerificationMethod = (
            check_identity_verification_method(identity_verification_method)
        )
        # Load private key if needed
        self._private_key: Optional[RSAPrivateKey] = None
        if self._identity_verification_method == IdentityVerificationMethod.KEYS:
            if not private_key:
                raise ValueError(
                    "Key-based identity verification selected but "
                    "no private key provided."
                )
            elif isinstance(private_key, Path):
                self._private_key = _RSAEncryption.load_private_key(private_key)
            else:
                self._private_key = private_key
        else:
            if private_key:
                logger.warning(
                    f"Private key provided but identity verification method "
                    f'"{self._identity_verification_method.value}" was chosen. '
                    f"Private key will be ignored."
                )
        self._idp_url = idp_url if idp_url is not None else _PRODUCTION_IDP_URL

    async def _send_task_requests(
        self, pod_identifiers: Iterable[str]
    ) -> _ModellerMailbox:
        """Sends task requests to pods.

        Args:
            pod_identifiers: The group of pods to run the task with.

        Returns:
            The created ModellerMailbox for the task.
        """
        # Load pod public keys
        loaded_pod_public_keys: Dict[str, RSAPublicKey] = _get_pod_public_keys(
            pod_identifiers=pod_identifiers,
            hub=self._hub,
            pod_public_key_paths=self._pod_public_key_paths,
        )

        # The bare minumum task request has as just a protocol and an algorithm.
        partial_protocol_details = partial(
            _ProtocolDetails,
            protocol=ProtocolType[self.protocol.name].value,
            algorithm=AlgorithmType[self.protocol.algorithm.name].value,
        )

        if isinstance(self.protocol.algorithm, _BaseModelAlgorithmFactory):
            # If the algorithm is an instance of `_BaseModelAlgorithmFactory`, this
            # means it has a model. This model is either a `BitfountModelReference`
            # or a built-in model.
            if isinstance(self.protocol.algorithm.model, BitfountModelReference):
                # If the model is a `BitfountModelReference`, we send the `model_ref`
                # prefixed with the `username` of the model.
                model = self.protocol.algorithm.model
                model_name = f"{model.username}.{model.model_ref}"
            else:
                # If the model is a built-in model, we send the model name prefixed
                # with `bitfount.`
                model_name = f"bitfount.{self.protocol.algorithm.model.name}"

            # Currently there can only be an aggregator if the algorithm has a model so
            # we can safely add the aggregator to the protocol details here.
            if hasattr(self.protocol, "aggregator"):
                protocol_details = partial_protocol_details(
                    model=model_name,
                    aggregator=AggregatorType[self.protocol.aggregator.name].value,  # type: ignore[attr-defined] # Reason: hasattr check # noqa: B950
                )
            # If there is no aggregator, we can just add the model to the protocol
            # details.
            else:
                protocol_details = partial_protocol_details(model=model_name)
        else:
            # If the algorithm is not an instance of `_BaseModelAlgorithmFactory`, this
            # means it has no model (and therefore no aggregator either).
            protocol_details = partial_protocol_details()

        task_request_msg_gen = self._get_task_request_msg_gen()

        # Send task requests to chosen pods. We haven't attached a handler for the
        # responses yet but this is handled below. There is no issue due to the
        # fact that the listening task hasn't been started yet, and the inherent
        # handler backoff.
        modeller_mailbox: _ModellerMailbox = await _ModellerMailbox.send_task_requests(
            protocol_details=protocol_details,
            pod_public_keys=loaded_pod_public_keys,
            task_request_msg_gen=task_request_msg_gen,
            message_service=self._message_service,
        )

        return modeller_mailbox

    def _get_task_request_msg_gen(self) -> _TaskRequestMessageGenerator:
        """Construct correct TaskRequestMessageGenerator object for the auth type."""
        authorization_checker_cls = _IDENTITY_VERIFICATION_METHODS_MAP[
            self._identity_verification_method
        ]
        if self._identity_verification_method == IdentityVerificationMethod.KEYS:
            authorization_checker_cls = cast(
                Type[_SignatureBasedAuthorisation], authorization_checker_cls
            )
            if not self._private_key:
                raise ValueError(
                    "Signature-based identification selected but no "
                    "private key provided."
                )
            return authorization_checker_cls.create_task_request_message_generator(
                self._private_key
            )
        else:
            return authorization_checker_cls.create_task_request_message_generator()

    async def _modeller_run(
        self,
        modeller_mailbox: _ModellerMailbox,
        response_handler: Optional[_ResponseHandler] = None,
    ) -> Union[Literal[False], Optional[Any]]:
        """Waits for pod responses and handles any who don't respond in time.

        Runs the modeller side of the protocol if some pods accepted the task.
        """
        # If additional response handling is specified, we call the handler
        if response_handler:
            await response_handler.handle(modeller_mailbox)

        # Process job accept/reject
        await modeller_mailbox.process_task_request_responses()

        # Fail-fast if no pod accepted.
        if not modeller_mailbox.accepted_worker_mailboxes:
            logger.error(
                "No workers with which to train. "
                "Please ensure you have sent task requests at least some of "
                "which have been accepted."
            )
            return False

        return await self._run_modeller_protocol(modeller_mailbox)

    async def _run_modeller_protocol(
        self, modeller_mailbox: _ModellerMailbox
    ) -> Optional[Any]:
        """Runs the modeller-side of the protocol."""
        # Run the task
        await modeller_mailbox.send_task_details(self.protocol.dump())
        protocol = self.protocol.modeller(mailbox=modeller_mailbox)
        result = await protocol.run(pretrained_file=self._pretrained_file)
        return result

    async def run_async(
        self,
        pod_identifiers: Iterable[str],
    ) -> Union[Literal[False], Optional[Any]]:
        """Runs the modeller's task with a set of pods.

        Will send a task request before commencing the task itself and only pods that
        accept the task request will be used.

        Args:
            pod_identifiers: The identifiers for the pods to run the task on.

        Returns:
            Whatever the protocol's return value is.
        """
        response_handler = self._get_response_handler()

        logger.info("Sending task requests...")
        modeller_mailbox: _ModellerMailbox = await self._send_task_requests(
            pod_identifiers
        )

        run_result: Union[
            Literal[False], Optional[Any]
        ] = await _run_func_and_listen_to_mailbox(
            self._modeller_run(
                modeller_mailbox=modeller_mailbox, response_handler=response_handler
            ),
            modeller_mailbox,
        )
        modeller_mailbox.delete_handler(_BitfountMessageType.LOG_MESSAGE)

        logger.info("Task complete")
        return run_result

    def _get_response_handler(self) -> Optional[_ResponseHandler]:
        """Construct a response handler for additional task messages if required.

        This may spin-up web servers if the response handler requires it. It is
        the responsibility of the handler to shut these down when no longer needed.
        """
        response_handler: Optional[_ResponseHandler] = None

        # SAML
        if self._identity_verification_method == IdentityVerificationMethod.SAML:
            logger.debug("Setting up SAML challenge listener")
            response_handler = _SAMLChallengeHandler(self._idp_url)
            # Start challenge handler in background as it takes some time
            asyncio.create_task(response_handler.start())

        # OIDC_ACF_PKCE
        elif (
            self._identity_verification_method
            == IdentityVerificationMethod.OIDC_ACF_PKCE
        ):
            auth_env = _get_auth_environment()
            logger.debug(
                f"Setting up OIDC Authorization Code Flow challenge listener against "
                f"{auth_env.name} authorization environment."
            )
            response_handler = _OIDCAuthFlowChallengeHandler(
                auth_domain=auth_env.auth_domain
            )
            # Start challenge handler in background as it takes some time
            asyncio.create_task(response_handler.start())

        # OIDC_DEVICE_CODE
        elif (
            self._identity_verification_method
            == IdentityVerificationMethod.OIDC_DEVICE_CODE
        ):
            auth_env = _get_auth_environment()
            response_handler = _OIDCDeviceCodeHandler(auth_domain=auth_env.auth_domain)

        return response_handler

    def run(
        self,
        pod_identifiers: Iterable[str],
    ) -> Union[Literal[False], Optional[Any]]:
        """Runs the modeller's task with a set of pods.

        Will send a task request before commencing the task itself and only pods
        that accept the task request will be used.

        Args:
            pod_identifiers: The identifiers for the pods to run the task on.

        Returns:
            Whatever the protocol's return value is.
        """
        return asyncio.run(self.run_async(pod_identifiers))
