"""Tests modeller.py module."""
import logging
from pathlib import Path
import re
import sys
from typing import Dict, List, cast
from unittest.mock import Mock, create_autospec

from _pytest.logging import LogCaptureFixture
from cryptography.hazmat.primitives.asymmetric.rsa import RSAPrivateKey
import pytest
from pytest import fixture
from pytest_mock import MockerFixture

from bitfount.federated.aggregators.aggregator import Aggregator
from bitfount.federated.algorithms.base import _BaseAlgorithmFactory
from bitfount.federated.algorithms.model_algorithms.federated_training import (
    FederatedModelTraining,
)
from bitfount.federated.authorisation_checkers import (
    IdentityVerificationMethod,
    _SAMLAuthorisation,
    _SignatureBasedAuthorisation,
)
from bitfount.federated.encryption import _RSAEncryption
from bitfount.federated.model_reference import BitfountModelReference
from bitfount.federated.modeller import Modeller
from bitfount.federated.protocols.base import _BaseProtocolFactory
from bitfount.federated.task_requests import _ProtocolDetails
from bitfount.federated.transport.base_transport import _WorkerMailboxDetails
from bitfount.federated.transport.message_service import _MessageService
from bitfount.federated.transport.modeller_transport import _ModellerMailbox
from bitfount.federated.types import _ResponseHandler, _TaskRequestMessageGenerator
from bitfount.hub.api import BitfountHub
from bitfount.hub.authentication_flow import _AuthEnv
from tests.bitfount import TEST_SECURITY_FILES
from tests.utils import PytestRequest
from tests.utils.helper import (
    get_debug_logs,
    get_error_logs,
    get_warning_logs,
    unit_test,
)

logging.basicConfig(level=logging.INFO, stream=sys.stdout)

PUBLIC_KEY_PATH = TEST_SECURITY_FILES / "test_public.testkey"
PRIVATE_KEY_PATH = TEST_SECURITY_FILES / "test_private.testkey"


@unit_test
class TestModeller:
    """Unit tests for Modeller."""

    @fixture
    def protocol_factory_name(self) -> str:
        """Fake BaseProtocolFactory.name attribute."""
        return "protocol_factory_name"

    @fixture
    def algorithm_factory_name(self) -> str:
        """Fake BaseAlgorithmFactory.name attribute."""
        return "algorithm_factory_name"

    @fixture
    def aggregator_factory_name(self) -> str:
        """Fake Aggregator.name attribute."""
        return "aggregator_factory_name"

    @fixture
    def model_name(self) -> str:
        """Fake model.name attribute."""
        return "PyTorchTabularClassifier"

    @fixture(
        params=[
            "protocol_with_aggregator",
            "protocol_with_aggregator_custom_model",
            "protocol_without_aggregator",
        ]
    )
    def mock_protocol_factory_param(self, request: PytestRequest) -> str:
        """Allows test-level retrieval of mock_protocol_factory params."""
        return cast(str, request.param)

    @fixture
    def mock_protocol_factory(
        self,
        aggregator_factory_name: str,
        algorithm_factory_name: str,
        mock_protocol_factory_param: str,
        model_name: str,
        protocol_factory_name: str,
    ) -> Mock:
        """A mocked protocol factory.

        Is parameterised to return one with and without an aggregator attribute.
        """
        mock_protocol_factory: Mock = create_autospec(
            _BaseProtocolFactory, instance=True
        )
        mock_protocol_factory.name = protocol_factory_name
        mock_algorithm_factory = create_autospec(_BaseAlgorithmFactory, instance=True)
        mock_algorithm_factory.name = algorithm_factory_name
        mock_protocol_factory.algorithm = mock_algorithm_factory

        # If we are testing with a protocol+aggregator, mock it out.
        if mock_protocol_factory_param != "protocol_without_aggregator":
            mock_aggregator_factory = create_autospec(Aggregator, instance=True)
            mock_protocol_factory.aggregator = mock_aggregator_factory
            mock_aggregator_factory.name = aggregator_factory_name

            if mock_protocol_factory_param == "protocol_with_aggregator":
                mock_algorithm_factory = FederatedModelTraining(model=Mock())
                mock_algorithm_factory.model.name = model_name
                mock_protocol_factory.algorithm = mock_algorithm_factory
            else:
                mock_algorithm_factory = FederatedModelTraining(
                    model=BitfountModelReference(
                        model_ref="MyModel",
                        username="username",
                        datastructure=Mock(),
                        schema=Mock(),
                    )
                )
                mock_protocol_factory.algorithm = mock_algorithm_factory

        return mock_protocol_factory

    @staticmethod
    def _enum__get_item__(x: str) -> Mock:
        """Returns a mock with x set as the `value` attribute."""
        mock = Mock()
        mock.value = x
        return mock

    @fixture
    def mock_protocol_type_enum(self, mocker: MockerFixture) -> Mock:
        """Mocks out the ProtocolType enum."""
        mock_enum = mocker.patch("bitfount.federated.modeller.ProtocolType")
        # Mock out the ProtocolType[x].value accesses
        mock_enum.__getitem__.side_effect = self._enum__get_item__
        return mock_enum

    @fixture
    def mock_algorithm_type_enum(self, mocker: MockerFixture) -> Mock:
        """Mocks out the AlgorithmType enum."""
        mock_enum = mocker.patch("bitfount.federated.modeller.AlgorithmType")
        # Mock out the AlgorithmType[x].value accesses
        mock_enum.__getitem__.side_effect = self._enum__get_item__
        return mock_enum

    @fixture
    def mock_aggregator_type_enum(self, mocker: MockerFixture) -> Mock:
        """Mocks out the AggregatorType enum."""
        mock_enum = mocker.patch("bitfount.federated.modeller.AggregatorType")
        # Mock out the AggregatorType[x].value accesses
        mock_enum.__getitem__.side_effect = self._enum__get_item__
        return mock_enum

    @fixture
    def mock_message_service(self) -> Mock:
        """A mocked message service."""
        mock_message_service: Mock = create_autospec(_MessageService, instance=True)
        return mock_message_service

    @fixture
    def mock_private_key(self) -> Mock:
        """A mocked RSA private key."""
        mock_private_key: Mock = create_autospec(RSAPrivateKey, instance=True)
        return mock_private_key

    @fixture
    def mock_bitfount_hub(self) -> Mock:
        """A mocked BitfountHub instance."""
        mock_bitfount_hub: Mock = create_autospec(BitfountHub, instance=True)
        return mock_bitfount_hub

    @fixture
    def pod_identifiers(self) -> List[str]:
        """A list of pod identifiers."""
        return ["user1/pod1", "user2/pod2"]

    @fixture
    def mock_pod_public_key_paths(self, pod_identifiers: List[str]) -> Dict[str, Mock]:
        """A dictionary of pod identifiers to mocked key file paths."""
        return {pod_identifier: Mock() for pod_identifier in pod_identifiers}

    @fixture
    def pretrained_file(self) -> str:
        """A fake path to a pretrained file."""
        return "fake_pretrained_file_path"

    @fixture
    def modeller(
        self,
        mock_bitfount_hub: Mock,
        mock_message_service: Mock,
        mock_private_key: Mock,
        mock_protocol_factory: Mock,
    ) -> Modeller:
        """Creates a modeller instance with most aspects mocked out.

        Optional args are not mocked, but are left as None.
        """
        modeller = Modeller(
            protocol=mock_protocol_factory,
            message_service=mock_message_service,
            bitfounthub=mock_bitfount_hub,
            private_key=mock_private_key,
        )
        return modeller

    @fixture
    def mock_modeller_mailbox(self) -> Mock:
        """Returns mock mailbox."""
        # Returning "Any" since that is the given return type for create_autospec
        mock_mailbox: Mock = create_autospec(_ModellerMailbox, instance=True)
        return mock_mailbox

    async def test__send_task_requests(
        self,
        aggregator_factory_name: str,
        algorithm_factory_name: str,
        default_task_request_msg_gen: _TaskRequestMessageGenerator,
        mock_aggregator_type_enum: Mock,
        mock_algorithm_type_enum: Mock,
        mock_message_service: Mock,
        mock_modeller_mailbox: Mock,
        mock_private_key: Mock,
        mock_protocol_factory_param: str,
        mock_protocol_type_enum: Mock,
        mocker: MockerFixture,
        model_name: str,
        modeller: Modeller,
        pod_identifiers: List[str],
        protocol_factory_name: str,
    ) -> None:
        """Tests Modeller._send_task_requests()."""
        # Mock out get_pod_public_keys_call; don't need autospec=True as don't
        # care about the actual call details.
        mock_get_public_keys = mocker.patch(
            "bitfount.federated.modeller._get_pod_public_keys"
        )

        # Mock out ModellerMailbox.send_task_requests() class method. autospec=True
        # means we can check assert_called_with() without having to worry about
        # args vs kwargs.
        mock_mailbox_send_task_requests = mocker.patch.object(
            _ModellerMailbox, "send_task_requests", autospec=True
        )
        mock_mailbox_send_task_requests.return_value = mock_modeller_mailbox

        # Recreate the expected task_request_body
        if mock_protocol_factory_param == "protocol_with_aggregator":
            expected_task_request_body = _ProtocolDetails(
                protocol_factory_name,
                "FederatedModelTraining",  # must be an instance of BaseModelAlgorithmFactory # noqa: B950
                f"bitfount.{model_name}",
                aggregator_factory_name,
            )
        elif mock_protocol_factory_param == "protocol_with_aggregator_custom_model":
            expected_task_request_body = _ProtocolDetails(
                protocol_factory_name,
                "FederatedModelTraining",  # must be an instance of BaseModelAlgorithmFactory # noqa: B950
                "username.MyModel",
                aggregator_factory_name,
            )
        else:
            expected_task_request_body = _ProtocolDetails(
                protocol_factory_name,
                algorithm_factory_name,
            )

        modeller_mailbox = await modeller._send_task_requests(pod_identifiers)

        # The mailbox returned from Modeller._send_task_requests() should be the
        # same as the one from ModellerMailbox.send_task_requests().
        assert modeller_mailbox == mock_modeller_mailbox
        # The class method should have been called with correctly constructed args.
        mock_mailbox_send_task_requests.assert_called_once_with(
            protocol_details=expected_task_request_body,
            pod_public_keys=mock_get_public_keys(),
            message_service=mock_message_service,
            task_request_msg_gen=default_task_request_msg_gen,
        )

    def test_modeller_init_fails_invalid_verification_method(
        self,
        mock_bitfount_hub: Mock,
        mock_message_service: Mock,
        mock_protocol_factory: Mock,
    ) -> None:
        """Tests Modeller.__init__ fails if unrecognised verification method."""
        fake_method = "fake_method"

        with pytest.raises(
            ValueError,
            match=re.escape(f"Unsupported identity verification method: {fake_method}"),
        ):
            Modeller(
                protocol=mock_protocol_factory,
                message_service=mock_message_service,
                bitfounthub=mock_bitfount_hub,
                identity_verification_method=fake_method,
            )

    def test_modeller_init_fails_key_based_verification_but_no_key(
        self,
        mock_bitfount_hub: Mock,
        mock_message_service: Mock,
        mock_protocol_factory: Mock,
    ) -> None:
        """Tests Modeller.__init__ fails if key-based verification method, no key."""
        with pytest.raises(
            ValueError,
            match=re.escape(
                "Key-based identity verification selected but no private key provided."
            ),
        ):
            Modeller(
                protocol=mock_protocol_factory,
                message_service=mock_message_service,
                bitfounthub=mock_bitfount_hub,
                identity_verification_method=IdentityVerificationMethod.KEYS,
                private_key=None,
            )

    def test_modeller_init_warns_non_key_verification_but_key_provided(
        self,
        caplog: LogCaptureFixture,
        mock_bitfount_hub: Mock,
        mock_message_service: Mock,
        mock_private_key: Mock,
        mock_protocol_factory: Mock,
    ) -> None:
        """Tests Modeller.__init__ warns if key provided for non-key verification."""
        Modeller(
            protocol=mock_protocol_factory,
            message_service=mock_message_service,
            bitfounthub=mock_bitfount_hub,
            identity_verification_method=IdentityVerificationMethod.SAML,
            private_key=mock_private_key,
        )

        warning_logs = get_warning_logs(caplog)
        assert (
            f"Private key provided but identity verification method "
            f'"{IdentityVerificationMethod.SAML.value}" was chosen. Private key '
            f"will be ignored." in warning_logs
        )

    def test_modeller_init_loads_key_if_path(
        self,
        mock_bitfount_hub: Mock,
        mock_message_service: Mock,
        mock_protocol_factory: Mock,
        mocker: MockerFixture,
    ) -> None:
        """Tests Modeller.__init__ loads key from path."""
        # Mock out key loading
        mock_load_private_key = mocker.patch.object(
            _RSAEncryption, "load_private_key", autospec=True
        )

        # Fake key path
        fake_path = create_autospec(Path, instance=True)

        m = Modeller(
            protocol=mock_protocol_factory,
            message_service=mock_message_service,
            bitfounthub=mock_bitfount_hub,
            identity_verification_method=IdentityVerificationMethod.KEYS,
            private_key=fake_path,
        )

        # Check loading done
        mock_load_private_key.assert_called_once_with(fake_path)
        assert m._private_key == mock_load_private_key.return_value

    def test_modeller_init_loads_key_if_key(
        self,
        mock_bitfount_hub: Mock,
        mock_message_service: Mock,
        mock_private_key: Mock,
        mock_protocol_factory: Mock,
    ) -> None:
        """Tests Modeller.__init__ uses provided key."""
        m = Modeller(
            protocol=mock_protocol_factory,
            message_service=mock_message_service,
            bitfounthub=mock_bitfount_hub,
            identity_verification_method=IdentityVerificationMethod.KEYS,
            private_key=mock_private_key,
        )

        # Check loading done
        assert m._private_key == mock_private_key

    async def test__modeller_run(
        self,
        mock_modeller_mailbox: Mock,
        mocker: MockerFixture,
        modeller: Modeller,
        pod_identifiers: List[str],
    ) -> None:
        """Tests _modeller_run performs expected operations."""
        # Set "accepted" pods
        mock_worker_mailboxes = {
            pod_identifier: create_autospec(_WorkerMailboxDetails, instance=True)
            for pod_identifier in pod_identifiers
        }
        mock_modeller_mailbox.accepted_worker_mailboxes = mock_worker_mailboxes

        # Mock out next call in chain
        mock__run_modeller_protocol = mocker.patch.object(
            modeller, "_run_modeller_protocol", autospec=True
        )

        await modeller._modeller_run(modeller_mailbox=mock_modeller_mailbox)

        # Check task response processing was called
        mock_modeller_mailbox.process_task_request_responses.assert_awaited_once()
        # Check next stage called
        mock__run_modeller_protocol.assert_awaited_once()

    async def test__modeller_run_fails_fast_if_no_accepted_pods(
        self,
        caplog: LogCaptureFixture,
        mock_modeller_mailbox: Mock,
        mocker: MockerFixture,
        modeller: Modeller,
    ) -> None:
        """Tests _modeller_run method fails fast if no pods accept."""
        # Set no "accepted" pods
        mock_modeller_mailbox.accepted_worker_mailboxes = {}

        # Mock out next call in chain
        mock__run_modeller_protocol = mocker.patch.object(
            modeller, "_run_modeller_protocol", autospec=True
        )

        result = await modeller._modeller_run(modeller_mailbox=mock_modeller_mailbox)

        # Check false return value
        assert result is False
        # Check error logged out
        error_logs = get_error_logs(caplog)
        assert "No workers with which to train." in error_logs
        # Check next stage NOT called
        mock__run_modeller_protocol.assert_not_called()

    async def test__modeller_run_with_response_handler(
        self,
        mock_modeller_mailbox: Mock,
        mocker: MockerFixture,
        modeller: Modeller,
        pod_identifiers: List[str],
    ) -> None:
        """Tests _modeller_run method when provided with a ResponseHandler."""
        # Set "accepted" pods
        mock_worker_mailboxes = {
            pod_identifier: create_autospec(_WorkerMailboxDetails, instance=True)
            for pod_identifier in pod_identifiers
        }
        mock_modeller_mailbox.accepted_worker_mailboxes = mock_worker_mailboxes

        # Mock out next call in chain
        mock__run_modeller_protocol = mocker.patch.object(
            modeller, "_run_modeller_protocol", autospec=True
        )

        # Create mock ResponseHandler
        mock_response_handler = create_autospec(_ResponseHandler, instance=True)

        await modeller._modeller_run(
            modeller_mailbox=mock_modeller_mailbox,
            response_handler=mock_response_handler,
        )

        # Check task response pre-processing was called
        mock_response_handler.handle.assert_awaited_once()
        # Check task response processing was called
        mock_modeller_mailbox.process_task_request_responses.assert_awaited_once()
        # Check next stage called
        mock__run_modeller_protocol.assert_awaited_once()

    async def test_run_async(
        self,
        mock_modeller_mailbox: Mock,
        mocker: MockerFixture,
        modeller: Modeller,
        pod_identifiers: List[str],
    ) -> None:
        """Tests run_async method performs expected operations."""
        # Mock out task request sending
        mock__send_task_requests = mocker.patch.object(
            modeller,
            "_send_task_requests",
            autospec=True,
            return_value=mock_modeller_mailbox,
        )
        # Mock out next stage call
        mock__modeller_run = mocker.patch.object(
            modeller, "_modeller_run", autospec=True
        )

        result = await modeller.run_async(pod_identifiers)

        # Assert task requests sent
        mock__send_task_requests.assert_awaited_once()
        # Assert next stage called
        mock__modeller_run.assert_awaited_once()
        # Check log message handler removed
        mock_modeller_mailbox.delete_handler.assert_called_once()
        # Check return value
        assert result == mock__modeller_run.return_value

    async def test_run_async_with_saml_handler(
        self,
        mock_modeller_mailbox: Mock,
        mocker: MockerFixture,
        modeller: Modeller,
        pod_identifiers: List[str],
    ) -> None:
        """Test run_async correctly starts SAML challenge handler."""
        # Set SAML identity verification method on modeller
        modeller._identity_verification_method = IdentityVerificationMethod.SAML

        # Mock out task request sending
        mock__send_task_requests = mocker.patch.object(
            modeller,
            "_send_task_requests",
            autospec=True,
            return_value=mock_modeller_mailbox,
        )
        # Mock out next stage call
        mock__modeller_run = mocker.patch.object(
            modeller, "_modeller_run", autospec=True
        )

        # Mock out SAML servers
        mock_saml_handler_cls = mocker.patch(
            "bitfount.federated.modeller._SAMLChallengeHandler", autospec=True
        )
        mock_saml_handler = mock_saml_handler_cls.return_value

        result = await modeller.run_async(pod_identifiers)

        # Assert SAML server running
        mock_saml_handler.start.assert_awaited_once()

        # Assert task requests sent
        mock__send_task_requests.assert_awaited_once()
        # Assert next stage called
        mock__modeller_run.assert_awaited_once()
        # Check log message handler removed
        mock_modeller_mailbox.delete_handler.assert_called_once()
        # Check return value
        assert result == mock__modeller_run.return_value

    async def test_run_async_with_oidc_auth_flow_handler(
        self,
        caplog: LogCaptureFixture,
        mock_modeller_mailbox: Mock,
        mocker: MockerFixture,
        modeller: Modeller,
        pod_identifiers: List[str],
    ) -> None:
        """Test run_async correctly starts OIDC auth code challenge handler."""
        # Set OIDC identity verification method on modeller
        modeller._identity_verification_method = (
            IdentityVerificationMethod.OIDC_ACF_PKCE
        )

        # Mock out task request sending
        mock__send_task_requests = mocker.patch.object(
            modeller,
            "_send_task_requests",
            autospec=True,
            return_value=mock_modeller_mailbox,
        )
        # Mock out next stage call
        mock__modeller_run = mocker.patch.object(
            modeller, "_modeller_run", autospec=True
        )

        # Mock out environment retrieval
        fake_auth_env = _AuthEnv(
            name="auth_env_name",
            auth_domain="auth_env_auth_domain",
            client_id="auth_env_client_id",
        )
        mocker.patch(
            "bitfount.federated.modeller._get_auth_environment",
            autospec=True,
            return_value=fake_auth_env,
        )

        # Mock out OIDC server
        mock_oidc_handler_cls = mocker.patch(
            "bitfount.federated.modeller._OIDCAuthFlowChallengeHandler", autospec=True
        )
        mock_oidc_handler = mock_oidc_handler_cls.return_value

        with caplog.at_level(logging.DEBUG):
            result = await modeller.run_async(pod_identifiers)

        # Assert OIDC server running
        mock_oidc_handler.start.assert_awaited_once()
        # Check OIDC server constructed correctly
        mock_oidc_handler_cls.assert_called_once_with(
            auth_domain=fake_auth_env.auth_domain
        )
        # Check logs output
        debug_logs = get_debug_logs(caplog)
        assert (
            f"Setting up OIDC Authorization Code Flow challenge listener against "
            f"{fake_auth_env.name} authorization environment." in debug_logs
        )

        # Assert task requests sent
        mock__send_task_requests.assert_awaited_once()
        # Assert next stage called
        mock__modeller_run.assert_awaited_once()
        # Check log message handler removed
        mock_modeller_mailbox.delete_handler.assert_called_once()
        # Check return value
        assert result == mock__modeller_run.return_value

    async def test_run_async_with_oidc_device_code_handler(
        self,
        mock_modeller_mailbox: Mock,
        mocker: MockerFixture,
        modeller: Modeller,
        pod_identifiers: List[str],
    ) -> None:
        """Test run_async correctly starts OIDC device code challenge handler."""
        # Set OIDC identity verification method on modeller
        modeller._identity_verification_method = (
            IdentityVerificationMethod.OIDC_DEVICE_CODE
        )

        # Mock out task request sending
        mock__send_task_requests = mocker.patch.object(
            modeller,
            "_send_task_requests",
            autospec=True,
            return_value=mock_modeller_mailbox,
        )
        # Mock out next stage call
        mock__modeller_run = mocker.patch.object(
            modeller, "_modeller_run", autospec=True
        )

        # Mock out environment retrieval
        fake_auth_env = _AuthEnv(
            name="auth_env_name",
            auth_domain="auth_env_auth_domain",
            client_id="auth_env_client_id",
        )
        mocker.patch(
            "bitfount.federated.modeller._get_auth_environment",
            autospec=True,
            return_value=fake_auth_env,
        )

        # Mock out OIDC Device Code init
        mock_oidc_handler_cls = mocker.patch(
            "bitfount.federated.modeller._OIDCDeviceCodeHandler", autospec=True
        )

        result = await modeller.run_async(pod_identifiers)

        # Check OIDC handler constructed correctly
        mock_oidc_handler_cls.assert_called_once_with(
            auth_domain=fake_auth_env.auth_domain
        )

        # Assert task requests sent
        mock__send_task_requests.assert_awaited_once()
        # Assert next stage called
        mock__modeller_run.assert_awaited_once()
        # Check log message handler removed
        mock_modeller_mailbox.delete_handler.assert_called_once()
        # Check return value
        assert result == mock__modeller_run.return_value

    def test__get_task_request_msg_gen_key_based(
        self, mock_private_key: Mock, mocker: MockerFixture, modeller: Modeller
    ) -> None:
        """Test request message generator creation for key-based authentication."""
        # Guarantee private key and key-based on modeller
        modeller._private_key = mock_private_key
        modeller._identity_verification_method = IdentityVerificationMethod.KEYS

        # Wrap mock around authorisation checker class
        wrapped_creator = mocker.patch.object(
            _SignatureBasedAuthorisation,
            "create_task_request_message_generator",
            wraps=_SignatureBasedAuthorisation.create_task_request_message_generator,
        )

        msg_gen = modeller._get_task_request_msg_gen()

        # Check called with key
        wrapped_creator.assert_called_once_with(mock_private_key)
        # Check returned gen
        assert isinstance(msg_gen, _TaskRequestMessageGenerator)

    def test__get_task_request_msg_gen_key_based_fails_no_key(
        self,
        modeller: Modeller,
    ) -> None:
        """Test message generator creation failure for key-based authentication.

        Will fail if no key provided.
        """
        # Guarantee NO private key and key-based on modeller
        modeller._private_key = None
        modeller._identity_verification_method = IdentityVerificationMethod.KEYS

        with pytest.raises(
            ValueError,
            match=re.escape(
                "Signature-based identification selected but no private key provided."
            ),
        ):
            modeller._get_task_request_msg_gen()

    def test__get_task_request_msg_gen_saml_based(
        self,
        mocker: MockerFixture,
        modeller: Modeller,
    ) -> None:
        """Test request message generator creation for key-based authentication."""
        # Guarantee SAML-based on modeller
        modeller._identity_verification_method = IdentityVerificationMethod.SAML

        # Wrap mock around authorisation checker class
        wrapped_creator = mocker.patch.object(
            _SAMLAuthorisation,
            "create_task_request_message_generator",
            wraps=_SAMLAuthorisation.create_task_request_message_generator,
        )

        msg_gen = modeller._get_task_request_msg_gen()

        # Check called with key
        wrapped_creator.assert_called_once()
        # Check returned gen
        assert isinstance(msg_gen, _TaskRequestMessageGenerator)
