"""Pytest fixtures for data tests."""

from pytest import fixture

from bitfount.data.datasets import _Dataset
from bitfount.data.datasource import DataSource
from bitfount.data.datastructure import DataStructure
from bitfount.data.schema import BitfountSchema
from bitfount.data.types import SemanticType
from bitfount.types import _DataFrameType
from tests.utils.helper import create_dataset


@fixture
def dataframe() -> _DataFrameType:
    """Underlying dataframe for single image datasets."""
    return create_dataset(image=True)


@fixture
def tabular_dataset(dataframe: _DataFrameType) -> _Dataset:
    """Basic tabular dataset for tests as fixture."""
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
    return _Dataset(
        data=datasource.data,
        target=target,
        selected_cols=datastructure.selected_cols_w_types,
    )


@fixture
def image_dataset(dataframe: _DataFrameType) -> _Dataset:
    """Basic image dataset for tests as fixture."""
    target = "TARGET"
    datasource = DataSource(dataframe)
    schema = BitfountSchema()
    schema.add_datasource_features(datasource, force_stype={"image": ["image"]})
    datasource.data = schema.apply(datasource.data)
    datasource.data = datasource.data.drop(
        columns=schema.feature_names(SemanticType.TEXT)
    )
    datastructure = DataStructure(
        target=target,
        selected_cols=["image", target],
        image_cols=["image"],
        batch_transforms=[
            {
                "image": {
                    "step": "train",
                    "output": True,
                    "arg": "image",
                    "transformations": [
                        {"Resize": {"height": 224, "width": 224}},
                        "Normalize",
                    ],
                }
            }
        ],
    )
    datastructure.set_training_column_split_by_semantic_type(schema)
    return _Dataset(
        data=datasource.data,
        target=target,
        selected_cols=datastructure.selected_cols_w_types,
        batch_transforms=datastructure.get_batch_transformations(),
        batch_transformation_step="train",
    )


@fixture
def image_tab_dataset(dataframe: _DataFrameType) -> _Dataset:
    """Basic tabular and image dataset for tests as fixture."""
    target = "TARGET"
    datasource = DataSource(dataframe)
    schema = BitfountSchema()
    schema.add_datasource_features(datasource, force_stype={"image": ["image"]})
    datasource.data = schema.apply(datasource.data)
    datasource.data = datasource.data.drop(
        columns=schema.feature_names(SemanticType.TEXT)
    )
    datastructure = DataStructure(target=target, image_cols=["image"])
    datastructure.set_training_column_split_by_semantic_type(schema)
    return _Dataset(
        data=datasource.data,
        target=target,
        selected_cols=datastructure.selected_cols_w_types,
    )


@fixture
def multiimage_dataframe() -> _DataFrameType:
    """Underlying dataframe for multi-image dataset."""
    return create_dataset(multiimage=True)


@fixture
def multiimage_dataset(multiimage_dataframe: _DataFrameType) -> _Dataset:
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

    return _Dataset(
        data=datasource.data,
        target=target,
        selected_cols=datastructure.selected_cols_w_types,
    )
