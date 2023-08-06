"""PyTorch-specific DataLoader implementations."""
from typing import Iterator, List, Optional

import numpy as np
from torch.utils.data import DataLoader as PyTorchDataLoader

from bitfount.backends.pytorch.data.datasets import _PyTorchBaseDataset
from bitfount.data.dataloader import _BitfountDataLoader


class _PyTorchBitfountDataLoader(_BitfountDataLoader):
    """Wraps a PyTorch DataLoader with bitfount functions."""

    def __init__(self, dataset: _PyTorchBaseDataset, batch_size: Optional[int] = None):

        super().__init__(dataset, batch_size)

        # We set both dataloader and dataset, the former to allow length and
        # iteration to work, the latter to allow the get_*_dataframe() methods to work.
        # Explicitly set batch_size to 1 for the dataloader to ensure "batching" still
        # takes place.
        dl_batch_size: int = self.batch_size if self.batch_size else 1
        self.dataloader: PyTorchDataLoader = PyTorchDataLoader(
            dataset, batch_size=dl_batch_size, shuffle=False
        )

    def __iter__(self) -> Iterator[List[np.ndarray]]:
        """Yield a batch of data or a single element if batch_size is None."""
        for batch in self.dataloader:
            yield [x for x in batch]

    def __len__(self) -> int:
        """Number of batches or number of elements if batch size is None."""
        return len(self.dataloader)
