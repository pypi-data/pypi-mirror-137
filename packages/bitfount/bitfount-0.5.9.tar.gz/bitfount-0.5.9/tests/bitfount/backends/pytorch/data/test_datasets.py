"""Tests for PyTorchDataset classes."""
from typing import Union

import pytest
from pytest import fixture
import torch

from bitfount.backends.pytorch.data.dataloaders import _PyTorchBitfountDataLoader
from bitfount.backends.pytorch.data.datasets import _PyTorchDataset
from bitfount.data.datasource import DataSource
from bitfount.data.datastructure import DataStructure
from bitfount.data.schema import BitfountSchema
from bitfount.data.types import SemanticType
from bitfount.types import _DataFrameType
from tests.utils.helper import backend_test, create_dataset, unit_test


@backend_test
@unit_test
class TestPyTorchDataset:
    """Tests for PyTorchTabularDataset class."""

    @fixture
    def dataframe(self) -> _DataFrameType:
        """Underlying dataframe for dataset."""
        return create_dataset(image=True)

    @fixture
    def tabular_dataset(self, dataframe: _DataFrameType) -> _PyTorchDataset:
        """Basic PyTorch tabular dataset for tests as fixture."""
        target = "TARGET"
        datasource = DataSource(dataframe)
        schema = BitfountSchema()
        schema.add_datasource_features(datasource)
        datasource.data = schema.apply(datasource.data)
        datasource.data = datasource.data.drop(
            columns=schema.feature_names(SemanticType.TEXT)
        )
        datastructure = DataStructure(target=target, ignore_cols=["image"])
        datastructure.set_training_column_split_by_semantic_type(schema)
        return _PyTorchDataset(
            data=datasource.data,
            target=target,
            selected_cols=datastructure.selected_cols_w_types,
        )

    @fixture
    def image_dataset(self, dataframe: _DataFrameType) -> _PyTorchDataset:
        """Basic PyTorch image dataset for tests as fixture."""
        target = "TARGET"
        datasource = DataSource(dataframe)
        schema = BitfountSchema()
        schema.add_datasource_features(datasource, force_stype={"image": ["image"]})
        datasource.data = schema.apply(datasource.data)
        datasource.data = datasource.data.drop(
            columns=schema.feature_names(SemanticType.TEXT)
        )
        datastructure = DataStructure(target=target, selected_cols=["image"])
        datastructure.set_training_column_split_by_semantic_type(schema)
        return _PyTorchDataset(
            data=datasource.data,
            target=target,
            selected_cols=datastructure.selected_cols_w_types,
        )

    @fixture
    def image_tab_dataset(self, dataframe: _DataFrameType) -> _PyTorchDataset:
        """Basic PyTorchPredictionDataset dataset for tests as fixture."""
        target = "TARGET"
        datasource = DataSource(dataframe)
        schema = BitfountSchema()
        schema.add_datasource_features(datasource, force_stype={"image": ["image"]})
        datasource.data = schema.apply(datasource.data)
        datasource.data = datasource.data.drop(
            columns=schema.feature_names(SemanticType.TEXT)
        )
        datastructure = DataStructure(target=target)
        datastructure.set_training_column_split_by_semantic_type(schema)
        return _PyTorchDataset(
            data=datasource.data,
            target=target,
            selected_cols=datastructure.selected_cols_w_types,
        )

    @fixture
    def multiimage_dataframe(self) -> _DataFrameType:
        """Underlying dataframe for multi-image dataset."""
        return create_dataset(multiimage=True)

    @fixture
    def multiimage_dataset(
        self, multiimage_dataframe: _DataFrameType
    ) -> _PyTorchDataset:
        """Basic multi-image dataset for tests as fixture."""
        target = "TARGET"
        datasource = DataSource(multiimage_dataframe)
        schema = BitfountSchema()
        schema.add_datasource_features(
            datasource, force_stype={"image": ["image1", "image2"]}
        )
        datasource.data = schema.apply(datasource.data)
        datasource.data = datasource.data.drop(
            columns=schema.feature_names(SemanticType.TEXT)
        )
        datastructure = DataStructure(
            target=target, selected_cols=["image1", "image2", target]
        )
        datastructure.set_training_column_split_by_semantic_type(schema)
        return _PyTorchDataset(
            data=datasource.data,
            target=target,
            selected_cols=datastructure.selected_cols_w_types,
        )

    def test_len_tab_data(
        self, dataframe: _DataFrameType, tabular_dataset: _PyTorchDataset
    ) -> None:
        """Tests tabular dataset __len__ method."""
        assert len(tabular_dataset) == len(dataframe)

    def test_len_image_data(
        self, dataframe: _DataFrameType, image_dataset: _PyTorchDataset
    ) -> None:
        """Tests image dataset __len__ method."""
        assert len(image_dataset) == len(dataframe)

    def test_len_image_tab_data(
        self, dataframe: _DataFrameType, image_tab_dataset: _PyTorchDataset
    ) -> None:
        """Tests mixed dataset __len__ method."""
        assert len(image_tab_dataset) == len(dataframe)

    def test_len_multiimage_data(
        self, multiimage_dataframe: _DataFrameType, multiimage_dataset: _PyTorchDataset
    ) -> None:
        """Tests multi-image dataset __len__ method."""
        assert len(multiimage_dataset) == len(multiimage_dataframe)

    @pytest.mark.parametrize("idx", [0, 42, 2048, torch.tensor(3999)])
    def test_idx_tab_data(
        self, idx: Union[int, torch.Tensor], tabular_dataset: _PyTorchDataset
    ) -> None:
        """Tests indexing (incl. tensors) returns the expected formats of data."""
        assert isinstance(tabular_dataset[idx], tuple)
        assert len(tabular_dataset[idx]) == 2  # split into x,y
        assert len(tabular_dataset[idx][0]) == 2  # split into tabular, support
        assert len(tabular_dataset[idx][0][0]) == 13  # training cols  check
        assert len(tabular_dataset[idx][0][1]) == 2  # support cols check
        assert len([tabular_dataset[idx][1]]) == 1  # y check

    @pytest.mark.parametrize("idx", [0, 42, 2048, torch.tensor(3999)])
    def test_idx_img_data(self, idx: int, image_dataset: _PyTorchDataset) -> None:
        """Tests indexing returns the expected formats of data."""
        assert isinstance(image_dataset[idx], tuple)
        assert len(image_dataset[idx]) == 2  # split into x,y
        assert len(image_dataset[idx][0]) == 2  # split into image, support
        assert len(image_dataset[idx][0][1]) == 2  # support cols check
        assert len([image_dataset[idx][1]]) == 1  # y check

    @pytest.mark.parametrize("idx", [0, 42, 2048, torch.tensor(3999)])
    def test_idx_img_tab_data(
        self, idx: int, image_tab_dataset: _PyTorchDataset
    ) -> None:
        """Tests indexing returns the expected formats of data."""
        assert isinstance(image_tab_dataset[idx], tuple)
        assert len(image_tab_dataset[idx]) == 2  # split into x,y
        assert len(image_tab_dataset[idx][0]) == 3  # split into tab, image, support
        assert len(image_tab_dataset[idx][0][0]) == 13  # tabular cols  check
        assert len(image_tab_dataset[idx][0][2]) == 2  # support cols check
        assert len([image_tab_dataset[idx][1]]) == 1  # y check

    @pytest.mark.parametrize("idx", [0, 42, 2048, torch.tensor(3999)])
    def test_idx_multiimg_data(
        self, idx: int, multiimage_dataset: _PyTorchDataset
    ) -> None:
        """Tests indexing returns the expected formats of data."""
        assert isinstance(multiimage_dataset[idx], tuple)
        assert len(multiimage_dataset[idx]) == 2  # split into x,y
        assert len(multiimage_dataset[idx][0]) == 2  # split into image, support
        assert isinstance(multiimage_dataset[idx][0][0], tuple)
        assert len(multiimage_dataset[idx][0][0]) == 2  # image cols check
        assert len(multiimage_dataset[idx][0][1]) == 2  # support cols check
        assert len([multiimage_dataset[idx][1]]) == 1  # y check

    @pytest.mark.parametrize("idx", [0, 42, 2048, torch.tensor(3999)])
    def test_idx_img_tab_category(
        self, idx: int, image_tab_dataset: _PyTorchDataset
    ) -> None:
        """Tests indexing with categories gives expected data formats."""
        target = "TARGET"
        data = create_dataset(image=True, multihead=True)
        datasource = DataSource(data, image_col=["image"])
        schema = BitfountSchema()
        schema.add_datasource_features(
            datasource, force_stype={"categorical": ["category"], "image": ["image"]}
        )
        datasource.data = schema.apply(datasource.data)
        datasource.data = datasource.data.drop(
            columns=schema.feature_names(SemanticType.TEXT)
        )
        datastructure = DataStructure(
            target=target, multihead_col="category", multihead_size=2
        )
        datastructure.set_training_column_split_by_semantic_type(schema)
        dataset = _PyTorchDataset(
            data=datasource.data,
            target=target,
            multihead_col="category",
            selected_cols=datastructure.selected_cols_w_types,
        )
        assert isinstance(dataset[idx], tuple)
        assert len(dataset[idx]) == 2  # split into x,y
        assert len(dataset[idx][0]) == 3  # split into tab, image, support
        assert (
            len(dataset[idx][0][0]) == 14
        )  # tabular cols check (multihead_col included)
        assert len(dataset[idx][0][2]) == 3  # support cols check
        assert len([dataset[idx][1]]) == 1  # y check

    def test_dataloader_pytorch(self, image_tab_dataset: _PyTorchDataset) -> None:
        """Tests iteration of dataloader."""
        batch_size = 64
        dl = _PyTorchBitfountDataLoader(image_tab_dataset, batch_size=batch_size)
        iterator = iter(dl)
        assert isinstance(next(iterator), list)
        assert len(next(iterator)[0]) == 3  # the x part
        assert len(next(iterator)[0][0]) == batch_size  # tabular part
        assert len(next(iterator)[0][1]) == batch_size  # image part
        assert len(next(iterator)[0][2]) == batch_size  # support part
        assert len(next(iterator)[1]) == batch_size  # the y part

    def test_dataloader_non_pytorch_img_tab(
        self, image_tab_dataset: _PyTorchDataset
    ) -> None:
        """Tests x- and y-dataframe retrieval from dataloader."""
        dl = _PyTorchBitfountDataLoader(image_tab_dataset)
        tab, img = dl.get_x_dataframe()
        y = dl.get_y_dataframe()
        assert len(tab) == len(y)
        assert len(img) == len(y)
        assert len(y.columns) == 1
        assert len(tab.columns) == 13
        assert len(img.columns) == 1
