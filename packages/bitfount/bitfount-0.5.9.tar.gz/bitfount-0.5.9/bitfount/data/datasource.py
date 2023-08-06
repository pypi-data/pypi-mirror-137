"""Classes concerning sources of data."""
from __future__ import annotations

import dataclasses
import os
from pathlib import Path
from typing import Any, Dict, Optional, Sequence, Union, cast

import databricks.koalas as ks
import pandas as pd
from pydantic import AnyUrl

from bitfount.data.datasplitters import PercentageSplitter, _DatasetSplitter
from bitfount.data.types import DataPathModifiers
from bitfount.data.utils import DatabaseConnection, _generate_dataframe_hash
from bitfount.types import _DataFrameType, _PandasLikeModule
from bitfount.utils import seed_all


class DataSource:
    """DataSource class which encapsulates data.

    Args:
        data: Data to load.
        data_splitter: Approach used for splitting the data into training, test,
            validation. Defaults to None.
        seed: Random number seed. Used for setting random seed for all libraries.
            Defaults to None.
        koalas: Whether to load data as koalas dataframe (rather than pandas).
            Defaults to False.
        modifiers: Dictionary used for modifying paths/ extensions in the dataframe.
            Defaults to None.
        ignore_cols: Column/list of columns to be ignored from the data.
            Defaults to None.

    Attributes:
        data: A Dataframe-type object which contains the data.
        seed: Random number seed. Used for setting random seed for all libraries.
        train_idxs: A numpy array containing the indices of the data which
            will be used for training.
        validation_idxs: A numpy array containing the indices of the data which
            will be used for validation.
        test_idxs: A numpy array containing the indices of the data which
            will be used for testing.

    Raises:
        TypeError: If data format is not supported.
        ValueError: If `image_col` is specified but can't be found in `data` or if
            `koalas` is additionally specified.
    """

    def __init__(
        self,
        data: Union[os.PathLike, AnyUrl, DatabaseConnection, _DataFrameType],
        data_splitter: Optional[_DatasetSplitter] = None,
        seed: Optional[int] = None,
        koalas: bool = False,
        modifiers: Optional[Dict[str, DataPathModifiers]] = None,
        ignore_cols: Optional[Union[str, Sequence[str]]] = None,
        **kwargs: Any,
    ):

        bf: _PandasLikeModule = cast(_PandasLikeModule, ks if koalas else pd)
        self.data: _DataFrameType
        self.seed = seed
        seed_all(self.seed)
        # If these if statement blocks increase much more in number or size, we
        # should consider subclassing DataSource for each one. At the moment, it is
        # reasonable to keep them together since we always end up with a dataframe
        # but if this changes, we should create a subclass for it
        if isinstance(data, (str, Path)):
            if not str(data).endswith(".csv"):
                raise TypeError("Please provide a Path or URL to a CSV file.")
            self.data = bf.read_csv(str(data), **kwargs)
        elif isinstance(data, DatabaseConnection):
            self.data = bf.read_sql_table(**dataclasses.asdict(data), **kwargs)
        elif isinstance(data, (pd.DataFrame, ks.DataFrame)):
            self.data = data
        else:
            raise TypeError(f"Can't read data of type {type(data)}")

        # Need to remove the ignored_columns from the dataframe.
        if ignore_cols:
            if isinstance(ignore_cols, str):
                ignore_cols = [ignore_cols]
            for col in ignore_cols:
                self.data = self.data.drop(col, axis=1)

        if modifiers:
            self._modify_file_paths(modifiers)

        if not data_splitter:
            data_splitter = PercentageSplitter()

        (
            self.train_idxs,
            self.validation_idxs,
            self.test_idxs,
        ) = data_splitter.create_dataset_splits(self.data)

    @property
    def hash(self) -> str:
        """The hash associated with this DataSource.

        This is the hash of the static information regarding the underlying DataFrame,
        primarily column names and content types but NOT anything content-related
        itself. It should be consistent across invocations, even if additional data
        is added, as long as the DataFrame is still compatible in its format.

        Returns:
            The hexdigest of the DataFrame hash.
        """
        return _generate_dataframe_hash(self.data)

    def _modify_file_paths(self, modifiers: Dict[str, DataPathModifiers]) -> None:
        """Modifies image file paths if provided.

        Args:
            modifiers: A dictionary with the column name and
            prefix and/or suffix to modify file path.
        """
        for column_name in modifiers.keys():
            self.data[column_name] = self.data[column_name].astype(str)
            # Get the modifier dictionary:
            modifier_dict = modifiers[column_name]
            for modifier_type, modifier_string in modifier_dict.items():
                if modifier_type == "prefix":
                    self.data[column_name] = self.data[column_name].apply(
                        lambda x: f"{modifier_string}{x}"
                    )
                elif modifier_type == "suffix":
                    self.data[column_name] = self.data[column_name].apply(
                        lambda x: f"{x}{modifier_string}"
                    )

    @property
    def test_set(self) -> _DataFrameType:
        """Test set portion of `self.data`.

        Returns:
            A dataframe-type object containing the data points with indices
            from the `self.test_idxs`.The indices will be reset in this test set.
        """
        return self.data.loc[self.test_idxs.tolist()].reset_index(drop=True)

    @property
    def train_set(self) -> _DataFrameType:
        """Train set portion of `self.data`.

        Returns:
            A dataframe-type object containing the data points with indices
            from the `self.train_idxs`.The indices will be reset in this train set.
        """
        return self.data.loc[self.train_idxs.tolist()].reset_index(drop=True)

    @property
    def validation_set(self) -> _DataFrameType:
        """Validation set portion of `self.data`.

        Returns:
            A dataframe-type object containing the data points with indices
            from the `self.validation_idxs`.The indices will be reset
            in this validation set.
        """
        return self.data.loc[self.validation_idxs.tolist()].reset_index(drop=True)
