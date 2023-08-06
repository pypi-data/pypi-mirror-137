"""Data factory classes.

Factory design patterns for producing datasets and dataloaders.
"""
from abc import ABC, abstractmethod
from typing import Any, List, Literal, Mapping, Optional, Union

import pandas as pd

from bitfount.config import _BASIC_ENGINE, _PYTORCH_ENGINE, BITFOUNT_ENGINE
from bitfount.data.dataloader import _BitfountDataLoader
from bitfount.data.datasets import _BaseDataset, _Dataset
from bitfount.data.types import _SemanticTypeValue
from bitfount.exceptions import BitfountEngineError
from bitfount.transformations.batch_operations import BatchTimeOperation


class _DataFactory(ABC):
    """A factory for producing dataset and dataloader instances."""

    def __init__(self, *args: Any, **kwargs: Any):
        pass

    @abstractmethod
    def create_dataloader(
        self, data: _BaseDataset, batch_size: Optional[int] = None
    ) -> _BitfountDataLoader:
        """Creates a dataloader as specified by this factory.

        Args:
            data: The dataset that should be loaded.
            batch_size: The batch size that the dataloader should output.

        Returns:
            A BitfountDataLoader instance.
        """
        raise NotImplementedError

    @abstractmethod
    def create_dataset(
        self,
        data: pd.DataFrame,
        selected_cols: Mapping[_SemanticTypeValue, List[str]],
        target: Optional[Union[str, List[str]]] = None,
        batch_transforms: Optional[List[BatchTimeOperation]] = None,
        batch_transformation_step: Optional[Literal["train", "validation"]] = None,
        **kwargs: Any,
    ) -> _Dataset:
        """Creates a dataset for prediction tasks.

        Args:
            data: The data to wrap in a dataset.
            target: The dependent variable name.
            selected_cols: A mapping of semantic types and column names.
            batch_transforms: A list of transformations to be applied at batch time.
            batch_transformation_step: The step for which batch transformations should
                be applied.
            **kwargs: Any
        """
        raise NotImplementedError


class _BasicDataFactory(_DataFactory):
    """A basic DataFactory implementation using core dataset and dataloaders."""

    def create_dataloader(
        self, data: _BaseDataset, batch_size: Optional[int] = None
    ) -> _BitfountDataLoader:
        """See base class."""
        return _BitfountDataLoader(data, batch_size)

    def create_dataset(
        self,
        data: pd.DataFrame,
        selected_cols: Mapping[_SemanticTypeValue, List[str]],
        target: Optional[Union[str, List[str]]] = None,
        batch_transforms: Optional[List[BatchTimeOperation]] = None,
        batch_transformation_step: Optional[Literal["train", "validation"]] = None,
        **kwargs: Any,
    ) -> _Dataset:
        """See base class."""
        return _Dataset(
            data=data,
            target=target,
            selected_cols=selected_cols,
            batch_transforms=batch_transforms,
            batch_transformation_step=batch_transformation_step,
            **kwargs,
        )


def _load_default_data_factory(*args: Any, **kwargs: Any) -> _DataFactory:
    """Create a DataFactory instance as specified by the backend engine.

    Args:
        *args: positional arguments, passed to the DataFactory constructor.
        **kwargs: keyword arguments, passed to the DataFactory constructor.

    Returns:
        The created DataFactory instance.

    Raises:
        BitfountEngineError: if there is an import issue in loading the backend.
    """
    if BITFOUNT_ENGINE == _PYTORCH_ENGINE:
        try:
            from bitfount.backends.pytorch.data.datafactory import _PyTorchDataFactory

            return _PyTorchDataFactory(*args, **kwargs)
        except ImportError:
            raise BitfountEngineError(
                "An error was encountered trying to load the pytorch engine; "
                "check pytorch is installed."
            )
    elif BITFOUNT_ENGINE == _BASIC_ENGINE:
        return _BasicDataFactory(*args, **kwargs)
    else:
        raise BitfountEngineError(f"Unable to load engine {BITFOUNT_ENGINE}.")
