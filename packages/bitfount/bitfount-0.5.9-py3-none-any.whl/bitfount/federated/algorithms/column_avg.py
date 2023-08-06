"""Column averaging algorithm."""
from __future__ import annotations

import os
from typing import Any, Dict, List, Optional, Type, Union

from marshmallow import Schema as MarshmallowSchema
from marshmallow import post_load
import numpy as np

from bitfount.data.datasource import DataSource
from bitfount.federated.algorithms.base import (
    _BaseAlgorithmFactory,
    _BaseAlgorithmSchema,
    _BaseModellerAlgorithm,
    _BaseWorkerAlgorithm,
)
from bitfount.federated.logging import _get_federated_logger
from bitfount.federated.privacy.differential import DPPodConfig

logger = _get_federated_logger(__name__)


class _ModellerSide(_BaseModellerAlgorithm):
    """Modeller side of the ColumnAverage algorithm."""

    def initialise(
        self,
        pretrained_file: Optional[Union[str, os.PathLike]] = None,
        **kwargs: Any,
    ) -> None:
        """Nothing to initialise here."""
        pass

    def run(self, results: List[Dict[str, float]]) -> List[Dict[str, float]]:
        """Simply returns results."""
        return results


class _WorkerSide(_BaseWorkerAlgorithm):
    """Worker side of the ColumnAverage algorithm."""

    def __init__(self, *, field: str, **kwargs: Any) -> None:
        self.datasource: DataSource
        self.field = field
        super().__init__(**kwargs)

    def initialise(
        self,
        datasource: DataSource,
        pod_dp: Optional[DPPodConfig] = None,
        **kwargs: Any,
    ) -> None:
        """Sets Datasource."""
        self.datasource = datasource

    def run(self) -> Dict[str, float]:
        """Returns the mean of the field in `DataSource` dataframe."""
        mean = np.mean(self.datasource.data[self.field], dtype=np.float64)
        return {"mean": float(mean)}


class ColumnAverage(_BaseAlgorithmSchema, _BaseAlgorithmFactory):
    """Simple algorithm for taking the arithmetic mean of a column in a table.

    Args:
        field: The name of the column to take the mean of.

    Attributes:
        name: The name of the algorithm.
        field: The name of the column to take the mean of.
    """

    def __init__(self, field: str):
        super().__init__()
        self.field = field

    def modeller(self, **kwargs: Any) -> _ModellerSide:
        """Returns the modeller side of the ColumnAverage algorithm."""
        return _ModellerSide(**kwargs)

    def worker(self, **kwargs: Any) -> _WorkerSide:
        """Returns the worker side of the ColumnAverage algorithm."""
        return _WorkerSide(field=self.field, **kwargs)

    @staticmethod
    def get_schema(**kwargs: Any) -> Type[MarshmallowSchema]:
        """Returns the schema for ColumnAverage."""

        class Schema(_BaseAlgorithmFactory._Schema):
            @post_load
            def recreate_factory(self, data: dict, **_kwargs: Any) -> ColumnAverage:
                return ColumnAverage(**data)

        return Schema
