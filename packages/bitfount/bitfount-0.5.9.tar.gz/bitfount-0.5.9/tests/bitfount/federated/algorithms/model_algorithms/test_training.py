"""Tests for the federated model training algorithm."""
from typing import TYPE_CHECKING
from unittest.mock import Mock, create_autospec

from pytest_mock import MockerFixture

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
from bitfount.federated.algorithms.model_algorithms.federated_training import (
    FederatedModelTraining,
    _BaseModelTrainingMixIn,
    _ModellerSide,
    _WorkerSide,
)
from bitfount.hub import BitfountHub
from tests.utils.helper import unit_test


class TestFederatedModelTraining:
    """Test Federated Model Training algorithm."""

    @unit_test
    def test_modeller(self, model: Mock) -> None:
        """Test modeller method."""
        algorithm_factory = FederatedModelTraining(model=model)
        algorithm = algorithm_factory.modeller()
        for type_ in [
            _BaseAlgorithm,
            _BaseModellerAlgorithm,
            _BaseModelAlgorithm,
            _BaseModellerModelAlgorithm,
        ]:
            assert isinstance(algorithm, type_)
        assert algorithm.steps == 10

    @unit_test
    def test_worker(self, model: Mock) -> None:
        """Test worker method."""
        algorithm_factory = FederatedModelTraining(model=model)
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
        assert algorithm.steps == 10

    @unit_test
    def test_modeller_logs_validation_metrics(
        self, mocker: MockerFixture, model: Mock
    ) -> None:
        """Test that the validation metrics are logged for the modeller."""
        mocker.patch.object(
            _BaseModelTrainingMixIn,
            "get_param_states",
            return_value={"layer1": [0, 1, 2, 3]},
        )
        mock_model_log = Mock()
        mocker.patch.object(model, "log_", mock_model_log)

        algorithm_factory = FederatedModelTraining(model=model)
        algorithm = algorithm_factory.modeller()

        algorithm.run(validation_metrics={"AUC": 0.8})
        mock_model_log.assert_called()


# Static tests for algorithm-protocol compatibility
if TYPE_CHECKING:
    from typing import cast

    from bitfount.federated.protocols.fed_avg import (
        _FederatedAveragingCompatibleAlgoFactory,
        _FederatedAveragingCompatibleModeller,
        _FederatedAveragingCompatibleWorker,
    )
    from bitfount.types import (
        DistributedModelProtocol,
        _DistributedModelTypeOrReference,
    )

    # Check compatible with FederatedAveraging
    _algo_factory: _FederatedAveragingCompatibleAlgoFactory = FederatedModelTraining(
        model=cast(_DistributedModelTypeOrReference, object())
    )
    _modeller_side: _FederatedAveragingCompatibleModeller = _ModellerSide(
        model=cast(DistributedModelProtocol, object())
    )
    _worker_side: _FederatedAveragingCompatibleWorker = _WorkerSide(
        model=cast(DistributedModelProtocol, object())
    )
