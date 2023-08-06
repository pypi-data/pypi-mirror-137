"""Tests base protocols module."""
from pathlib import Path
from typing import cast
from unittest.mock import Mock

import pytest
from pytest_mock import MockerFixture

from bitfount.federated.algorithms.column_avg import ColumnAverage
from bitfount.federated.protocols.base import _BaseProtocolFactory, _run_protocol
from bitfount.federated.protocols.results_only import ResultsOnly
from tests.utils.helper import unit_test


@unit_test
def test_run_protocol(mocker: MockerFixture) -> None:
    """Tests we can run a protocol."""
    algorithm = ColumnAverage(field="TARGET")

    # Mock out Modeller creation
    mock_modeller = mocker.patch(
        "bitfount.federated.protocols.base.Modeller", autospec=True
    )
    mock_modeller.return_value = mock_modeller  # for __init__
    mock_modeller.run.return_value = None

    protocol = ResultsOnly(algorithm=algorithm)

    _run_protocol(
        protocol=protocol,
        pod_identifiers=["fake/fake"],
        hub=Mock(),
        message_service=Mock(),
        private_key_or_file=Path("fake.pem"),
        idp_url="https://idp-url.unit-test.bitfount.com",
    )

    mock_modeller.run.assert_called_once_with(["fake/fake"])


@unit_test
def test_load() -> None:
    """Test BaseProtocolFactory.load() works."""
    # Get unbound classmethod for ease of testing
    load_classmethod = cast(classmethod, _BaseProtocolFactory.load).__func__

    mock_serialized_protocol = Mock()

    # Test with a cls with `get_schema`
    mock_cls = Mock(spec_set=["get_schema"])
    loaded = load_classmethod(mock_cls, mock_serialized_protocol)
    assert loaded == mock_cls.get_schema.return_value.load.return_value
    mock_cls.get_schema.return_value.load.assert_called_once_with(
        mock_serialized_protocol
    )

    # Test with a cls with no `get_schema`
    with pytest.raises(
        AttributeError, match="Chosen protocol class does not implement get_schema"
    ):
        mock_cls = Mock(spec_set=[])
        load_classmethod(mock_cls, mock_serialized_protocol)
