"""Tests Aggregator."""
from typing import List, cast
from unittest.mock import Mock, create_autospec

import numpy as np
from pytest import fixture

from bitfount.federated.aggregators.aggregator import (
    Aggregator,
    _ModellerSide,
    _WorkerSide,
)
from bitfount.federated.aggregators.base import _BaseAggregator
from bitfount.federated.shim import BackendTensorShim
from bitfount.types import _SerializedWeights, _TensorLike
from tests.bitfount.federated.aggregators.util import assert_equal_weight_dicts
from tests.utils.helper import unit_test


@fixture
def tensor_shim() -> Mock:
    """Returns mock tensor_shim."""
    mock_tensor_shim: Mock = create_autospec(BackendTensorShim)
    mock_tensor_shim.to_list.side_effect = lambda x: x.tolist()
    mock_tensor_shim.to_tensor.side_effect = lambda x, dtype: np.asarray(x, dtype)
    return mock_tensor_shim


@unit_test
class TestModellerSide:
    """Test Aggregator ModellerSide."""

    @fixture
    def modeller_side(self, tensor_shim: Mock) -> _ModellerSide:
        """Create ModellerSide for tests."""
        return _ModellerSide(tensor_shim=tensor_shim)

    def test_run(self, modeller_side: _ModellerSide) -> None:
        """Test run method."""
        parameter_updates: List[_SerializedWeights] = [
            {"hello": [1.0, 1.0, 1.0], "world": [2.0, 2.0, 2.0]},
            {"hello": [2.0, 2.0, 2.0], "world": [3.0, 3.0, 3.0]},
        ]
        average = modeller_side.run(parameter_updates=parameter_updates)

        expected_result = {
            "hello": np.asarray([1.5, 1.5, 1.5]),
            "world": np.asarray([2.5, 2.5, 2.5]),
        }
        assert_equal_weight_dicts(average, expected_result)


@unit_test
class TestWorkerSide:
    """Test Aggregator WorkerSide."""

    @fixture
    def worker_side(self, tensor_shim: Mock) -> _WorkerSide:
        """Create WorkerSide for tests."""
        return _WorkerSide(tensor_shim=tensor_shim)

    async def test_run(self, worker_side: _WorkerSide) -> None:
        """Test run method."""
        parameter_update = {"hello": [1, 1, 1], "world": [2, 2, 2]}
        output = await worker_side.run(
            {
                key: cast(_TensorLike, np.asarray(value))
                for key, value in parameter_update.items()
            }
        )
        assert output == parameter_update


@unit_test
class TestAggregator:
    """Test Aggregator."""

    def test_modeller(self, tensor_shim: Mock) -> None:
        """Test modeller method."""
        aggregator_factory = Aggregator(tensor_shim=tensor_shim)
        aggregator = aggregator_factory.modeller()
        for type_ in [_BaseAggregator, _ModellerSide]:
            assert isinstance(aggregator, type_)

    def test_worker(self, tensor_shim: Mock) -> None:
        """Test worker method."""
        aggregator_factory = Aggregator(tensor_shim=tensor_shim)
        aggregator = aggregator_factory.worker()
        for type_ in [_BaseAggregator, _WorkerSide]:
            assert isinstance(aggregator, type_)
