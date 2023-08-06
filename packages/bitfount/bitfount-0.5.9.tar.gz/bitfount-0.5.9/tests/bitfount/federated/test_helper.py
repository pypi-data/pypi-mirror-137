"""Tests federated helper.py."""
from typing import Optional, cast
from unittest.mock import Mock, create_autospec

from _pytest.logging import LogCaptureFixture
import pytest
from pytest import fixture
from pytest_lazyfixture import lazy_fixture
from pytest_mock import MockerFixture

from bitfount.data.schema import BitfountSchema
from bitfount.federated.aggregators.aggregator import Aggregator
from bitfount.federated.aggregators.secure import SecureAggregator
from bitfount.federated.algorithms.model_algorithms.federated_training import (
    FederatedModelTraining,
)
from bitfount.federated.helper import (
    _create_aggregator,
    _create_and_connect_pod_mailbox,
    _create_federated_averaging_protocol_factory,
    _create_message_service,
)
from bitfount.federated.protocols.fed_avg import FederatedAveraging
from bitfount.federated.transport.config import (
    _DEV_MESSAGE_SERVICE_PORT,
    _DEV_MESSAGE_SERVICE_TLS,
    _DEV_MESSAGE_SERVICE_URL,
    _STAGING_MESSAGE_SERVICE_URL,
    PRODUCTION_MESSAGE_SERVICE_URL,
    MessageServiceConfig,
)
from bitfount.federated.transport.message_service import _MessageService
from bitfount.federated.transport.pod_transport import _PodMailbox
from bitfount.hub.authentication_flow import BitfountSession
from tests.utils.helper import create_schema, get_warning_logs, unit_test


@unit_test
class TestHelperFunctions:
    """Test federated helper functions."""

    @fixture
    def test_url(self) -> str:
        """Test URL."""
        return "not.a.real.url.com"

    @fixture
    def schema(self) -> BitfountSchema:
        """Creates a schema fixture."""
        return create_schema(classification=True)

    def test_create_insecure_aggregator_successfully(self) -> None:
        """Tests create_aggregator function without secure aggregation."""
        model = Mock()  # Mock() is inherently instance of DistributedModelProtocol
        aggregator = _create_aggregator(model=model, secure_aggregation=False)
        assert isinstance(aggregator, Aggregator)
        assert not isinstance(aggregator, SecureAggregator)

    def test_create_secure_aggregator_successfully(self) -> None:
        """Tests create_aggregator function with secure aggregation."""
        model = Mock()  # Mock() is inherently instance of DistributedModelProtocol
        aggregator = _create_aggregator(model=model, secure_aggregation=True)
        assert isinstance(aggregator, SecureAggregator)

    @pytest.mark.parametrize(
        "environment, expected_config, input_config",
        [
            (
                "production",
                MessageServiceConfig(url=PRODUCTION_MESSAGE_SERVICE_URL),
                None,
            ),
            ("staging", MessageServiceConfig(url=_STAGING_MESSAGE_SERVICE_URL), None),
            (
                "dev",
                MessageServiceConfig(
                    url=_DEV_MESSAGE_SERVICE_URL,
                    port=_DEV_MESSAGE_SERVICE_PORT,
                    tls=_DEV_MESSAGE_SERVICE_TLS,
                ),
                None,
            ),
            (
                None,
                MessageServiceConfig(url=cast(str, lazy_fixture("test_url"))),
                MessageServiceConfig(url=cast(str, lazy_fixture("test_url"))),
            ),
        ],
        indirect=["environment"],
    )
    def test_create_message_service_successfully(
        self,
        environment: None,
        expected_config: MessageServiceConfig,
        input_config: Optional[MessageServiceConfig],
    ) -> None:
        """Tests create_message_service method works.

        Ensures correct config is passed through to the created message service.
        """
        message_service = _create_message_service(
            session=create_autospec(BitfountSession, instance=True),
            ms_config=input_config,
        )
        assert isinstance(message_service, _MessageService)
        assert message_service.config == expected_config

    def test_create_message_service_issues_warning_for_local_storage(
        self, caplog: LogCaptureFixture
    ) -> None:
        """Tests create_message_service issues warning if using local storage."""
        ms_config = MessageServiceConfig(use_local_storage=True)
        message_service = _create_message_service(
            session=create_autospec(BitfountSession, instance=True),
            ms_config=ms_config,
        )
        assert isinstance(message_service, _MessageService)

        # Check for warning message; should be thing logged
        warning_logs = get_warning_logs(caplog)
        assert (
            "Messages will contain local file references. "
            "Ensure all pods have access to your local file system. "
            "Otherwise your task will hang." in warning_logs
        )

    async def test_create_and_connect_pod_mailbox_successfully(
        self, mocker: MockerFixture
    ) -> None:
        """Tests create_and_connect_pod_mailbox method works."""
        # We know that `create_message_service` is already tested so we mock out
        # its response and check it is called correctly.
        mock_create_message_service = mocker.patch(
            "bitfount.federated.helper._create_message_service"
        )

        # We also need to mock out the PodMailbox.connect_pod() class method.
        mock_connect_pod = mocker.patch.object(
            _PodMailbox, "connect_pod", autospec=True
        )
        mock_connect_pod.return_value = create_autospec(_PodMailbox, instance=True)

        # Create mocks for args we don't care about
        pod_name = "not-a-real-pod"
        mock_session = create_autospec(BitfountSession, instance=True)
        mock_ms_config = create_autospec(MessageServiceConfig, instance=True)

        mailbox = await _create_and_connect_pod_mailbox(
            pod_name=pod_name,
            session=mock_session,
            ms_config=mock_ms_config,
        )

        assert isinstance(mailbox, _PodMailbox)
        mock_connect_pod.assert_called_once_with(
            pod_name=pod_name, message_service=mock_create_message_service()
        )

    @pytest.mark.parametrize("secure_aggregation", [True, False])
    def test_create_federated_averaging_protocol_factory_successfully(
        self, schema: BitfountSchema, secure_aggregation: bool
    ) -> None:
        """Tests that create_federated_averaging_protocol_factory works as expected."""
        model = Mock(epochs=1)

        algorithm = FederatedModelTraining(model=model)

        aggregator = _create_aggregator(
            model=algorithm.model, secure_aggregation=secure_aggregation
        )
        protocol = _create_federated_averaging_protocol_factory(
            protocol_cls=FederatedAveraging,
            algorithm=algorithm,
            aggregator=aggregator,
            steps_between_parameter_updates=None,
            epochs_between_parameter_updates=2,
            auto_eval=False,
        )
        assert isinstance(protocol, FederatedAveraging)
        assert protocol.epochs_between_parameter_updates == 2
        assert protocol.steps_between_parameter_updates is None

    @pytest.mark.parametrize("secure_aggregation", [True, False])
    def test_create_federated_averaging_protocol_factory_iterations_not_provided(
        self, schema: BitfountSchema, secure_aggregation: bool
    ) -> None:
        """Tests create_federated_averaging_protocol_factory with no iteration provided.

        Tests that iterations is set to a default value if no value is provided.
        """
        model = Mock(epochs=1)
        algorithm = FederatedModelTraining(model=model)
        aggregator = _create_aggregator(
            model=algorithm.model, secure_aggregation=secure_aggregation
        )
        protocol = _create_federated_averaging_protocol_factory(
            protocol_cls=FederatedAveraging,
            algorithm=algorithm,
            aggregator=aggregator,
            steps_between_parameter_updates=None,
            epochs_between_parameter_updates=None,
            auto_eval=False,
        )
        assert isinstance(protocol, FederatedAveraging)
        assert protocol.steps_between_parameter_updates == 1
        assert protocol.epochs_between_parameter_updates is None
