"""Tests for the model evaluation algorithm."""
from typing import TYPE_CHECKING
from unittest.mock import Mock, create_autospec

from marshmallow import Schema as MarshmallowSchema
from pytest_mock import MockerFixture

from bitfount.federated.algorithms.base import (
    _BaseAlgorithm,
    _BaseModellerAlgorithm,
    _BaseWorkerAlgorithm,
)
from bitfount.federated.algorithms.model_algorithms import evaluate
from bitfount.federated.algorithms.model_algorithms.base import (
    _BaseModelAlgorithm,
    _BaseModellerModelAlgorithm,
    _BaseWorkerModelAlgorithm,
)
from bitfount.federated.algorithms.model_algorithms.evaluate import (
    ModelEvaluation,
    _ModellerSide,
    _WorkerSide,
)
from bitfount.hub import BitfountHub
from tests.utils.helper import unit_test


class TestModelEvaluation:
    """Test Evaluate algorithm."""

    @unit_test
    def test_modeller_types(self, model: Mock) -> None:
        """Test modeller method."""
        algorithm_factory = ModelEvaluation(model=model)
        algorithm = algorithm_factory.modeller()
        for type_ in [
            _BaseAlgorithm,
            _BaseModellerAlgorithm,
            _BaseModelAlgorithm,
            _BaseModellerModelAlgorithm,
        ]:
            assert isinstance(algorithm, type_)

    @unit_test
    def test_worker_types(self, model: Mock) -> None:
        """Test worker method."""
        algorithm_factory = ModelEvaluation(model=model)
        algorithm = algorithm_factory.worker(
            hub=create_autospec(BitfountHub, instance=True)
        )
        for type_ in [
            _BaseAlgorithm,
            _BaseWorkerAlgorithm,
            _BaseModelAlgorithm,
            _BaseWorkerModelAlgorithm,
        ]:
            assert isinstance(algorithm, type_)

    @unit_test
    def test_worker_run(self, mocker: MockerFixture, model: Mock) -> None:
        """Tests that worker run does metric calculation."""
        worker = evaluate._WorkerSide(model=model)
        mock_metrics = Mock()
        mocker.patch(
            "bitfount.metrics.MetricCollection.create_from_model", mock_metrics
        )
        worker.run()
        mock_metrics.assert_called_once()

    @unit_test
    def test_modeller_run(self, model: Mock) -> None:
        """Tests that modeller run returns results."""
        modeller = evaluate._ModellerSide(model=model)
        results = [{"AUC": 0.5}]
        assert results == modeller.run(results=results)

    @unit_test
    def test_schema(self, model: Mock) -> None:
        """Tests that schema returns parent class."""
        schema_cls = ModelEvaluation.get_schema(create_autospec(MarshmallowSchema))
        schema = schema_cls()
        factory = schema.recreate_factory(data={"model": model})  # type: ignore[attr-defined]  # Reason: test will fail if wrong type  # noqa: B950
        assert isinstance(factory, ModelEvaluation)


# Static tests for algorithm-protocol compatibility
if TYPE_CHECKING:
    from typing import cast

    from bitfount.federated.protocols.results_only import (
        _ResultsOnlyCompatibleModelAlgoFactory,
        _ResultsOnlyCompatibleModeller,
        _ResultsOnlyDataIncompatibleWorker,
    )
    from bitfount.types import (
        DistributedModelProtocol,
        _DistributedModelTypeOrReference,
    )

    # Check compatible with ResultsOnly
    _algo_factory: _ResultsOnlyCompatibleModelAlgoFactory = ModelEvaluation(
        model=cast(_DistributedModelTypeOrReference, object())
    )
    _modeller_side: _ResultsOnlyCompatibleModeller = _ModellerSide(
        model=cast(DistributedModelProtocol, object())
    )
    _worker_side: _ResultsOnlyDataIncompatibleWorker = _WorkerSide(
        model=cast(DistributedModelProtocol, object())
    )
