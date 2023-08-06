"""Tests for data utils classes and methods."""
import hashlib
from typing import cast
from unittest.mock import MagicMock

from pytest import fixture

from bitfount.data.helper import convert_epochs_to_steps
from bitfount.data.utils import _generate_dataframe_hash, _hash_str
from bitfount.types import _DataFrameLib, _DataFrameType, _PandasLikeModule
from bitfount.utils import _get_df_library
from tests.utils import PytestRequest
from tests.utils.helper import unit_test


@unit_test
def test_convert_epochs_to_steps() -> None:
    """Test converting of epochs to steps is correct."""
    dataloader = MagicMock()
    dataloader.__len__.return_value = 100
    steps = convert_epochs_to_steps(5, dataloader)
    assert steps == 100 * 5


@unit_test
class TestDataFrameHashing:
    """Tests for generate_dataframe_hash()."""

    @fixture(params=[_DataFrameLib.PANDAS, _DataFrameLib.KOALAS])
    def dataframe_lib(self, request: PytestRequest) -> _PandasLikeModule:
        """Parameterised fixture to get each dataframe library.

        Parameterised to pandas and databricks.koalas.
        """
        df_lib_type: _DataFrameLib = request.param
        return _get_df_library(df_lib_type)

    @fixture
    def dataframe(self, dataframe_lib: _PandasLikeModule) -> _DataFrameType:
        """A test dataframe with data."""
        return dataframe_lib.DataFrame(data={"test": [1, 2, 3]})

    @fixture
    def dataframe_hash(self, dataframe_lib: _PandasLikeModule) -> str:
        """The expected hash for the dataframe fixture."""
        # The hash is on the DataFrame.dtypes (which returns a Series), so we
        # manually construct the expected matching one.
        series = dataframe_lib.Series(data={"test": "int64"})
        str_rep: str = cast(str, series.to_string())
        return hashlib.sha256(str_rep.encode("utf8")).hexdigest()

    @fixture
    def empty_dataframe(self, dataframe_lib: _PandasLikeModule) -> _DataFrameType:
        """A test dataframe with no data."""
        return dataframe_lib.DataFrame(data={})

    @fixture
    def empty_dataframe_hash(self, dataframe_lib: _PandasLikeModule) -> str:
        """The expected hash of an empty dataframe."""
        # The hash is on the DataFrame.dtypes (which returns a Series), so we
        # manually construct the expected matching one.
        empty_series = dataframe_lib.Series(data={})
        str_rep: str = cast(str, empty_series.to_string())
        return hashlib.sha256(str_rep.encode("utf8")).hexdigest()

    def test_generate_dataframe_hash(
        self, dataframe: _DataFrameType, dataframe_hash: str
    ) -> None:
        """Tests generated hash is expected one for non-empty dataframe."""
        assert _generate_dataframe_hash(dataframe) == dataframe_hash

    def test_generate_dataframe_hash_empty_dataframe(
        self, empty_dataframe: _DataFrameType, empty_dataframe_hash: str
    ) -> None:
        """Tests generated hash is expected one for empty dataframe."""
        assert _generate_dataframe_hash(empty_dataframe) == empty_dataframe_hash

    def test_generate_dataframe_hash_same_for_same_dataframes(
        self, dataframe: _DataFrameType, dataframe_hash: str
    ) -> None:
        """Tests generated hash is consistent for two dataframes with same cols."""
        dataframe_2 = dataframe.copy(deep=True)

        # Check they are different instances
        assert dataframe is not dataframe_2
        # Check hashes match
        assert (
            _generate_dataframe_hash(dataframe)
            == _generate_dataframe_hash(dataframe_2)
            == dataframe_hash
        )

    def test_generate_dataframe_hash_different_for_different_dtype_dataframes(
        self, dataframe: _DataFrameType, dataframe_hash: str
    ) -> None:
        """Tests hash is different for two dataframes with diff col dtypes."""
        dataframe_2 = dataframe.copy(deep=True)
        # Change the column dtype from int64 to string
        dataframe_2 = dataframe_2.astype({"test": "string"})

        # Check they are different instances
        assert dataframe is not dataframe_2
        # Check hashes differ
        assert (
            _generate_dataframe_hash(dataframe)
            != _generate_dataframe_hash(dataframe_2)
            != dataframe_hash
        )


@unit_test
def test_hash_str() -> None:
    """Tests that hash_str() works."""
    test_string = "Hello, world!"
    expected_hash = "315f5bdb76d078c43b8ac0064e4a0164612b1fce77c869345bfc94c75894edd3"
    assert _hash_str(test_string) == expected_hash
