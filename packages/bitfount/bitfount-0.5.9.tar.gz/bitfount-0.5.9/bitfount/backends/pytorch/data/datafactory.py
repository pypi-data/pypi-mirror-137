"""PyTorch implementations of the datafactory module contents."""
from typing import Any, List, Literal, Mapping, Optional, Union, cast

import pandas as pd
from torch.utils.data import Dataset

from bitfount.backends.pytorch.data.dataloaders import _PyTorchBitfountDataLoader
from bitfount.backends.pytorch.data.datasets import _PyTorchBaseDataset, _PyTorchDataset
from bitfount.data.datafactory import _BaseDataset, _DataFactory
from bitfount.data.types import _SemanticTypeValue
from bitfount.transformations.batch_operations import BatchTimeOperation


class _PyTorchDataFactory(_DataFactory):
    """A PyTorch-specific implementation of the DataFactory provider."""

    def create_dataloader(
        self, data: _BaseDataset, batch_size: Optional[int] = None
    ) -> _PyTorchBitfountDataLoader:
        """See base class."""
        if not isinstance(data, Dataset):
            raise TypeError(
                "The PyTorchBitfountDataLoader class only supports "
                "subclasses of PyTorch Dataset."
            )

        # If it's an instance of Dataset and of BitfountDataset, we can try to use it
        data = cast(_PyTorchBaseDataset, data)  # stop type-checker from complaining
        return _PyTorchBitfountDataLoader(data, batch_size)

    def create_dataset(
        self,
        data: pd.DataFrame,
        selected_cols: Mapping[_SemanticTypeValue, List[str]],
        target: Optional[Union[str, List[str]]] = None,
        batch_transforms: Optional[List[BatchTimeOperation]] = None,
        batch_transformation_step: Optional[Literal["train", "validation"]] = None,
        **kwargs: Any,
    ) -> _PyTorchDataset:
        """See base class."""
        return _PyTorchDataset(
            data=data,
            target=target,
            selected_cols=selected_cols,
            batch_transforms=batch_transforms,
            batch_transformation_step=batch_transformation_step,
            **kwargs,
        )
