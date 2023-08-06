"""Classes concerning data loading and dataloaders."""
from __future__ import annotations

import math
from typing import TYPE_CHECKING, Iterator, Optional, Tuple, Union

import numpy as np

from bitfount.data.types import _SingleOrMulti
from bitfount.types import _DataFrameType
from bitfount.utils import _get_df_library

if TYPE_CHECKING:
    from bitfount.data.datasets import _BaseDataset


class _BitfountDataLoader:
    """An agnostic data loader for models that load data batch by batch."""

    def __init__(self, dataset: _BaseDataset, batch_size: Optional[int] = None):
        self.dataset = dataset
        self.batch_size = batch_size

    def __iter__(self) -> Iterator[_SingleOrMulti[_SingleOrMulti[np.ndarray]]]:
        """Iterates through the dataset, returning (X,Y) pairs.

        A naive batch-based iteration over numpy representations of the x- and
        y- dataframes.

        If no batch size is provided, uses a batch size of 1.
        """
        batch_size = self.batch_size if self.batch_size else 1
        num_batches = math.ceil(len(self.dataset) / batch_size)

        x_dataframe = self.get_x_dataframe()
        x_data: Union[np.ndarray, Tuple[np.ndarray, np.ndarray]]
        if isinstance(x_dataframe, tuple):
            tab, img = x_dataframe
            x_data = (tab.to_numpy(), img.to_numpy())
        else:
            x_data = x_dataframe.to_numpy()
        y_data: np.ndarray = self.get_y_dataframe().to_numpy()

        for i in range(num_batches):
            x_batch: Union[np.ndarray, Tuple[np.ndarray, np.ndarray]]
            if isinstance(x_data, tuple):
                tab, img = x_data
                x_batch = (
                    tab[i * batch_size : (i + 1) * batch_size],
                    img[i * batch_size : (i + 1) * batch_size],
                )
            else:
                x_batch = x_data[i * batch_size : (i + 1) * batch_size]
            y_batch: np.ndarray = y_data[i * batch_size : (i + 1) * batch_size]
            yield x_batch, y_batch

    def __len__(self) -> int:
        """Number of batches or number of elements if batch size is None."""
        if not self.batch_size:
            return len(self.dataset)
        return math.ceil(len(self.dataset) / self.batch_size)

    def get_x_dataframe(
        self,
    ) -> Union[_DataFrameType, Tuple[_DataFrameType, _DataFrameType]]:
        """Gets the x-dataframe of the data i.e. features.

        For models incompatible with the __iter__ approach.
        """
        tabular, image, support_cols = self.dataset.x_var
        bf = _get_df_library(self.dataset.data)
        if tabular.size and image.size:
            tab_cols = [
                col
                for col in self.dataset.x_columns
                if col not in self.dataset.image_columns
            ]
            tab_df = bf.DataFrame(data=tabular, columns=tab_cols)
            tab_df[self.dataset.embedded_col_names] = tab_df[
                self.dataset.embedded_col_names
            ].astype("int64")
            img_df = bf.DataFrame(data=image, columns=self.dataset.image_columns)
            return tab_df, img_df
        elif image.size:
            img_df = bf.DataFrame(data=image, columns=self.dataset.image_columns)
            return img_df
        elif tabular.size:
            columns = self.dataset.x_columns
            tab_df = bf.DataFrame(data=tabular, columns=columns)
            tab_df[self.dataset.embedded_col_names] = tab_df[
                self.dataset.embedded_col_names
            ].astype("int64")
            return tab_df
        else:
            raise ValueError("No tabular or image data to train with.")

    def get_y_dataframe(self) -> _DataFrameType:
        """Gets the y-dataframe of the data i.e. target.

        For models incompatible with the __iter__ approach.
        """
        columns = self.dataset.y_columns
        data = self.dataset.y_var
        bf = _get_df_library(self.dataset.data)
        dataframe = bf.DataFrame(data=data, columns=columns)
        return dataframe
