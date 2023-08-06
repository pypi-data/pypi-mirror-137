"""Test worker can communicate with modeller."""
import asyncio
from collections import namedtuple
from datetime import datetime, timezone
import re
from typing import Callable, Dict, Iterable, List
from unittest.mock import ANY, Mock, call, create_autospec

from grpc import RpcError
import msgpack
import pytest
from pytest import fixture, raises
from pytest_mock import MockerFixture

from bitfount.federated.transport.base_transport import (
    MessageRetrievalError,
    _run_func_and_listen_to_mailbox,
)
from bitfount.federated.transport.message_service import (
    _BitfountMessage,
    _BitfountMessageType,
    _MessageEncryption,
    _MessageService,
)
from bitfount.federated.transport.protos.messages_pb2 import SuccessResponse
from bitfount.federated.transport.worker_transport import (
    _send_secure_shares_to_others,
    _WorkerMailbox,
)
from bitfount.federated.types import _PodResponseType
from tests.utils.fixtures import MessageOrException
from tests.utils.helper import unit_test
from tests.utils.mocks import AsyncIteratorMock

WorkerDetails = namedtuple("WorkerDetails", ["pod_identifier", "mailbox_id"])


@fixture
def pod_identifier() -> str:
    """A pod identifier."""
    return "someUser/somePod"


@fixture
def worker_mailbox_id() -> str:
    """A mailbox ID for the worker."""
    return "thisWorkersMailboxID"


@fixture
def modeller_mailbox_id() -> str:
    """The mailbox ID for the modeller."""
    return "someModellerMailboxId"


@fixture
def modeller_name() -> str:
    """The name of the modeller."""
    return "someModeller"


@fixture
def aes_key() -> bytes:
    """The AES key to use in message encryption between worker and modeller."""
    return b"SecretAESKey"


@fixture
def mock_message_service() -> Mock:
    """Mock message service."""
    mock_message_service: Mock = create_autospec(_MessageService, instance=True)
    return mock_message_service


@fixture
def other_pod_details() -> List[WorkerDetails]:
    """Details of the other pods involved in the task."""
    return [
        WorkerDetails("user/differentpod", "someMailboxID2"),
        WorkerDetails("another/pod", "someMailboxID3"),
    ]


@fixture
def pod_mailbox_ids(
    other_pod_details: List[WorkerDetails], pod_identifier: str, worker_mailbox_id: str
) -> Dict[str, str]:
    """A mapping of pod identifier to mailbox ID for all task workers.

    This includes the worker itself.
    """
    return {
        pod_identifier: worker_mailbox_id,
        other_pod_details[0].pod_identifier: other_pod_details[0].mailbox_id,
        other_pod_details[1].pod_identifier: other_pod_details[1].mailbox_id,
    }


@fixture
def worker_mailbox(
    aes_key: bytes,
    mock_message_service: Mock,
    modeller_mailbox_id: str,
    modeller_name: str,
    pod_identifier: str,
    pod_mailbox_ids: Dict[str, str],
) -> _WorkerMailbox:
    """A WorkerMailbox instance with components mocked out."""
    return _WorkerMailbox(
        pod_identifier=pod_identifier,
        modeller_mailbox_id=modeller_mailbox_id,
        modeller_name=modeller_name,
        aes_encryption_key=aes_key,
        message_service=mock_message_service,
        pod_mailbox_ids=pod_mailbox_ids,
    )


@unit_test
class TestWorkerMailbox:
    """Test WorkerMailbox class."""

    async def test__send_aes_encrypted_message_successful(
        self,
        aes_key: bytes,
        mock_message_service: Mock,
        mock_message_timestamps: Callable[[Iterable[str]], Mock],
        mocker: MockerFixture,
        modeller_mailbox_id: str,
        modeller_name: str,
        pod_identifier: str,
        worker_mailbox: _WorkerMailbox,
        worker_mailbox_id: str,
    ) -> None:
        """Message is sent AES encrypted using provided key."""
        fake_timestamps = ["Hello"]
        mock_message_timestamps(fake_timestamps)

        expected_encrypted_message: bytes = b"encrypted_message"
        encrypt = mocker.patch.object(_MessageEncryption, "encrypt_outgoing_message")
        encrypt.return_value = expected_encrypted_message

        message = "some message"
        dumped_message = msgpack.dumps(message)

        await worker_mailbox._send_aes_encrypted_message(
            message, _BitfountMessageType.TRAINING_UPDATE
        )

        encrypt.assert_called_once_with(dumped_message, aes_key)
        mock_message_service.send_message.assert_called_once_with(
            _BitfountMessage(
                message_type=_BitfountMessageType.TRAINING_UPDATE,
                body=expected_encrypted_message,
                recipient=modeller_name,
                recipient_mailbox_id=modeller_mailbox_id,
                sender=pod_identifier,
                sender_mailbox_id=worker_mailbox_id,
                timestamp=fake_timestamps[0],
            ),
            already_packed=True,
        )

    async def test__send_aes_encrypted_message_throws_error(
        self,
        aes_key: bytes,
        mock_message_service: Mock,
        mock_message_timestamps: Callable[[Iterable[str]], Mock],
        mocker: MockerFixture,
        modeller_mailbox_id: str,
        modeller_name: str,
        pod_identifier: str,
        worker_mailbox: _WorkerMailbox,
        worker_mailbox_id: str,
    ) -> None:
        """Sending encrypted message receives RpcError."""
        fake_timestamps = ["Hello"]
        mock_message_timestamps(fake_timestamps)

        expected_encrypted_message: bytes = b"encrypted_message"
        encrypt = mocker.patch.object(_MessageEncryption, "encrypt_outgoing_message")
        encrypt.return_value = expected_encrypted_message

        message = "some message"
        dumped_message = msgpack.dumps(message)

        mock_message_service.send_message.side_effect = RpcError()

        with raises(RpcError):
            await worker_mailbox._send_aes_encrypted_message(
                message, _BitfountMessageType.TRAINING_UPDATE
            )

        encrypt.assert_called_once_with(dumped_message, aes_key)
        mock_message_service.send_message.assert_called_once_with(
            _BitfountMessage(
                message_type=_BitfountMessageType.TRAINING_UPDATE,
                body=expected_encrypted_message,
                recipient=modeller_name,
                recipient_mailbox_id=modeller_mailbox_id,
                sender=pod_identifier,
                sender_mailbox_id=worker_mailbox_id,
                timestamp=fake_timestamps[0],
            ),
            already_packed=True,
        )

    async def test__get_message_and_decrypt_successful(
        self,
        aes_key: bytes,
        mock_poll_for_messages: Callable[
            [Iterable[MessageOrException]], AsyncIteratorMock
        ],
        mocker: MockerFixture,
        modeller_mailbox_id: str,
        modeller_name: str,
        pod_identifier: str,
        worker_mailbox: _WorkerMailbox,
        worker_mailbox_id: str,
    ) -> None:
        """Receives and decrypts messages using provided AES key."""
        expected_message = "some message"
        dumped_message: bytes = msgpack.dumps(expected_message)
        # We will be manually mocking out the decryption so this message can just
        # be arbitrary.
        mock_encrypted_message: bytes = b"encrypted_message"

        # Mock out decryption
        decrypt = mocker.patch.object(_MessageEncryption, "decrypt_incoming_message")
        decrypt.return_value = dumped_message

        # Set up the mocked messages to be received
        mock_poll_for_messages(
            [
                _BitfountMessage(
                    message_type=_BitfountMessageType.TRAINING_UPDATE,
                    body=mock_encrypted_message,
                    recipient=modeller_name,
                    recipient_mailbox_id=modeller_mailbox_id,
                    sender=pod_identifier,
                    sender_mailbox_id=worker_mailbox_id,
                )
            ]
        )

        # Start listening and processing messages
        message = await _run_func_and_listen_to_mailbox(
            worker_mailbox._get_message_and_decrypt(
                _BitfountMessageType.TRAINING_UPDATE
            ),
            worker_mailbox,
        )

        assert message == expected_message
        decrypt.assert_called_once_with(mock_encrypted_message, aes_key)

    async def test__get_message_and_decrypt_error_never_receives_message(
        self,
        mock_poll_for_messages: Callable[
            [Iterable[MessageOrException]], AsyncIteratorMock
        ],
        worker_mailbox: _WorkerMailbox,
    ) -> None:
        """Never receives message using provided AES key."""
        # Use empty list to indicate no message scenario
        mock_poll_for_messages([])

        with raises(asyncio.TimeoutError):
            # Start listening and processing (non-existent) messages. We will
            # timeout on the responses to simulate what happens when no message
            # is received.
            await _run_func_and_listen_to_mailbox(
                worker_mailbox._get_message_and_decrypt(
                    _BitfountMessageType.TRAINING_UPDATE,  # this is arbitrary
                    timeout=1,
                ),
                worker_mailbox,
            )

    async def test__get_message_and_decrypt_error(
        self,
        mock_poll_for_messages: Callable[
            [Iterable[MessageOrException]], AsyncIteratorMock
        ],
        rpc_error: RpcError,
        worker_mailbox: _WorkerMailbox,
    ) -> None:
        """Receiving message throws RpcError."""
        mock_poll_for_messages([rpc_error])

        with raises(
            MessageRetrievalError,
            match="An error occurred when trying to communicate with the "
            "messaging service",
        ):
            # Start listening and processing messages
            await _run_func_and_listen_to_mailbox(
                worker_mailbox._get_message_and_decrypt(
                    _BitfountMessageType.TRAINING_UPDATE  # this is arbitrary
                ),
                worker_mailbox,
            )

    async def test_accept_job_successful(
        self,
        mocker: MockerFixture,
        worker_mailbox: _WorkerMailbox,
    ) -> None:
        """Training job acceptance sent."""
        mock_message_send = mocker.patch.object(
            worker_mailbox,
            "_send_aes_encrypted_message",
            return_value=SuccessResponse(),
        )

        await worker_mailbox.accept_task()

        mock_message_send.assert_called_once_with(
            {_PodResponseType.ACCEPT.name: worker_mailbox.pod_identifier},
            _BitfountMessageType.JOB_ACCEPT,
        )

    async def test_accept_job_unsuccessful(
        self,
        mocker: MockerFixture,
        worker_mailbox: _WorkerMailbox,
    ) -> None:
        """Sending training job acceptance fails."""
        mock_message_send = mocker.patch.object(
            worker_mailbox, "_send_aes_encrypted_message", side_effect=RpcError()
        )

        with pytest.raises(RpcError):
            await worker_mailbox.accept_task()

        mock_message_send.assert_called_once_with(
            {_PodResponseType.ACCEPT.name: worker_mailbox.pod_identifier},
            _BitfountMessageType.JOB_ACCEPT,
        )

    async def test_reject_job_successful(
        self,
        mocker: MockerFixture,
        worker_mailbox: _WorkerMailbox,
    ) -> None:
        """Training job rejection sent."""
        expected_error_messages = {"error": "messages"}
        mock_message_send = mocker.patch.object(
            worker_mailbox,
            "_send_aes_encrypted_message",
            return_value=SuccessResponse(),
        )

        await worker_mailbox.reject_task(
            expected_error_messages,
        )

        mock_message_send.assert_called_once_with(
            expected_error_messages,
            _BitfountMessageType.JOB_REJECT,
        )

    async def test_reject_job_unsuccessful(
        self,
        mocker: MockerFixture,
        worker_mailbox: _WorkerMailbox,
    ) -> None:
        """Sending training job rejection fails."""
        expected_error_messages = {"error": "messages"}
        mock_message_send = mocker.patch.object(
            worker_mailbox, "_send_aes_encrypted_message", side_effect=RpcError()
        )

        with pytest.raises(RpcError):
            await worker_mailbox.reject_task(
                expected_error_messages,
            )

        mock_message_send.assert_called_once_with(
            expected_error_messages,
            _BitfountMessageType.JOB_REJECT,
        )

    async def test_issue_saml_challenge_successful(
        self,
        mocker: MockerFixture,
        worker_mailbox: _WorkerMailbox,
    ) -> None:
        """Training SAML challenge sent."""
        expected_saml_request = "some saml request"
        mock_message_send = mocker.patch.object(
            worker_mailbox,
            "_send_aes_encrypted_message",
            return_value=SuccessResponse(),
        )

        await worker_mailbox.issue_saml_challenge(
            expected_saml_request,
        )

        mock_message_send.assert_called_once_with(
            expected_saml_request,
            _BitfountMessageType.SAML_REQUEST,
        )

    async def test_issue_saml_challenge_unsuccessful(
        self,
        mocker: MockerFixture,
        worker_mailbox: _WorkerMailbox,
    ) -> None:
        """Sending SAML challenge fails."""
        expected_saml_request = "some saml request"
        mock_message_send = mocker.patch.object(
            worker_mailbox, "_send_aes_encrypted_message", side_effect=RpcError()
        )

        with pytest.raises(RpcError):
            await worker_mailbox.issue_saml_challenge(
                expected_saml_request,
            )

        mock_message_send.assert_called_once_with(
            expected_saml_request,
            _BitfountMessageType.SAML_REQUEST,
        )

    async def test_get_saml_response(
        self,
        mocker: MockerFixture,
        worker_mailbox: _WorkerMailbox,
    ) -> None:
        """SAML challenge response retrieved."""
        expected_saml_response = "some saml response"
        mock_message_decrypt = mocker.patch.object(
            worker_mailbox,
            "_get_message_and_decrypt",
            return_value=expected_saml_response,
        )

        response = await worker_mailbox.get_saml_response()

        assert response == expected_saml_response
        mock_message_decrypt.assert_awaited_once_with(
            _BitfountMessageType.SAML_RESPONSE, None
        )

    async def test_get_task_complete_response(
        self,
        mocker: MockerFixture,
        worker_mailbox: _WorkerMailbox,
    ) -> None:
        """Tests worker gets task complete empty message ."""
        mock_message_decrypt = mocker.patch.object(
            worker_mailbox,
            "_get_message_and_decrypt",
            return_value=None,
        )

        await worker_mailbox.get_task_complete_update()
        mock_message_decrypt.assert_awaited_once_with(
            _BitfountMessageType.TASK_COMPLETE, timeout=None
        )

    async def test_get_training_complete_update(
        self,
        mocker: MockerFixture,
        worker_mailbox: _WorkerMailbox,
    ) -> None:
        """Tests worker gets task complete empty message ."""
        expected_message = True
        mock_message_decrypt = mocker.patch.object(
            worker_mailbox,
            "_get_message_and_decrypt",
            return_value=expected_message,
        )

        response = await worker_mailbox.get_training_iteration_complete_update()
        assert response == expected_message
        mock_message_decrypt.assert_awaited_once_with(
            _BitfountMessageType.TRAINING_COMPLETE, timeout=None
        )

    async def test_send_oidc_client_id(
        self,
        mocker: MockerFixture,
        worker_mailbox: _WorkerMailbox,
    ) -> None:
        """Test send_oidc_client_id() works correctly."""
        # Patch out _WorkerMailbox._send_aes_encrypted_message()
        mock_message_send = mocker.patch.object(
            worker_mailbox,
            "_send_aes_encrypted_message",
            return_value=SuccessResponse(),
        )

        client_id = "client_id_value"

        await worker_mailbox.send_oidc_client_id(client_id)

        # Check called correctly
        mock_message_send.assert_called_once_with(
            {"client_id": client_id},
            _BitfountMessageType.OIDC_CHALLENGE,
        )

    async def test_get_oidc_auth_flow_response(
        self,
        mocker: MockerFixture,
        worker_mailbox: _WorkerMailbox,
    ) -> None:
        """Tests get_oidc_auth_flow_response() correctly extracts details."""
        expected_message = {
            "auth_code": "auth_code_value",
            "code_verifier": "code_verifier_value",
            "redirect_uri": "redirect_uri_value",
        }

        # Patch out _WorkerMailbox._get_message_and_decrypt()
        mock_message_decrypt = mocker.patch.object(
            worker_mailbox,
            "_get_message_and_decrypt",
            return_value=expected_message,
        )

        response = await worker_mailbox.get_oidc_auth_flow_response()

        # Check calls/returns
        mock_message_decrypt.assert_awaited_once_with(
            _BitfountMessageType.OIDC_AFC_PKCE_RESPONSE, ANY
        )
        assert response.auth_code == expected_message["auth_code"]
        assert response.code_verifier == expected_message["code_verifier"]
        assert response.redirect_uri == expected_message["redirect_uri"]

    async def test_get_oidc_auth_flow_response_fails_wrong_type(
        self,
        mocker: MockerFixture,
        worker_mailbox: _WorkerMailbox,
    ) -> None:
        """Tests get_oidc_auth_flow_response() fails with wrong type."""
        expected_message = "not a dict"

        # Patch out _WorkerMailbox._get_message_and_decrypt()
        mock_message_decrypt = mocker.patch.object(
            worker_mailbox,
            "_get_message_and_decrypt",
            return_value=expected_message,
        )

        with pytest.raises(
            TypeError,
            match=re.escape(
                f"Unable to access OIDC response contents; "
                f"expected dict, got {type(expected_message)}"
            ),
        ):
            await worker_mailbox.get_oidc_auth_flow_response()

        # Check calls/returns
        mock_message_decrypt.assert_awaited_once_with(
            _BitfountMessageType.OIDC_AFC_PKCE_RESPONSE, ANY
        )

    @pytest.mark.parametrize(
        "key_to_drop", ("auth_code", "code_verifier", "redirect_uri")
    )
    async def test_get_oidc_auth_flow_response_fails_missing_key(
        self,
        key_to_drop: str,
        mocker: MockerFixture,
        worker_mailbox: _WorkerMailbox,
    ) -> None:
        """Tests get_oidc_auth_flow_response() fails with missing key."""
        expected_message = {
            "auth_code": "auth_code_value",
            "code_verifier": "code_verifier_value",
            "redirect_uri": "redirect_uri_value",
        }
        expected_message.pop(key_to_drop)

        # Patch out _WorkerMailbox._get_message_and_decrypt()
        mock_message_decrypt = mocker.patch.object(
            worker_mailbox,
            "_get_message_and_decrypt",
            return_value=expected_message,
        )

        with pytest.raises(
            KeyError,
            match=re.escape(
                f"Expected auth_code, code_verifier, and redirect_uri to be in "
                f"OIDC response; got {expected_message.keys()}"
            ),
        ):
            await worker_mailbox.get_oidc_auth_flow_response()

        # Check calls/returns
        mock_message_decrypt.assert_awaited_once_with(
            _BitfountMessageType.OIDC_AFC_PKCE_RESPONSE, ANY
        )

    async def test_get_oidc_device_code_response(
        self,
        mocker: MockerFixture,
        worker_mailbox: _WorkerMailbox,
    ) -> None:
        """Tests get_oidc_device_code_response() correctly extracts details."""
        now = datetime.now(timezone.utc)
        expected_message = {
            "device_code": "someDeviceCode",
            "expires_at": now.isoformat(),
            "interval": 5,
        }

        # Patch out _WorkerMailbox._get_message_and_decrypt()
        mock_message_decrypt = mocker.patch.object(
            worker_mailbox,
            "_get_message_and_decrypt",
            return_value=expected_message,
        )

        response = await worker_mailbox.get_oidc_device_code_response()

        # Check calls/returns
        mock_message_decrypt.assert_awaited_once_with(
            _BitfountMessageType.OIDC_DEVICE_CODE_RESPONSE, ANY
        )
        assert response.device_code == expected_message["device_code"]
        assert response.expires_at == now
        assert response.interval == 5

    async def test_get_oidc_device_code_response_fails_wrong_type(
        self,
        mocker: MockerFixture,
        worker_mailbox: _WorkerMailbox,
    ) -> None:
        """Tests get_oidc_device_code_response() fails with wrong type."""
        expected_message = "not a dict"

        # Patch out _WorkerMailbox._get_message_and_decrypt()
        mock_message_decrypt = mocker.patch.object(
            worker_mailbox,
            "_get_message_and_decrypt",
            return_value=expected_message,
        )

        with pytest.raises(
            TypeError,
            match=re.escape(
                f"Unable to access OIDC response contents; "
                f"expected dict, got {type(expected_message)}"
            ),
        ):
            await worker_mailbox.get_oidc_device_code_response()

        # Check calls/returns
        mock_message_decrypt.assert_awaited_once_with(
            _BitfountMessageType.OIDC_DEVICE_CODE_RESPONSE, ANY
        )

    @pytest.mark.parametrize(
        "key_to_drop",
        ("device_code", "expires_at", "interval"),
    )
    async def test_get_oidc_device_code_response_fails_missing_key(
        self,
        key_to_drop: str,
        mocker: MockerFixture,
        worker_mailbox: _WorkerMailbox,
    ) -> None:
        """Tests get_oidc_device_code_response() fails with missing key."""
        now = datetime.now(timezone.utc)
        expected_message = {
            "device_code": "someDeviceCode",
            "expires_at": now.isoformat(),
            "interval": 5,
        }
        expected_message.pop(key_to_drop)

        # Patch out _WorkerMailbox._get_message_and_decrypt()
        mock_message_decrypt = mocker.patch.object(
            worker_mailbox,
            "_get_message_and_decrypt",
            return_value=expected_message,
        )

        with pytest.raises(
            KeyError,
            match=re.escape(
                f"Expected device_code, expires_at, and interval to be in "
                f"OIDC response; got {expected_message.keys()}"
            ),
        ):
            await worker_mailbox.get_oidc_device_code_response()

        # Check calls/returns
        mock_message_decrypt.assert_awaited_once_with(
            _BitfountMessageType.OIDC_DEVICE_CODE_RESPONSE, ANY
        )


@unit_test
class TestWorkerTransportFunctions:
    """Test the other functions not contained within WorkerMailbox."""

    async def test_send_to_pods_sends_message(
        self,
        mock_message_service: Mock,
        mock_message_timestamps: Callable[[Iterable[str]], Mock],
        other_pod_details: List[WorkerDetails],
        pod_identifier: str,
        worker_mailbox: _WorkerMailbox,
        worker_mailbox_id: str,
    ) -> None:
        """Tests send_secure_shares_to_others method works correctly.

        Asserts each pod receives their own message generated by secure_share_generator.
        """
        fake_timestamps = ["Hello", "World"]
        mock_message_timestamps(fake_timestamps)

        mock_message_service.send_message.return_value = SuccessResponse()

        class DummySecureShare:
            def __init__(self) -> None:
                self.counter = 0

            def message_body_generator(self) -> int:
                self.counter += 1
                return self.counter

        sec = DummySecureShare()

        await _send_secure_shares_to_others(
            sec.message_body_generator,
            worker_mailbox,
        )

        # Call count is pods in `pod_mailbox_ids`
        # excluding this pod as it doesnt send to itself
        assert mock_message_service.send_message.call_count == 2
        mock_message_service.send_message.assert_has_calls(
            [
                call(
                    _BitfountMessage(
                        message_type=_BitfountMessageType.SECURE_SHARE,
                        body=msgpack.dumps(1),
                        recipient=other_pod_details[0].pod_identifier,
                        recipient_mailbox_id=other_pod_details[0].mailbox_id,
                        sender=pod_identifier,
                        sender_mailbox_id=worker_mailbox_id,
                        timestamp=fake_timestamps[0],
                    ),
                    already_packed=True,
                ),
                call(
                    _BitfountMessage(
                        message_type=_BitfountMessageType.SECURE_SHARE,
                        body=msgpack.dumps(2),
                        recipient=other_pod_details[1].pod_identifier,
                        recipient_mailbox_id=other_pod_details[1].mailbox_id,
                        sender=pod_identifier,
                        sender_mailbox_id=worker_mailbox_id,
                        timestamp=fake_timestamps[1],
                    ),
                    already_packed=True,
                ),
            ]
        )
