"""Tests datasource.py."""
from functools import partial
from pathlib import Path
from typing import Any, Callable, Tuple
from unittest.mock import Mock

from _pytest.monkeypatch import MonkeyPatch
import numpy as np
import pandas as pd
import pytest
from pytest import fixture
from pytest_mock import MockerFixture

from bitfount.data.datasource import DataSource
from bitfount.data.datasplitters import _DatasetSplitter
from bitfount.data.types import DataPathModifiers
from bitfount.data.utils import DatabaseConnection
from bitfount.types import _DataFrameType
from tests.utils import PytestRequest
from tests.utils.helper import DATASET_ROW_COUNT, create_dataset, unit_test


@fixture
def data(request: PytestRequest) -> _DataFrameType:
    """Returns dataset."""
    return create_dataset(koalas=request.param)


@unit_test
class TestDataSource:
    """Test DataSource classes from bitfount.data."""

    @fixture
    def mock_pandas_sql(self, monkeypatch: MonkeyPatch) -> None:
        """Pandas `read_sql_table()` mocked."""
        data = create_dataset()

        def get_df(**_kwargs: Any) -> _DataFrameType:
            return data

        monkeypatch.setattr(pd, "read_sql_table", get_df)

    class FakeSplitter(_DatasetSplitter):
        """Fake Splitter that just returns predefined indices."""

        def __init__(
            self,
            train_indices: np.ndarray,
            validation_indices: np.ndarray,
            test_indices: np.ndarray,
        ):
            self.train_indices = train_indices
            self.validation_indices = validation_indices
            self.test_indices = test_indices

        @classmethod
        def splitter_name(cls) -> str:
            """Splitter name for config."""
            return "FakeSplitter"

        def create_dataset_splits(
            self, data: _DataFrameType
        ) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
            """Returns predefined indices and provided data."""
            return self.train_indices, self.validation_indices, self.test_indices

    @fixture(scope="function", params=["pandas", "koalas", "image"])
    def datasource_generator(self, request: PytestRequest) -> Callable[..., DataSource]:
        """Dataset loader for use in tests."""
        koalas, image = False, False
        if request.param == "koalas":
            koalas = True
        elif request.param == "image":
            image = True
        data = create_dataset(koalas=koalas, image=image)
        if image:
            return partial(DataSource, data=data, seed=420)

        return partial(DataSource, data=data, koalas=koalas, seed=420)

    def test_database_input(self, mock_pandas_sql: None) -> None:
        """Checks DataSource initialises correctly with `DatabaseConnection`."""
        db_conn = DatabaseConnection("table_name", "URI")
        dataset = DataSource(db_conn, seed=420)
        assert dataset.data is not None
        assert len(dataset.train_idxs) + len(dataset.validation_idxs) + len(
            dataset.test_idxs
        ) == len(dataset.data)

    def test_training_set(
        self, datasource_generator: Callable[..., DataSource]
    ) -> None:
        """Checks training set is behaving correctly."""
        test_percentage = 25
        validation_percentage = 55
        train_percentage = (100 - test_percentage) - validation_percentage
        data_source = datasource_generator(
            data_splitter=self.FakeSplitter(
                np.array(range(int(DATASET_ROW_COUNT * (train_percentage / 100)))),
                np.array(range(int(DATASET_ROW_COUNT * (validation_percentage / 100)))),
                np.array(range(int(DATASET_ROW_COUNT * (test_percentage / 100)))),
            )
        )

        # assert columns match the original data
        assert data_source.data.shape[1] == data_source.train_set.shape[1]
        # assert there are the expected number of rows
        assert (
            int(train_percentage * data_source.data.shape[0] / 100)
            == data_source.train_set.shape[0]
        )

    def test_validation_set(
        self, datasource_generator: Callable[..., DataSource]
    ) -> None:
        """Checks validation set is behaving correctly."""
        test_percentage = 25
        validation_percentage = 55
        train_percentage = (100 - test_percentage) - validation_percentage
        data_source = datasource_generator(
            data_splitter=self.FakeSplitter(
                np.array(range(int(DATASET_ROW_COUNT * (train_percentage / 100)))),
                np.array(range(int(DATASET_ROW_COUNT * (validation_percentage / 100)))),
                np.array(range(int(DATASET_ROW_COUNT * (test_percentage / 100)))),
            )
        )
        # assert columns match the original data
        assert data_source.data.shape[1] == data_source.validation_set.shape[1]
        # assert there are the expected number of rows
        assert (
            int(validation_percentage * data_source.data.shape[0] / 100)
            == data_source.validation_set.shape[0]
        )

    def test_test_set(self, datasource_generator: Callable[..., DataSource]) -> None:
        """Checks test set is behaving correctly."""
        test_percentage = 25
        validation_percentage = 55
        train_percentage = (100 - test_percentage) - validation_percentage
        data_source = datasource_generator(
            data_splitter=self.FakeSplitter(
                np.array(range(int(DATASET_ROW_COUNT * (train_percentage / 100)))),
                np.array(range(int(DATASET_ROW_COUNT * (validation_percentage / 100)))),
                np.array(range(int(DATASET_ROW_COUNT * (test_percentage / 100)))),
            )
        )
        # assert columns match the original data
        assert data_source.data.shape[1] == data_source.test_set.shape[1]
        # assert there are the expected number of rows
        assert (
            int(test_percentage * data_source.data.shape[0] / 100)
            == data_source.test_set.shape[0]
        )

    def test_zero_validation_test_size(
        self, datasource_generator: Callable[..., DataSource]
    ) -> None:
        """Checks Dataset object behaves properly when if valid and test pct are 0."""
        data_source = datasource_generator(
            data_splitter=self.FakeSplitter(
                train_indices=np.array(range(DATASET_ROW_COUNT)),
                validation_indices=np.array([]),
                test_indices=np.array([]),
            )
        )

        assert len(data_source.data) == len(data_source.train_set)
        assert len(data_source.test_idxs) == 0
        assert len(data_source.validation_idxs) == 0

    def test_tabular_datasource_errors(self) -> None:
        """Checks DataSource object errors via wrong first argument."""
        with pytest.raises(TypeError):
            DataSource("test1", seed=420)
        with pytest.raises(TypeError):
            test_path = Path("/my/root/directory")
            DataSource(test_path, seed=420)

    def test_datasource_modifiers_path_prefix(self) -> None:
        """Tests functionality for providing image path prefix."""
        data = create_dataset()
        data["image"] = "image_file_name"
        modifiers = {"image": DataPathModifiers({"prefix": "/path/to/"})}
        dataset = DataSource(
            data=data,
            modifiers=modifiers,
            seed=420,
        )
        assert len(dataset.data["image"].unique()) == 1
        assert dataset.data["image"].unique()[0] == "/path/to/image_file_name"

    def test_image_datasource_ext_suffix(self) -> None:
        """Tests functionality for finding images by file extension."""
        data = create_dataset()
        data["image"] = "image_file_name"
        modifiers = {"image": DataPathModifiers({"suffix": ".jpeg"})}
        dataset = DataSource(
            data=data,
            modifiers=modifiers,
            seed=420,
        )
        assert len(dataset.data["image"].unique()) == 1
        assert dataset.data["image"].unique()[0] == "image_file_name.jpeg"

    def test_image_datasource_ext_prefix_suffix(self) -> None:
        """Tests functionality for finding images by file extension."""
        data = create_dataset()
        data["image"] = "image_file_name"
        modifiers = {
            "image": DataPathModifiers({"prefix": "/path/to/", "suffix": ".jpeg"})
        }
        dataset = DataSource(
            data=data,
            modifiers=modifiers,
            seed=420,
        )
        assert len(dataset.data["image"].unique()) == 1
        assert dataset.data["image"].unique()[0] == "/path/to/image_file_name.jpeg"

    def test_multiple_img_datasource_modifiers(self) -> None:
        """Tests functionality for finding multiple images by file extension."""
        data = create_dataset(multiimage=True, img_size=1)
        data["image1"] = "image1_file_name"
        data["image2"] = "image2_file_name"
        modifiers = {
            "image1": DataPathModifiers({"prefix": "/path/to/"}),
            "image2": DataPathModifiers({"suffix": ".jpeg"}),
        }
        dataset = DataSource(
            data=data,
            modifiers=modifiers,
            seed=420,
        )
        assert len(dataset.data["image1"].unique()) == 1
        assert dataset.data["image1"].unique()[0] == "/path/to/image1_file_name"
        assert len(dataset.data["image2"].unique()) == 1
        assert dataset.data["image2"].unique()[0] == "image2_file_name.jpeg"

    def test_tabular_datasource_read_csv_correctly(self, tmp_path: Path) -> None:
        """Tests DataSource loading from csv."""
        file_path = tmp_path / "tabular_data_test.csv"
        data = create_dataset()
        data.to_csv(file_path)
        DataSource(file_path)

    def test_ignored_cols_list_excluded_from_df(self) -> None:
        """Tests that a list of ignore_cols are ignored in the data."""
        data = create_dataset()
        data["image"] = "image_file_name"
        ignore_cols = ["N", "O", "P"]
        dataset = DataSource(
            data=data,
            image_col=["image"],
            seed=420,
            image_extension="jpeg",
            ignore_cols=ignore_cols,
        )
        assert not any(item in dataset.data.columns for item in ignore_cols)

    def test_ignored_single_col_list_excluded_from_df(self) -> None:
        """Tests that a str ignore_cols is ignored in the data."""
        data = create_dataset()
        data["image"] = "image_file_name"
        ignore_cols = "N"
        dataset = DataSource(
            data=data,
            image_col=["image"],
            seed=420,
            image_extension="jpeg",
            ignore_cols=ignore_cols,
        )
        assert ignore_cols not in dataset.data.columns

    def test_hash(
        self, datasource_generator: Callable[..., DataSource], mocker: MockerFixture
    ) -> None:
        """Tests hash is called on the dataframe."""
        datasource = datasource_generator()
        expected_hash = f"hash_{id(datasource.data)}"
        mock_hash_function: Mock = mocker.patch(
            "bitfount.data.datasource._generate_dataframe_hash",
            return_value=expected_hash,
            autospec=True,
        )

        actual_hash = datasource.hash

        # Check hash is expected return and how it was called
        assert actual_hash == expected_hash
        mock_hash_function.assert_called_once_with(datasource.data)
