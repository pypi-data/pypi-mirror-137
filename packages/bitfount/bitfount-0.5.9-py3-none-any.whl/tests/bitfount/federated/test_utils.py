"""Tests for `bitfount/federated/utils.py`."""
from typing import Any

import pytest

from bitfount.federated.utils import _validate_pod_identifiers
from tests.utils.helper import unit_test


@unit_test
class TestUtils:
    """Tests `bitfount/federated/utils.py` functions."""

    @pytest.mark.parametrize(
        "worker_names, error",
        [
            (["blah"], True),
            (["/blah"], True),
            (["blah/"], True),
            (["bl/a/h"], True),
            ("username/workername", True),
            (["username/workername"], False),
        ],
    )
    def test_validate_worker_names(self, error: bool, worker_names: Any) -> None:
        """Tests `validate_worker_names` works correctly."""
        if error:
            with pytest.raises(ValueError):
                _validate_pod_identifiers(worker_names)

        else:
            # No ValueError raised
            _validate_pod_identifiers(worker_names)
