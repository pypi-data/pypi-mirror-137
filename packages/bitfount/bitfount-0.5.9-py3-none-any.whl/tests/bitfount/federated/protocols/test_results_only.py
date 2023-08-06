"""Tests for the results only protocol."""
import re
from typing import Callable
from unittest.mock import Mock, create_autospec

import pytest
from pytest import fixture
from pytest_mock import MockerFixture

from bitfount.data import DataSource
from bitfount.federated.algorithms.model_algorithms.train_and_evaluate import (
    ModelTrainingAndEvaluation,
)
from bitfount.federated.protocols import results_only
from bitfount.federated.protocols.base import (
    _BaseModellerProtocol,
    _BaseProtocol,
    _BaseWorkerProtocol,
)
from bitfount.federated.protocols.results_only import (
    ResultsOnly,
    _ResultsOnlyCompatibleAlgoFactory_,
    _ResultsOnlyCompatibleModelAlgoFactory,
    _ResultsOnlyDataCompatibleWorker,
    _ResultsOnlyDataIncompatibleWorker,
    _WorkerSide,
)
from bitfount.federated.transport.worker_transport import _WorkerMailbox
from tests.utils.helper import unit_test


@unit_test
class TestWorkerSide:
    """Tests worker-side of ResultsOnly."""

    @fixture
    def mock_datasource(self) -> Mock:
        """Mock DataSource."""
        mock_datasource: Mock = create_autospec(DataSource, instance=True)
        return mock_datasource

    @fixture
    def mock_mailbox(self) -> Mock:
        """Mock WorkerMailbox."""
        mock_mailbox: Mock = create_autospec(_WorkerMailbox, instance=True)
        return mock_mailbox

    @fixture
    def worker_side_factory(self, mock_mailbox: Mock) -> Callable[[Mock], _WorkerSide]:
        """Factory to create WorkerSide instances from mock algorithms."""

        def _create(algo: Mock) -> _WorkerSide:
            return _WorkerSide(
                algorithm=algo,
                mailbox=mock_mailbox,
            )

        return _create

    async def test_run_with_data_algo(
        self,
        mock_datasource: Mock,
        mock_mailbox: Mock,
        worker_side_factory: Callable[[Mock], _WorkerSide],
    ) -> None:
        """Tests WorkerSide.run() with an algorithm needing data."""
        mock_data_algorithm: Mock = create_autospec(
            _ResultsOnlyDataCompatibleWorker, instance=True
        )
        worker_side: _WorkerSide = worker_side_factory(mock_data_algorithm)

        await worker_side.run(mock_datasource)

        mock_data_algorithm.run.assert_called_once_with(data=mock_datasource)
        mock_mailbox.send_evaluation_results.assert_awaited_once_with(
            mock_data_algorithm.run.return_value
        )
        mock_mailbox.get_task_complete_update.assert_called_once()

    async def test_run_with_non_data_algo(
        self,
        mock_datasource: Mock,
        mock_mailbox: Mock,
        worker_side_factory: Callable[[Mock], _WorkerSide],
    ) -> None:
        """Tests WorkerSide.run() with an algorithm not needing data."""
        mock_algorithm: Mock = create_autospec(
            _ResultsOnlyDataIncompatibleWorker, instance=True
        )
        worker_side: _WorkerSide = worker_side_factory(mock_algorithm)

        await worker_side.run(mock_datasource)

        mock_algorithm.run.assert_called_once_with()
        mock_mailbox.send_evaluation_results.assert_awaited_once_with(
            mock_algorithm.run.return_value
        )


@unit_test
class TestResultsOnly:
    """Test Results Only protocol."""

    @fixture
    def remote_algorithm(self) -> ModelTrainingAndEvaluation:
        """Returns remote algorithm."""
        return ModelTrainingAndEvaluation(model=Mock())

    def test_modeller(
        self, mock_modeller_mailbox: Mock, remote_algorithm: ModelTrainingAndEvaluation
    ) -> None:
        """Test modeller method."""
        protocol_factory = ResultsOnly(algorithm=remote_algorithm)
        protocol = protocol_factory.modeller(mailbox=mock_modeller_mailbox)
        for type_ in [
            _BaseProtocol,
            _BaseModellerProtocol,
            results_only._ModellerSide,
        ]:
            assert isinstance(protocol, type_)

    def test_worker(
        self,
        mock_hub: Mock,
        mock_worker_mailbox: Mock,
        remote_algorithm: ModelTrainingAndEvaluation,
    ) -> None:
        """Test worker method."""
        protocol_factory = ResultsOnly(algorithm=remote_algorithm)
        protocol = protocol_factory.worker(mailbox=mock_worker_mailbox, hub=mock_hub)
        for type_ in [
            _BaseProtocol,
            _BaseWorkerProtocol,
            results_only._WorkerSide,
        ]:
            assert isinstance(protocol, type_)

    def test__validate_algorithm_accepts(self) -> None:
        """Tests _validate_algorithm accepts compatible."""
        # Test with ResultsOnlyCompatibleAlgoFactory
        mock_algorithm: Mock = create_autospec(
            _ResultsOnlyCompatibleAlgoFactory_, instance=True
        )
        ResultsOnly._validate_algorithm(mock_algorithm)

        # Test with ResultsOnlyCompatibleModelAlgoFactory
        mock_algorithm = create_autospec(
            _ResultsOnlyCompatibleModelAlgoFactory, instance=True
        )
        ResultsOnly._validate_algorithm(mock_algorithm)

    def test__validate_algorithm_rejects(self) -> None:
        """Tests _validate_algorithm rejects incompatible."""
        mock_algorithm: Mock = Mock(spec_set=["__name__"])
        with pytest.raises(
            TypeError,
            match=re.escape(
                f"The {ResultsOnly.__name__} protocol does not "
                f"support the {type(mock_algorithm).__name__} algorithm."
            ),
        ):
            ResultsOnly._validate_algorithm(mock_algorithm)

    def test_dump_works_with_model_based_algorithm(self, mocker: MockerFixture) -> None:
        """Tests dump() works with model-algorithm schemas."""
        mock_get_schema = mocker.patch.object(ResultsOnly, "get_schema", autospec=True)
        mock_algorithm: Mock = create_autospec(
            _ResultsOnlyCompatibleModelAlgoFactory, instance=True
        )

        results_only = ResultsOnly(algorithm=mock_algorithm)
        dumped = results_only.dump()

        # Check dumped value is the value from get_schema
        assert dumped == mock_get_schema.return_value.dump.return_value
        # Check schema was generated with the right args
        mock_algorithm.get_schema.assert_called_once_with(
            model_schema=mock_algorithm.model_schema
        )
        mock_get_schema.assert_called_once_with(mock_algorithm.get_schema.return_value)
