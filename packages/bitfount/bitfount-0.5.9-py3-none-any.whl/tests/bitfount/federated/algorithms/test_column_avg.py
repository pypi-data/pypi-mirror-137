"""Tests for the column averaging algorithm."""
from typing import TYPE_CHECKING

from bitfount.federated.algorithms.base import (
    _BaseAlgorithm,
    _BaseModellerAlgorithm,
    _BaseWorkerAlgorithm,
)
from bitfount.federated.algorithms.column_avg import (
    ColumnAverage,
    _ModellerSide,
    _WorkerSide,
)
from tests.utils.helper import unit_test


class TestColumnAverage:
    """Test ColumnAverage algorithm."""

    @unit_test
    def test_modeller(self) -> None:
        """Test modeller method."""
        algorithm_factory = ColumnAverage(field="TARGET")
        algorithm = algorithm_factory.modeller()
        for type_ in [_BaseAlgorithm, _BaseModellerAlgorithm]:
            assert isinstance(algorithm, type_)

    @unit_test
    def test_worker(self) -> None:
        """Test worker method."""
        algorithm_factory = ColumnAverage(field="TARGET")
        algorithm = algorithm_factory.worker()
        for type_ in [_BaseAlgorithm, _BaseWorkerAlgorithm]:
            assert isinstance(algorithm, type_)


# Static tests for algorithm-protocol compatibility
if TYPE_CHECKING:
    from typing import cast

    from bitfount.federated.protocols.results_only import (
        _ResultsOnlyCompatibleAlgoFactory_,
        _ResultsOnlyCompatibleModeller,
        _ResultsOnlyDataIncompatibleWorker,
    )

    # Check compatible with ResultsOnly
    _algo_factory: _ResultsOnlyCompatibleAlgoFactory_ = ColumnAverage(
        field=cast(str, object())
    )
    _modeller_side: _ResultsOnlyCompatibleModeller = _ModellerSide()
    _worker_side: _ResultsOnlyDataIncompatibleWorker = _WorkerSide(
        field=cast(str, object())
    )
