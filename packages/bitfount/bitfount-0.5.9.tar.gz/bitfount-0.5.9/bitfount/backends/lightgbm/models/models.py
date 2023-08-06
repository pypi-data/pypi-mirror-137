"""Models using LightGBM as the backend."""
from __future__ import annotations

from typing import Any, Type

from marshmallow import post_load

from bitfount.backends.lightgbm.models.base_models import BaseLGBMRandomForest
from bitfount.models.base_models import ClassifierMixIn, RegressorMixIn
from bitfount.types import _JSONDict


class LGBMRandomForestClassifier(ClassifierMixIn, BaseLGBMRandomForest):
    """LGBM Classifier for Random Forests and GBMs.

    Currently only supports binary classification.
    """

    def __init__(self, **kwargs: Any):
        super().__init__(**kwargs)
        self._set_objective()
        self._set_training_metrics()
        self.set_number_of_classes()

    def _set_objective(self) -> None:
        self.objective: str = "binary"

    def _set_training_metrics(self) -> None:
        self.training_metrics = ["binary_logloss", "auc"]

    class _Schema(BaseLGBMRandomForest._Schema, ClassifierMixIn._Schema):
        @post_load
        def recreate_model(
            self, data: _JSONDict, **kwargs: Any
        ) -> LGBMRandomForestClassifier:
            """Recreate LGBM Classifier."""
            return LGBMRandomForestClassifier(**data)

    @classmethod
    def get_schema(cls) -> Type[LGBMRandomForestClassifier._Schema]:
        """Get the model schema."""
        return cls._Schema


class LGBMRandomForestRegressor(RegressorMixIn, BaseLGBMRandomForest):
    """LGBM Regressor for Random Forests and GBMs."""

    def __init__(self, **kwargs: Any):
        super().__init__(**kwargs)
        self._set_objective()
        self._set_training_metrics()

    def _set_objective(self) -> None:
        self.objective = "regression"

    def _set_training_metrics(self) -> None:
        self.training_metrics = ["mae", "mse", "rmse"]

    class _Schema(BaseLGBMRandomForest._Schema):
        @post_load
        def recreate_model(
            self, data: _JSONDict, **kwargs: Any
        ) -> LGBMRandomForestRegressor:
            """Recreate LGBM Regressor."""
            return LGBMRandomForestRegressor(**data)

    @classmethod
    def get_schema(cls) -> Type[LGBMRandomForestRegressor._Schema]:
        """Get the model schema."""
        return cls._Schema
