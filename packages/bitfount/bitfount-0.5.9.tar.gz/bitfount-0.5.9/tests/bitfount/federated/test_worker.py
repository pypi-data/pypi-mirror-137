"""Tests worker.py."""
import re
from typing import Any, cast
from unittest.mock import AsyncMock, Mock, create_autospec

from _pytest.logging import LogCaptureFixture
from _pytest.monkeypatch import MonkeyPatch
import pytest
from pytest import fixture
from pytest_mock import MockerFixture

from bitfount.federated.aggregators.base import _BaseAggregatorFactory
from bitfount.federated.aggregators.base import _registry as aggregator_registry
from bitfount.federated.algorithms.base import (
    _BaseAlgorithmFactory,
    _BaseAlgorithmSchema,
)
from bitfount.federated.algorithms.base import _registry as algorithm_registry
from bitfount.federated.algorithms.model_algorithms.base import (
    _BaseModelAlgorithmSchema,
)
from bitfount.federated.authorisation_checkers import (
    _AuthorisationChecker,
    _LocalAuthorisation,
)
from bitfount.federated.protocols.base import _BaseProtocolFactory
from bitfount.federated.protocols.base import _registry as protocol_registry
from bitfount.federated.protocols.fed_avg import FederatedAveraging
from bitfount.federated.task_requests import _ProtocolDetails
from bitfount.federated.utils import _DISTRIBUTED_MODELS
from bitfount.federated.worker import _Worker
from bitfount.types import DistributedModelProtocol, _JSONDict
from tests.utils.helper import unit_test


@unit_test
class TestWorker:
    """Tests Worker class."""

    @fixture
    def dummy_protocol(self) -> FederatedAveraging:
        """Returns a FederatedAveraging instance."""
        protocol = Mock(algorithm=Mock(), aggregator=Mock())
        protocol.name = "FederatedAveraging"
        protocol.algorithm.name = "FederatedModelTraining"
        protocol.aggregator.name = "Aggregator"
        return protocol

    @fixture
    def authoriser(self) -> _AuthorisationChecker:
        """An AuthorisationChecker object.

        An instance of LocalAuthorisation is returned because AuthorisationChecker
        cannot itself be instantiated.
        """
        return _LocalAuthorisation(
            Mock(),
            _ProtocolDetails(
                "bitfount.FederatedAveraging",
                "bitfount.FederatedModelTraining",
                aggregator="bitfount.SecureAggregator",
            ),
        )

    async def test_unverified_protocol_aborts_task(
        self,
        authoriser: _AuthorisationChecker,
        caplog: LogCaptureFixture,
        dummy_protocol: FederatedAveraging,
        mocker: MockerFixture,
    ) -> None:
        """Tests that an unverified protocol from the Modeller aborts the task.

        The authoriser expects the aggregator to be Secure but the protocol that is
        received actually uses the insecure aggregator. Thus we expect the task to
        be aborted.
        """
        caplog.set_level("INFO")
        mocker.patch.object(
            authoriser, "check_authorisation", return_value=Mock(messages=None)
        )
        worker = _Worker(Mock(), AsyncMock(), Mock(), authoriser)
        mocker.patch.object(worker, "_get_protocol", return_value=dummy_protocol)

        await worker.run()

        assert len(caplog.records) == 3

        for i, record in enumerate(caplog.records):

            if i == 0:
                assert record.levelname == "INFO"
                assert record.msg == "Task accepted, informing modeller."

            elif i == 1:
                assert record.levelname == "ERROR"
                assert (
                    record.msg == "Aggregator Aggregator does not match "
                    "bitfount.SecureAggregator"
                )
            elif i == 2:
                assert record.levelname == "ERROR"
                assert (
                    record.msg == "The protocol that has been received does not match "
                    "the original protocol that was authorised and accepted. "
                    "Aborting task."
                )
            else:
                pytest.fail("Unexpected log level.")

    @fixture
    def mock_aggregator_cls_name(self) -> str:
        """Registry name for mock aggregator class."""
        return "mock_aggregator_cls"

    @fixture
    def mock_aggregator_cls_in_registry(
        self, mock_aggregator_cls_name: str, monkeypatch: MonkeyPatch
    ) -> Mock:
        """Places mock aggregator class in relevant registry."""
        mock_aggregator_cls: Mock = create_autospec(_BaseAggregatorFactory)
        # cast() needed as mypy cannot infer type correctly for MonkeyPatch.setitem()
        monkeypatch.setitem(
            aggregator_registry,
            mock_aggregator_cls_name,
            cast(Any, mock_aggregator_cls),
        )
        return mock_aggregator_cls

    @fixture
    def mock_algorithm_cls_name(self) -> str:
        """Registry name for mock algorithm class."""
        return "mock_algorithm_cls"

    @fixture
    def mock_algorithm_cls_in_registry(
        self, mock_algorithm_cls_name: str, monkeypatch: MonkeyPatch
    ) -> Mock:
        """Places mock algorithm class in relevant registry."""
        mock_algorithm_cls: Mock = create_autospec(_BaseAlgorithmFactory)
        # cast() needed as mypy cannot infer type correctly for MonkeyPatch.setitem()
        monkeypatch.setitem(
            algorithm_registry, mock_algorithm_cls_name, cast(Any, mock_algorithm_cls)
        )
        return mock_algorithm_cls

    @fixture
    def mock_model_cls_name(self) -> str:
        """Registry name for mock model class."""
        return "mock_model_cls"

    @fixture
    def mock_model_cls_in_registry(
        self, mock_model_cls_name: str, monkeypatch: MonkeyPatch
    ) -> Mock:
        """Places mock model class in relevant registry."""
        mock_model_cls: Mock = create_autospec(DistributedModelProtocol)
        mock_model_cls.Schema = Mock()
        # cast() needed as mypy cannot infer type correctly for MonkeyPatch.setitem()
        monkeypatch.setitem(
            _DISTRIBUTED_MODELS, mock_model_cls_name, cast(Any, mock_model_cls)
        )
        return mock_model_cls

    @fixture
    def mock_protocol_cls_name(self) -> str:
        """Registry name for mock protocol class."""
        return "mock_protocol_cls"

    @fixture
    def mock_protocol_cls_in_registry(
        self, mock_protocol_cls_name: str, monkeypatch: MonkeyPatch
    ) -> Mock:
        """Places mock protocol class in relevant registry."""
        mock_protocol_cls: Mock = create_autospec(_BaseProtocolFactory)
        # cast() needed as mypy cannot infer type correctly for MonkeyPatch.setitem()
        monkeypatch.setitem(
            protocol_registry, mock_protocol_cls_name, cast(Any, mock_protocol_cls)
        )
        return mock_protocol_cls

    @fixture
    def serialized_protocol_modelless(
        self, mock_algorithm_cls_name: str, mock_protocol_cls_name: str
    ) -> _JSONDict:
        """Serialized protocol dict without model."""
        return {
            "algorithm": {
                "name": mock_algorithm_cls_name,
            },
            "name": mock_protocol_cls_name,
        }

    @fixture
    def serialized_protocol_with_model(
        self,
        mock_aggregator_cls_name: str,
        mock_algorithm_cls_name: str,
        mock_model_cls_name: str,
        mock_protocol_cls_name: str,
    ) -> _JSONDict:
        """Serialized protocol dict with model (and aggregator)."""
        return {
            "algorithm": {
                "name": mock_algorithm_cls_name,
                "model": {"name": mock_model_cls_name},
            },
            "aggregator": {"name": mock_aggregator_cls_name},
            "name": mock_protocol_cls_name,
        }

    @fixture
    def mock_worker(self) -> Mock:
        """Mock Worker instance to use in `self` arg."""
        mock_worker = Mock(spec=_Worker, hub=Mock())
        return mock_worker

    def test__deserialize_protocol_with_modelless_algo(
        self,
        mock_algorithm_cls_in_registry: Mock,
        mock_protocol_cls_in_registry: Mock,
        mock_worker: Mock,
        mocker: MockerFixture,
        monkeypatch: MonkeyPatch,
        serialized_protocol_modelless: _JSONDict,
    ) -> None:
        """Test _deserialize_protocol works with modelless algorithm."""
        # Patch with BaseAlgorithmSchema style get_schema
        mock_algorithm_cls_in_registry.get_schema = create_autospec(
            _BaseAlgorithmSchema.get_schema
        )

        # Difficult to handle issubclass checks with mocks; easiest way is to just
        # patch the builtin directly
        mocker.patch("bitfount.federated.worker.issubclass", return_value=True)

        _Worker._deserialize_protocol(
            self=mock_worker, serialized_protocol=serialized_protocol_modelless
        )

        # Check protocol/schema calls as expected
        mock_algorithm_cls_in_registry.get_schema.assert_called_once_with()
        mock_protocol_cls_in_registry.load.assert_called_once_with(
            serialized_protocol=serialized_protocol_modelless,
            algorithm_schema=mock_algorithm_cls_in_registry.get_schema.return_value,
            aggregator_schema=None,
        )

    def test__deserialize_protocol_with_model_algo(
        self,
        mock_aggregator_cls_in_registry: Mock,
        mock_algorithm_cls_in_registry: Mock,
        mock_model_cls_in_registry: Mock,
        mock_protocol_cls_in_registry: Mock,
        mock_worker: Mock,
        mocker: MockerFixture,
        monkeypatch: MonkeyPatch,
        serialized_protocol_with_model: _JSONDict,
    ) -> None:
        """Test _deserialize_protocol works with model algorithm."""
        # Patch with BaseModelAlgorithmSchema style get_schema
        mock_algorithm_cls_in_registry.get_schema = create_autospec(
            _BaseModelAlgorithmSchema.get_schema
        )

        # Difficult to handle issubclass checks with mocks; easiest way is to just
        # patch the builtin directly. Need to fail first check, pass second.
        mocker.patch("bitfount.federated.worker.issubclass", side_effect=[False, True])

        _Worker._deserialize_protocol(
            self=mock_worker, serialized_protocol=serialized_protocol_with_model
        )

        # Check protocol/schema calls as expected
        mock_algorithm_cls_in_registry.get_schema.assert_called_once_with(
            model_schema=mock_model_cls_in_registry.get_schema()
        )
        mock_protocol_cls_in_registry.load.assert_called_once_with(
            serialized_protocol=serialized_protocol_with_model,
            algorithm_schema=mock_algorithm_cls_in_registry.get_schema.return_value,
            aggregator_schema=mock_aggregator_cls_in_registry.get_schema.return_value,
        )

    def test__deserialize_protocol_fails_with_model_algo_but_no_model(
        self,
        mock_algorithm_cls_in_registry: Mock,
        mock_protocol_cls_in_registry: Mock,
        mock_worker: Mock,
        mocker: MockerFixture,
        monkeypatch: MonkeyPatch,
        serialized_protocol_modelless: _JSONDict,
    ) -> None:
        """Test _deserialize_protocol fails with model algorithm but no model."""
        # Patch with BaseModelAlgorithmSchema style get_schema
        mock_algorithm_cls_in_registry.get_schema = create_autospec(
            _BaseModelAlgorithmSchema.get_schema
        )

        # Difficult to handle issubclass checks with mocks; easiest way is to just
        # patch the builtin directly. Need to fail first check, pass second.
        mocker.patch("bitfount.federated.worker.issubclass", side_effect=[False, True])

        with pytest.raises(
            TypeError,
            match=re.escape(
                f"Chosen algorithm ({mock_algorithm_cls_in_registry}) is a model "
                f"algorithm, but no model schema was specified"
            ),
        ):
            _Worker._deserialize_protocol(
                self=mock_worker, serialized_protocol=serialized_protocol_modelless
            )

    def test__deserialize_protocol_fails_if_algo_schema_style_not_supported(
        self,
        mock_algorithm_cls_in_registry: Mock,
        mock_protocol_cls_in_registry: Mock,
        mock_worker: Mock,
        mocker: MockerFixture,
        monkeypatch: MonkeyPatch,
        serialized_protocol_modelless: _JSONDict,
    ) -> None:
        """Test _deserialize_protocol fails with unknown algorithm schema style."""
        # Difficult to handle issubclass checks with mocks; easiest way is to just
        # patch the builtin directly. Need to fail all checks.
        mocker.patch("bitfount.federated.worker.issubclass", return_value=False)

        with pytest.raises(
            AttributeError,
            match=re.escape(
                f"Algorithm class {mock_algorithm_cls_in_registry} does not "
                f"implement get_schema()"
            ),
        ):
            _Worker._deserialize_protocol(
                self=mock_worker, serialized_protocol=serialized_protocol_modelless
            )
