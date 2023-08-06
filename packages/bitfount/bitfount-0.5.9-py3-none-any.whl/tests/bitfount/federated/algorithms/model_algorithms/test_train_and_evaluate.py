"""Tests for the model training and evaluation algorithm."""
from typing import TYPE_CHECKING
from unittest.mock import Mock, create_autospec

from bitfount.federated.algorithms.base import (
    _BaseAlgorithm,
    _BaseModellerAlgorithm,
    _BaseWorkerAlgorithm,
)
from bitfount.federated.algorithms.model_algorithms.base import (
    _BaseModelAlgorithm,
    _BaseModellerModelAlgorithm,
    _BaseWorkerModelAlgorithm,
)
from bitfount.federated.algorithms.model_algorithms.train_and_evaluate import (
    ModelTrainingAndEvaluation,
    _ModellerSide,
    _WorkerSide,
)
from bitfount.hub import BitfountHub
from tests.utils.helper import unit_test


class TestModelTrainingAndEvaluation:
    """Test Remote Model Training And Evaluation algorithm."""

    @unit_test
    def test_modeller(self, model: Mock) -> None:
        """Test modeller method."""
        algorithm_factory = ModelTrainingAndEvaluation(model=model)
        algorithm = algorithm_factory.modeller()
        for type_ in [
            _BaseAlgorithm,
            _BaseModellerAlgorithm,
            _BaseModelAlgorithm,
            _BaseModellerModelAlgorithm,
        ]:
            assert isinstance(algorithm, type_)

    @unit_test
    def test_worker(self, model: Mock) -> None:
        """Test worker method."""
        algorithm_factory = ModelTrainingAndEvaluation(model=model)
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


# Static tests for algorithm-protocol compatibility
if TYPE_CHECKING:
    from typing import cast

    from bitfount.federated.protocols.results_only import (
        _ResultsOnlyCompatibleModelAlgoFactory,
        _ResultsOnlyCompatibleModeller,
        _ResultsOnlyDataCompatibleWorker,
    )
    from bitfount.types import (
        DistributedModelProtocol,
        _DistributedModelTypeOrReference,
    )

    # Check compatible with ResultsOnly
    _algo_factory: _ResultsOnlyCompatibleModelAlgoFactory = ModelTrainingAndEvaluation(
        model=cast(_DistributedModelTypeOrReference, object())
    )
    _modeller_side: _ResultsOnlyCompatibleModeller = _ModellerSide(
        model=cast(DistributedModelProtocol, object())
    )
    _worker_side: _ResultsOnlyDataCompatibleWorker = _WorkerSide(
        model=cast(DistributedModelProtocol, object())
    )
