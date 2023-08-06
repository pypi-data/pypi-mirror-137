"""Test dataset classes in data/datasets.py."""


from PIL import Image
import numpy as np
import pytest
from pytest import fixture

from bitfount.data.datasets import _Dataset
from bitfount.data.datasource import DataSource
from bitfount.data.datastructure import DataStructure
from bitfount.data.schema import BitfountSchema
from bitfount.data.types import SemanticType
from bitfount.types import _DataFrameType
from tests.utils.helper import create_dataset, unit_test


@unit_test
class TestDataset:
    """Tests for PredictionDataset class."""

    @fixture
    def dataframe(self) -> _DataFrameType:
        """Underlying dataframe for single image datasets."""
        return create_dataset(image=True)

    def test_len_tab_data(
        self, dataframe: _DataFrameType, tabular_dataset: _Dataset
    ) -> None:
        """Tests tabular dataset __len__ method."""
        assert len(tabular_dataset) == len(dataframe)

    @pytest.mark.parametrize("idx", [0, 42, 2048])
    def test_idx_tab_data(self, idx: int, tabular_dataset: _Dataset) -> None:
        """Tests indexing returns the expected formats of data."""
        assert isinstance(tabular_dataset[idx], tuple)
        assert len(tabular_dataset[idx]) == 2  # split into x,y
        assert len(tabular_dataset[idx][0]) == 2  # split into tabular, support
        assert len(tabular_dataset[idx][0][0]) == 13  # training cols  check
        assert len(tabular_dataset[idx][0][1]) == 2  # support cols check
        assert len([tabular_dataset[idx][1]]) == 1  # y check

    def test_len_img_data(
        self, dataframe: _DataFrameType, image_tab_dataset: _Dataset
    ) -> None:
        """Tests image dataset __len__ method."""
        assert len(image_tab_dataset) == len(dataframe)

    @pytest.mark.parametrize("idx", [0, 42, 2048])
    def test_idx_img_data(self, idx: int, image_dataset: _Dataset) -> None:
        """Tests indexing returns the expected formats of data."""
        assert isinstance(image_dataset[idx], tuple)
        assert len(image_dataset[idx]) == 2  # split into x,y
        assert len(image_dataset[idx][0]) == 2  # split into image, support
        assert len(image_dataset[idx][0][1]) == 2  # support cols check
        assert len([image_dataset[idx][1]]) == 1  # y check

    def test_len_img_tab_data(
        self, dataframe: _DataFrameType, image_dataset: _Dataset
    ) -> None:
        """Tests dataset __len__ method."""
        assert len(image_dataset) == len(dataframe)

    @pytest.mark.parametrize("idx", [0, 42, 2048])
    def test_idx_img_tab_data(self, idx: int, image_tab_dataset: _Dataset) -> None:
        """Tests indexing returns the expected formats of data."""
        indexed_item = image_tab_dataset[idx]
        assert isinstance(indexed_item, tuple)
        assert len(indexed_item) == 2  # split into x,y

        X: tuple = indexed_item[0]
        assert isinstance(X, tuple)
        assert len(X) == 3  # split into tab, image, support

        assert len(X[0]) == 13  # tabular cols  check
        assert len(X[2]) == 2  # support cols check

        assert len([indexed_item[1]]) == 1  # y check

    def test_len_multiimg_data(
        self, multiimage_dataframe: _DataFrameType, multiimage_dataset: _Dataset
    ) -> None:
        """Tests multi-image dataset __len__ method."""
        assert len(multiimage_dataset) == len(multiimage_dataframe)

    @pytest.mark.parametrize("idx", [0, 42, 2048])
    def test_idx_multiimg_data(self, idx: int, multiimage_dataset: _Dataset) -> None:
        """Tests indexing returns the expected formats of data."""
        assert isinstance(multiimage_dataset[idx], tuple)
        assert len(multiimage_dataset[idx]) == 2  # split into x,y
        assert len(multiimage_dataset[idx][0]) == 2  # split into image, support
        assert isinstance(multiimage_dataset[idx][0][0], tuple)
        assert len(multiimage_dataset[idx][0][0]) == 2  # image col check
        assert len(multiimage_dataset[idx][0][1]) == 2  # support cols check
        assert len([multiimage_dataset[idx][1]]) == 1  # y check

    @pytest.mark.parametrize("idx", [0, 42, 2048])
    def test_idx_category(self, idx: int) -> None:
        """Tests indexing with categories gives expected data formats."""
        target = "TARGET"
        data = create_dataset(image=True, multihead=True)
        datasource = DataSource(data)
        datastructure = DataStructure(
            target=target,
            multihead_col="category",
            multihead_size=2,
        )
        schema = BitfountSchema()
        schema.add_datasource_features(
            datasource, force_stype={"categorical": ["category"], "image": ["image"]}
        )
        datasource.data = schema.apply(datasource.data)
        datasource.data = datasource.data.drop(
            columns=schema.feature_names(SemanticType.TEXT)
        )

        datastructure.set_training_column_split_by_semantic_type(schema)
        dataset = _Dataset(
            data=datasource.data,
            target=target,
            multihead_col="category",
            selected_cols=datastructure.selected_cols_w_types,
        )

        indexed_item: tuple = dataset[idx]
        assert isinstance(indexed_item, tuple)
        assert len(indexed_item) == 2  # split into x,y

        X: tuple = indexed_item[0]
        assert isinstance(X, tuple)
        assert len(X) == 3  # split into tab, image, support
        assert len(X[0]) == 14  # tabular cols check (multihead_col included)
        assert len(X[2]) == 3  # support cols check

        assert len([indexed_item[1]]) == 1  # y check

    def test_dataset_works_only_with_continuous_features(
        self, dataframe: _DataFrameType
    ) -> None:
        """Test no errors are raised if the dataset only has continuous features."""
        datasource = DataSource(dataframe.loc[:, ["A", "B", "TARGET"]])
        schema = BitfountSchema()
        schema.add_datasource_features(datasource)
        datastructure = DataStructure(target=["TARGET"])
        datastructure.set_training_column_split_by_semantic_type(schema)
        dataset = _Dataset(
            data=datasource.data,
            target=["TARGET"],
            selected_cols=datastructure.selected_cols_w_types,
        )
        assert "categorical" not in schema.features
        idx = 10
        assert isinstance(dataset[idx], tuple)
        assert len(dataset[idx]) == 2  # split into x,y
        assert len(dataset[idx][0]) == 2  # split into tabular, support
        assert len(dataset[idx][0][0]) == 2  # training cols  check
        assert len(dataset[idx][0][1]) == 2  # support cols check
        assert len([dataset[idx][1]]) == 1  # y check

    def test_dataset_works_without_target(self, dataframe: _DataFrameType) -> None:
        """Test no errors are raised if the dataset has no target."""
        datasource = DataSource(dataframe.loc[:, ["A", "B"]])
        schema = BitfountSchema()
        schema.add_datasource_features(datasource)
        datastructure = DataStructure()
        datastructure.set_training_column_split_by_semantic_type(schema)
        dataset = _Dataset(
            data=datasource.data,
            selected_cols=datastructure.selected_cols_w_types,
        )
        idx = 10
        assert isinstance(dataset[idx], tuple)
        assert len(dataset[idx]) == 2  # split into x,y
        assert len(dataset[idx][0]) == 2  # split into tabular, support
        assert len(dataset[idx][0][0]) == 2  # training cols  check
        assert len(dataset[idx][0][1]) == 2  # support cols check
        assert len([dataset[idx][1]]) == 1  # y check
        for i in range(0, len(dataset)):
            assert dataset[i][1] == 0  # all target values default to 0.

    def test_dataset_works_only_with_categorical_features(
        self, dataframe: _DataFrameType
    ) -> None:
        """Test no errors are raised if the dataset only has categorical features."""
        datasource = DataSource(dataframe.loc[:, ["M", "N", "TARGET"]])
        schema = BitfountSchema()
        schema.add_datasource_features(
            datasource, force_stype={"categorical": ["TARGET"]}
        )
        datastructure = DataStructure(target=["TARGET"])
        datastructure.set_training_column_split_by_semantic_type(schema)
        dataset = _Dataset(
            data=datasource.data,
            target=["TARGET"],
            selected_cols=datastructure.selected_cols_w_types,
        )
        assert "continuous" not in schema.features
        idx = 10
        assert isinstance(dataset[idx], tuple)
        assert len(dataset[idx]) == 2  # split into x,y
        assert len(dataset[idx][0]) == 2  # split into tabular, support
        assert len(dataset[idx][0][0]) == 2  # training cols  check
        assert len(dataset[idx][0][1]) == 2  # support cols check
        assert len([dataset[idx][1]]) == 1  # y check

    def test_batch_transformation_step_missing_raises_value_error(
        self, dataframe: _DataFrameType
    ) -> None:
        """Tests that a ValueError is raised if batch transformation step is missing."""
        target = "TARGET"
        datasource = DataSource(dataframe)
        schema = BitfountSchema()
        schema.add_datasource_features(datasource, force_stype={"image": ["image"]})
        datasource.data = schema.apply(datasource.data)
        datasource.data = datasource.data.drop(
            columns=schema.feature_names(SemanticType.TEXT)
        )
        datastructure = DataStructure(
            target=target, selected_cols=["image", target], image_cols=["image"]
        )
        datastructure.set_training_column_split_by_semantic_type(schema)
        with pytest.raises(ValueError):
            _Dataset(
                data=datasource.data,
                target=target,
                selected_cols=datastructure.selected_cols_w_types,
                batch_transforms=datastructure.get_batch_transformations(),
            )

    def test_transform_image(self, image_dataset: _Dataset) -> None:
        """Test transform_image method."""
        assert image_dataset.batch_transforms is not None
        img_array = np.array(Image.new("RGB", size=(224, 224), color=(55, 100, 2)))
        transformed_image = image_dataset._transform_image(img_array, 0)
        assert isinstance(transformed_image, np.ndarray)
        assert transformed_image.shape == (224, 224, 3)

        # Assert that the transformed image is not the same as the original
        with pytest.raises(AssertionError):
            np.testing.assert_array_equal(img_array, transformed_image)

    def test_load_image(self, image_dataset: _Dataset) -> None:
        """Test transform_image method."""
        loaded_transformed_image = image_dataset._load_images(0)
        assert isinstance(loaded_transformed_image, np.ndarray)
        assert loaded_transformed_image.shape == (224, 224, 3)

    # The below comment can be removed unless anyone thinks we need more tests.
    # TODO: [BIT-983] Add non-backend dataset tests
