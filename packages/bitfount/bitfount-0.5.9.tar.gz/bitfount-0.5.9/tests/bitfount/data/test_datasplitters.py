"""Tests datasplitters.py."""
from typing import cast

import numpy as np
import pandas
import pytest
from pytest import fixture

from bitfount.data.datasplitters import (
    PercentageSplitter,
    SplitterDefinedInData,
    _DatasetSplitter,
)
from bitfount.types import _DataFrameLib, _DataFrameType
from bitfount.utils import _get_df_library, _get_df_library_type
from tests.utils import PytestRequest
from tests.utils.helper import (
    DATASET_ROW_COUNT,
    create_dataset,
    integration_test,
    unit_test,
)


@fixture
def data(request: PytestRequest) -> _DataFrameType:
    """Returns dataset."""
    return create_dataset(koalas=request.param)


@unit_test
class TestDataSplitter:
    """Tests abstract DataSplitter."""

    @pytest.mark.parametrize(
        "splitter_name",
        [
            PercentageSplitter.splitter_name(),
            # This helps ensure that it can be mapped to
            # from a string in the config file
            # in case we accidentally change the return type
            # Of the class property above
            "percentage",
        ],
    )
    def test_create_produces_percentage_splitter(self, splitter_name: str) -> None:
        """Test Percentage splitter created."""
        created_splitter = _DatasetSplitter.create(splitter_name)
        assert isinstance(created_splitter, PercentageSplitter)

    def test_create_produces_percentage_splitter_with_arguments(self) -> None:
        """Test created percentage splitter has expected values."""
        time_series_sort = ["hello"]

        created_splitter = _DatasetSplitter.create(
            PercentageSplitter.splitter_name(),
            validation_percentage=1,
            test_percentage=2,
            time_series_sort_by=time_series_sort,
        )

        assert isinstance(created_splitter, PercentageSplitter)
        assert created_splitter.validation_percentage == 1
        assert created_splitter.test_percentage == 2
        assert created_splitter.time_series_sort_by == time_series_sort

    @pytest.mark.parametrize(
        "splitter_name",
        [
            SplitterDefinedInData.splitter_name(),
            # This helps ensure that it can be mapped to
            # from a string in the config file
            # in case we accidentally change the return type
            # Of the class property above
            "predefined",
        ],
    )
    def test_create_produces_predefined_splitter(self, splitter_name: str) -> None:
        """Test create predefined splitter."""
        created_splitter = _DatasetSplitter.create(splitter_name)
        assert isinstance(created_splitter, SplitterDefinedInData)

    def test_create_produces_predefined_splitter_with_arguments(self) -> None:
        """Test created predefined splitter has expected values."""
        column_name = "someColumn"
        training_set_label = "UNIT_TRAIN"
        validation_set_label = "UNIT_VALIDATION"
        test_set_label = "UNIT_TEST"

        created_splitter = _DatasetSplitter.create(
            SplitterDefinedInData.splitter_name(),
            column_name=column_name,
            training_set_label=training_set_label,
            validation_set_label=validation_set_label,
            test_set_label=test_set_label,
        )

        assert isinstance(created_splitter, SplitterDefinedInData)
        assert created_splitter.column_name == column_name
        assert created_splitter.training_set_label == training_set_label
        assert created_splitter.validation_set_label == validation_set_label
        assert created_splitter.test_set_label == test_set_label


class TestPercentageSplitter:
    """Tests the Percentage splitter."""

    @pytest.mark.parametrize(
        "data",
        [
            pytest.param(True, marks=integration_test),
            pytest.param(False, marks=unit_test),
        ],
        indirect=["data"],
    )
    @pytest.mark.parametrize("validation_percentage", [0, 7])
    @pytest.mark.parametrize("test_percentage", [0, 7])
    def test_sets_split_by_percentage(
        self, data: _DataFrameType, test_percentage: int, validation_percentage: int
    ) -> None:
        """Test the percentages are as expected."""
        untouched_copy_of_data = data.copy()
        data_splitter = PercentageSplitter(
            validation_percentage=validation_percentage, test_percentage=test_percentage
        )

        (
            train_indices,
            validation_indices,
            test_indices,
        ) = data_splitter.create_dataset_splits(data)

        # Ensure we have the expected number of indices
        assert (
            len(train_indices) + len(validation_indices) + len(test_indices)
            == DATASET_ROW_COUNT
        )
        # Ensure validation and test (and transitively training sets)
        # are the expected sizes
        assert len(validation_indices) == DATASET_ROW_COUNT * (
            validation_percentage / 100
        )
        assert len(test_indices) == DATASET_ROW_COUNT * (test_percentage / 100)

        # Ensure indices are distinct
        # (combines all 3 sets then filters out any duplicates)
        recombined_indices = np.concatenate(
            [train_indices, validation_indices, test_indices]
        )
        unique_indices_returned = np.unique(recombined_indices)
        assert len(unique_indices_returned) == DATASET_ROW_COUNT

        # Ensure we didn't do any sorting
        if _get_df_library_type(data) is _DataFrameLib.KOALAS:
            data = data.to_pandas()
            untouched_copy_of_data = untouched_copy_of_data.to_pandas()
        pandas.testing.assert_frame_equal(data, untouched_copy_of_data)

    @pytest.mark.parametrize(
        "data",
        [
            pytest.param(True, marks=integration_test),
            pytest.param(False, marks=unit_test),
        ],
        indirect=["data"],
    )
    @pytest.mark.parametrize("validation_percentage", [0, 7])
    @pytest.mark.parametrize("test_percentage", [0, 7])
    def test_time_series(
        self, data: _DataFrameType, test_percentage: int, validation_percentage: int
    ) -> None:
        """Checks the time series sorting works correctly."""
        data_frame_library = _get_df_library(data)
        data["Date"] = data_frame_library.to_datetime(
            data["Date"], infer_datetime_format=True
        )
        data = data.reindex(np.random.permutation(data.index.tolist()))

        data_splitter = PercentageSplitter(
            validation_percentage=validation_percentage,
            test_percentage=test_percentage,
            time_series_sort_by="Date",
        )

        (
            train_indices,
            validation_indices,
            test_indices,
        ) = (x.tolist() for x in data_splitter.create_dataset_splits(data))

        # Ensure no overlap of indices between all 3 datasets
        assert not bool(set(train_indices).intersection(validation_indices))
        assert not bool(set(validation_indices).intersection(test_indices))
        assert not bool(set(train_indices).intersection(test_indices))

        if _get_df_library_type(data) is _DataFrameLib.KOALAS:
            data = data.to_pandas()

        train_max = data.loc[train_indices, "Date"].max(skipna=True)
        validation_min = data.loc[validation_indices, "Date"].min(skipna=True)
        validation_max = data.loc[validation_indices, "Date"].max(skipna=True)
        test_min = data.loc[test_indices, "Date"].min(skipna=True)

        # Ensure no overlap of dates between all 3 datasets
        if validation_percentage > 0:
            assert validation_min > train_max

        if test_percentage > 0:
            assert test_min > train_max
            if validation_percentage > 0:
                assert test_min > validation_max

    @pytest.mark.parametrize(
        "data",
        [
            pytest.param(True, marks=integration_test),
            pytest.param(False, marks=unit_test),
        ],
        indirect=["data"],
    )
    def test_time_series_multiple_columns(self, data: _DataFrameType) -> None:
        """Tests time series ordering works when multiple columns are supplied."""
        data_frame_library = _get_df_library(data)
        data["Date"] = data_frame_library.to_datetime(
            data["Date"], infer_datetime_format=True
        )
        data["year"] = data.Date.dt.year
        data["month"] = data.Date.dt.month

        data = data.reindex(np.random.permutation(data.index.tolist()))
        data_splitter = PercentageSplitter(time_series_sort_by=["year", "month"])

        (
            train_indices,
            validation_indices,
            test_indices,
        ) = (x.tolist() for x in data_splitter.create_dataset_splits(data))

        # Ensure no overlap of indices between all 3 datasets
        assert not bool(set(train_indices).intersection(validation_indices))
        assert not bool(set(validation_indices).intersection(test_indices))
        assert not bool(set(train_indices).intersection(test_indices))

        if _get_df_library_type(data) is _DataFrameLib.KOALAS:
            data = data.to_pandas()

        # Train set
        train = data.loc[train_indices]
        train_max_year, train_max_month = train.loc[train["Date"].idxmax()][
            ["year", "month"]
        ]
        # Validation set
        validation = data.loc[validation_indices]
        validation_min_year, validation_min_month = validation.loc[
            validation["Date"].idxmin()
        ][["year", "month"]]
        validation_max_year, validation_max_month = validation.loc[
            validation["Date"].idxmax()
        ][["year", "month"]]
        # Test set
        test = data.loc[test_indices]
        test_min_year, test_min_month = test.loc[test["Date"].idxmin()][
            ["year", "month"]
        ]

        # Ensure no overlap of dates between all 3 datasets
        assert (
            validation_min_year > train_max_year
            or validation_min_month > train_max_month
        )
        assert (
            test_min_year > validation_max_year or test_min_month > validation_max_month
        )


class TestSplitterDefinedInData:
    """Test SplitterDefinedInData."""

    @pytest.mark.parametrize(
        "data",
        [
            pytest.param(True, marks=integration_test),
            pytest.param(False, marks=unit_test),
        ],
        indirect=["data"],
    )
    def test_sets_split(self, data: _DataFrameType) -> None:
        """Test that the specification in the data is respected."""
        data_frame_library = _get_df_library(data)
        # This is a string column that's present in the dataset
        # We can't create a new one in this test because
        # Koalas/Spark doesn't like it...
        data_split_column_name = "L"
        training_set_label = "BF_TRAIN"
        validation_set_label = "BF_VALIDATION"
        test_set_label = "BF_TEST"

        data_split_column = np.random.choice(
            [training_set_label, validation_set_label, test_set_label],
            size=data.shape[0],
        )
        data.update(
            # Because name is set, will be coerced into dataframe
            cast(
                _DataFrameType,
                data_frame_library.Series(
                    data_split_column, name=data_split_column_name
                ),
            )
        )

        data = data.reindex(np.random.permutation(data.index.tolist()))
        data_splitter = SplitterDefinedInData(
            column_name=data_split_column_name,
            training_set_label=training_set_label,
            validation_set_label=validation_set_label,
            test_set_label=test_set_label,
        )

        (
            train_indices,
            validation_indices,
            test_indices,
        ) = data_splitter.create_dataset_splits(data)

        # Indices for all rows are included
        assert (
            len(train_indices) + len(validation_indices) + len(test_indices)
            == data.shape[0]
        )

        if _get_df_library_type(data) is _DataFrameLib.KOALAS:
            data = data.to_pandas()

        # We use the indices to get the
        # The training set indices refer to the relevant rows in the dataframe
        assert np.all(data.loc[train_indices].L == training_set_label)
        # The test set indices refer to the relevant rows in the dataframe
        assert np.all(data.loc[test_indices].L == test_set_label)
        # The validation set indices refer to the relevant rows in the dataframe
        assert np.all(data.loc[validation_indices].L == validation_set_label)
