"""Classes concerning databunches."""
from __future__ import annotations

import logging
from typing import Any, Literal, Optional

from bitfount.data.datafactory import _DataFactory, _load_default_data_factory
from bitfount.data.dataloader import _BitfountDataLoader
from bitfount.data.datasets import _BaseDataset, _Dataset
from bitfount.data.datasource import DataSource
from bitfount.data.datastructure import DataStructure
from bitfount.data.schema import BitfountSchema
from bitfount.data.types import SemanticType
from bitfount.types import _DataFrameType
from bitfount.utils import _add_this_to_list

logger = logging.getLogger(__name__)


class _BitfountDataBunch:
    """Wrapper for train, validation and test data.

    Provides methods to access dataloaders for training.

    Args:
        data_structure: A `DataStructure` object.
        datasource: A `DataSource` object.
        data_factory: A `_DataFactory` instance for creating
            datasets and dataloaders. Defaults to None.
         **kwargs: additional arguments to pass to the `_DataBunch`.
    """

    def __init__(
        self,
        data_structure: DataStructure,
        schema: BitfountSchema,
        datasource: DataSource,
        data_factory: Optional[_DataFactory] = None,
        **kwargs: Any,
    ):
        self.data_structure = data_structure
        self.datasource = datasource
        self.schema = schema
        self.target = data_structure.target
        self.loss_weights_col = data_structure.loss_weights_col
        self.multihead_col = data_structure.multihead_col
        self.ignore_classes_col = data_structure.ignore_classes_col

        # Placeholders for generated datasets
        self.train_ds: _BaseDataset
        self.validation_ds: Optional[_BaseDataset] = None
        self.test_ds: Optional[_BaseDataset] = None

        # Make sure that the appropriate columns are selected from schema
        if (
            not self.data_structure.selected_cols
            and not self.data_structure.ignore_cols
        ):
            self.data_structure.selected_cols = [
                col
                for col in self.schema.feature_names()
                if col not in schema.feature_names(SemanticType.TEXT)
            ]
        elif not self.data_structure.selected_cols:
            self.data_structure.selected_cols = [
                col
                for col in self.schema.feature_names()
                if col not in self.data_structure.ignore_cols
                and col not in schema.feature_names(SemanticType.TEXT)
            ]
        elif not self.data_structure.ignore_cols:
            self.data_structure.ignore_cols = [
                col
                for col in self.schema.feature_names()
                if col not in self.data_structure.selected_cols
            ]

        disallowed_columns = []
        for col in self.data_structure.selected_cols:
            if col in schema.feature_names(SemanticType.TEXT):
                disallowed_columns.append(col)
                logger.warning(
                    f"DataStructure has selected the text column {col} "
                    f"which is not supported. Removing this from the selection."
                )
        self.data_structure.ignore_cols = _add_this_to_list(
            disallowed_columns, self.data_structure.ignore_cols
        )
        self.data_structure.selected_cols = [
            i for i in self.data_structure.selected_cols if i not in disallowed_columns
        ]
        # Make sure that the appropriate columns are selected from schema
        self.data_structure.set_training_column_split_by_semantic_type(schema)
        self.ignore_cols = self.data_structure.ignore_cols[:]
        self.ignore_cols = _add_this_to_list(self.target, self.ignore_cols)
        self.ignore_cols = _add_this_to_list(self.loss_weights_col, self.ignore_cols)
        self.ignore_cols = _add_this_to_list(self.ignore_classes_col, self.ignore_cols)

        # In future we may want to allow different choices of features from the schema
        self.categorical_features = [
            feature
            for feature in self.schema.feature_names(SemanticType.CATEGORICAL)
            if feature not in self.ignore_cols
        ]
        self.continuous_features = [
            feature
            for feature in self.schema.feature_names(SemanticType.CONTINUOUS)
            if feature not in self.ignore_cols
        ]
        if data_factory is None:
            data_factory = _load_default_data_factory()
        self.data_factory = data_factory

        # Datasource will always be provided with the new refactor.
        self.create_datasets()

    def _data_to_dataset(
        self, data: _DataFrameType, step: Literal["train", "validation"]
    ) -> _Dataset:
        """Converts pandas dataframe to relevant BitfountDataset."""
        rel_cols = self.data_structure.selected_cols
        # `rel_cols` needs to be passed to the `apply` method here to ensure that we
        # don't end up removing the extra columns in our dataframe that are used during
        # training (e.g. loss_weights_col, etc.) but aren't part of the schema
        data = self.schema.apply(data, keep_cols=rel_cols)
        # Applying the schema adds extra columns to the dataframe if they are missing.
        # Therefore we need to subset the data columns here to ensure we are only using
        # the columns specified for this task
        data = data[rel_cols].reset_index(drop=True)
        extra_cols = dict(
            weights_col=self.loss_weights_col,
            multihead_col=self.multihead_col,
            ignore_classes_col=self.ignore_classes_col,
        )

        transforms = self.data_structure.get_batch_transformations()

        return self.data_factory.create_dataset(
            data=data,
            target=self.target,
            selected_cols=self.data_structure.selected_cols_w_types,
            batch_transforms=transforms,
            batch_transformation_step=step,
            **extra_cols,
        )

    def create_datasets(self) -> None:
        """Creates datasets for dataloaders.

        Sets `self.train_ds`, `self.validation_ds` and `self.test_ds`
        """
        self.train_ds = self._data_to_dataset(self.datasource.train_set, "train")
        self.validation_ds = self._data_to_dataset(
            self.datasource.validation_set, "validation"
        )
        self.test_ds = self._data_to_dataset(self.datasource.test_set, "validation")

    def get_train_dataloader(
        self, batch_size: Optional[int] = None
    ) -> _BitfountDataLoader:
        """Gets the relevant data loader for training data."""
        return self.data_factory.create_dataloader(self.train_ds, batch_size=batch_size)

    def get_validation_dataloader(
        self, batch_size: Optional[int] = None
    ) -> Optional[_BitfountDataLoader]:
        """Gets the relevant data loader for validation data."""
        if not self.validation_ds:
            logging.warning(
                "No validation data in the dataset. Validation DataLoader is 'None'."
            )
            return None

        return self.data_factory.create_dataloader(
            self.validation_ds, batch_size=batch_size
        )

    def get_test_dataloader(
        self, batch_size: Optional[int] = None
    ) -> Optional[_BitfountDataLoader]:
        """Gets the relevant data loader for test data."""
        if not self.test_ds:
            logging.warning("No test data in the dataset. Test DataLoader is 'None'.")
            return None

        return self.data_factory.create_dataloader(self.test_ds, batch_size=batch_size)
