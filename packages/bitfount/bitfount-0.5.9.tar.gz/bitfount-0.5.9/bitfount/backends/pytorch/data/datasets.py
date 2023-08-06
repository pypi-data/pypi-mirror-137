"""PyTorch implementations for Bitfount Dataset classes."""
from abc import ABC
from typing import Any, Sequence, Union, cast

import torch
from torch.utils.data import Dataset as PTDataset

from bitfount.data.datasets import _BaseDataset, _Dataset


class _PyTorchBaseDataset(_BaseDataset, PTDataset, ABC):
    """Base class for tagging and ensuring all abstract methods are implemented."""

    @staticmethod
    def _index_tensor_handler(
        idx: Union[int, Sequence[int], torch.Tensor]
    ) -> Union[int, Sequence[int]]:
        """If the index is a torch tensor, converts it to a list."""
        if torch.is_tensor(idx):
            idx = cast(torch.Tensor, idx)
            list_idx: list = idx.tolist()
            return list_idx
        else:
            idx = cast(Union[int, Sequence[int]], idx)
            return idx


class _PyTorchDataset(_Dataset, _PyTorchBaseDataset):
    """Pytorch prediction dataset."""

    def __getitem__(self, idx: Union[int, Sequence[int], torch.Tensor]) -> Any:
        idx = self._index_tensor_handler(idx)
        return super().__getitem__(idx)
