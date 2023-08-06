"""Utility functions for aggregator tests."""
from typing import Mapping, Union

import numpy as np
from numpy.testing import assert_array_equal

from bitfount.types import _WeightMapping


def assert_equal_weight_dicts(
    a: Union[_WeightMapping, Mapping[str, np.ndarray]],
    b: Union[_WeightMapping, Mapping[str, np.ndarray]],
) -> None:
    """Checks if two WeightDicts are equal.

    Check keys match and array values match.
    """
    # Check keys
    assert a.keys() == b.keys()
    # Check arrays
    for key, value in a.items():
        assert_array_equal(np.asarray(value), np.asarray(b[key]))
