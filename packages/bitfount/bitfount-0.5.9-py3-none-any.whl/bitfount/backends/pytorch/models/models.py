"""Model implementations using PyTorch."""
from __future__ import annotations

import logging
from typing import Any, List, Optional, Tuple, Type, Union, cast

from marshmallow import post_load
import pandas as pd
from pytorch_tabnet.tab_model import TabNetClassifier as TabNetClassifier_
import torch
from torch import nn as nn

from bitfount.backends.pytorch.models.base_models import (
    _OPTIMIZERS,
    _SCHEDULERS,
    BasePyTorchModel,
    BaseTabNetModel,
    PyTorchClassifierMixIn,
    _calculate_embedding_sizes,
)
from bitfount.backends.pytorch.models.nn import (
    _get_torchvision_classification_model,
    _PyTorchConvNeuralNet,
    _PyTorchFeedForwardNeuralNet,
)
from bitfount.backends.pytorch.types import (
    ImgAndTabDataSplit,
    ImgDataReturnType,
    ImgFwdTypes,
    ImgXorTabDataSplit,
    TabDataReturnType,
)
from bitfount.data.types import SemanticType
from bitfount.models.base_models import (
    CNNModelStructure,
    FeedForwardModelStructure,
    NeuralNetworkModelStructure,
    NeuralNetworkPredefinedModel,
    Scheduler,
)
from bitfount.types import _JSONDict
from bitfount.utils import DEFAULT_SEED

logger = logging.getLogger(__name__)


class PyTorchImageClassifier(PyTorchClassifierMixIn, BasePyTorchModel):
    """A Pytorch model designed specifically for image classification problems.

    The model can handle binary, multiclass and multilabel classification problems.

    Raises:
        ValueError: If the model structure is not an instance of `CNNModelStructure` or
            `NeuralNetworkPredefinedModel`.
        ValueError: If the loss function is not `nn.BCEWithLogitsLoss` or
            `nn.CrossEntropyLoss`.

    :::info

    Currently images are scaled to 224 x 224.

    :::
    """

    input_dim: int = 224  # default input images are 224 x 224

    def __init__(self, **kwargs: Any):
        model_structure = kwargs.pop("model_structure", CNNModelStructure())
        if not isinstance(
            model_structure, (CNNModelStructure, NeuralNetworkPredefinedModel)
        ):
            raise ValueError("Model structure does not match model")

        super().__init__(model_structure=model_structure, **kwargs)

        if self.loss_func is None:
            if self.multilabel:
                self.loss_func = nn.BCEWithLogitsLoss
            else:
                self.loss_func = nn.CrossEntropyLoss
        elif self.loss_func not in [nn.BCEWithLogitsLoss, nn.CrossEntropyLoss]:
            raise ValueError("This loss function is not currently supported")

    def forward(self, x: ImgFwdTypes) -> Any:  # type: ignore[override] # Reason: see below # noqa: B950
        """Performs a forward pass of the model."""
        # override as the forward function is incompatible with pl.LightningModule
        if self.datastructure.number_of_images > 1:
            aux = []
            for i in range(len(x)):
                aux.append(self._model(x[i]))  # type: ignore[misc] # reason: model should be initialised already # noqa: B950
            return torch.cat([item[0] for item in aux], 1)
        else:
            return self._model(x)  # type: ignore[misc] # reason: model should be initialised already # noqa: B950

    def _split_dataloader_output(
        self,
        data: Union[
            ImgAndTabDataSplit,
            ImgXorTabDataSplit,
        ],
    ) -> Union[ImgDataReturnType, TabDataReturnType]:
        """Splits dataloader output into image tensor, weights and category."""
        images, sup = cast(Tuple[torch.Tensor, torch.Tensor], data)
        weights = sup[:, 0].float()
        category: Optional[torch.Tensor]
        if sup.shape[1] > 2:
            category = sup[:, -1:].long()
        else:
            category = None

        return images, weights, category

    def _get_convolution_final_output_dimension(self) -> int:
        """Calculates the output size of the final convolutional layer.

        This will become the input size of the first feedforward layer
        """
        input_dim: float = self.input_dim
        if isinstance(self.model_structure, CNNModelStructure):
            # self.model_structure.layers is set in post_init, so we can just cast
            for _ in cast(List[int], self.model_structure.layers):
                output_dim = self._get_convolution_output_dimension(
                    input_dim,
                    self.model_structure.kernel_size,
                    self.model_structure.padding,
                    self.model_structure.stride,
                )
                output_dim = output_dim / 2  # due to pooling
                input_dim = output_dim

            return int(
                (output_dim**2) * cast(List[int], self.model_structure.layers)[-1]
            )
        else:
            raise TypeError("This method only works with the cnn model structure.")

    @staticmethod
    def _get_convolution_output_dimension(
        input_size: Union[int, float], kernel_size: int, padding: int, stride: int
    ) -> float:
        """Gets convolution output dimension."""
        return ((input_size - kernel_size + (2 * padding)) / stride) + 1

    def _create_model(self) -> nn.Module:
        """Creates the model to use.

        If `self.model_structure` is a `NeuralNetworkPredefinedModel`, then calls
        `get_torchvision_classification_model` to adapt model head for the task
        before returning the model

        Otherwise, creates model as defined by `CNNModelStructure`
        """
        self.set_number_of_classes()
        if isinstance(self.model_structure, NeuralNetworkPredefinedModel):
            kwargs = self.model_structure.kwargs or {}
            model = _get_torchvision_classification_model(
                self.model_structure.name,
                self.model_structure.pretrained,
                self.n_classes,
                **kwargs,
            )
        elif isinstance(self.model_structure, CNNModelStructure):
            # self.model_structure.layers is set in post_init, so we can just cast
            layer_sizes = self._get_layer_sizes(
                cast(List[int], self.model_structure.layers), 3
            )

            head_sizes = [
                (self.model_structure.ff_layers[-1], self.n_classes)
                for _ in range(self.model_structure.num_heads)
            ]
            ff_layer_sizes = self._get_layer_sizes(
                self.model_structure.ff_layers,
                self._get_convolution_final_output_dimension(),
            )
            # self.model_structure.dropout_probs is set in post_init,
            # so we can just cast below
            logger.debug(f"Creating model with {self.model_structure.num_heads} heads")
            model = _PyTorchConvNeuralNet(
                layer_sizes,
                cast(List[float], self.model_structure.dropout_probs),
                self.model_structure.mish_activation_function,
                head_sizes,
                ff_layer_sizes,
                self.model_structure.ff_dropout_probs,
                self.model_structure.kernel_size,
                self.model_structure.padding,
                self.model_structure.stride,
                self.model_structure.pooling_function,
            )
        return model

    class _Schema(BasePyTorchModel._Schema, PyTorchClassifierMixIn._Schema):
        @post_load
        def recreate_model(
            self, data: _JSONDict, **kwargs: Any
        ) -> PyTorchImageClassifier:
            """Recreates a PyTorchImageClassifier."""
            return PyTorchImageClassifier(**data)

    @classmethod
    def get_schema(cls) -> Type[PyTorchImageClassifier._Schema]:
        """Returns the Schema for the model."""
        return cls._Schema


class PyTorchTabularClassifier(PyTorchClassifierMixIn, BasePyTorchModel):
    """A Pytorch model designed specifically for tabular classification problems.

    The model can handle binary, multiclass and multilabel classification problems.

    Raises:
        ValueError: If the model structure is not an instance of
            `FeedForwardModelStructure`.
        ValueError: If the loss function is not `nn.BCEWithLogitsLoss` or
            `nn.CrossEntropyLoss`.
    """

    def __init__(self, **kwargs: Any):
        model_structure = kwargs.pop("model_structure", FeedForwardModelStructure())
        if (
            isinstance(model_structure, NeuralNetworkPredefinedModel)
            and model_structure.name == "TabNet"
        ):
            raise ValueError("Please create a TabNetClassifier directly.")
        elif not isinstance(model_structure, FeedForwardModelStructure):
            raise ValueError("Please provide a FeedForwardModelStructure")
        super().__init__(
            model_structure=cast(NeuralNetworkModelStructure, model_structure),
            **kwargs,
        )
        if self.loss_func is None:
            if hasattr(self, "multilabel") and (self.multilabel is not False):

                self.loss_func = nn.BCEWithLogitsLoss
            else:
                self.loss_func = nn.CrossEntropyLoss
        elif self.loss_func not in [nn.BCEWithLogitsLoss, nn.CrossEntropyLoss]:
            raise ValueError("This loss function is not currently supported")

    def _create_model(self) -> _PyTorchFeedForwardNeuralNet:
        """Creates model to use.

        Takes number of continuous features and number of heads. Creates and
        returns model.
        """
        self.set_number_of_classes()
        ignore_cols_for_training = self.datastructure.get_columns_ignored_for_training()
        num_continuous = len(
            [
                col
                for col in self.schema.feature_names(SemanticType.CONTINUOUS)
                if col not in ignore_cols_for_training
            ]
        )
        embedding_sizes = _calculate_embedding_sizes(
            self.schema.categorical_feature_sizes(ignore_cols_for_training)
        )
        self.model_structure = cast(FeedForwardModelStructure, self.model_structure)
        num_heads = self.model_structure.num_heads
        num_categorical = sum(size for _, size in embedding_sizes)
        # self.model_structure.layers is set in post_init, so we can just cast
        layer_sizes = self._get_layer_sizes(
            cast(
                List[int],
                self.model_structure.layers,
            ),
            num_continuous + num_categorical,
        )
        head_sizes = [
            (
                cast(
                    List[int],
                    self.model_structure.layers,
                )[-1],
                self.n_classes,
            )
            for _ in range(num_heads)
        ]
        logger.debug(f"Creating model with {num_heads} heads")
        # self.model_structure.dropout probs is set in post_init,
        # so we can just cast below
        model = _PyTorchFeedForwardNeuralNet(
            embedding_sizes,
            self.model_structure.embedding_dropout,
            num_continuous,
            layer_sizes,
            cast(
                List[float],
                self.model_structure.dropout_probs,
            ),
            self.model_structure.mish_activation_function,
            head_sizes,
        )
        return model

    def _split_dataloader_output(
        self,
        data: Union[
            ImgAndTabDataSplit,
            ImgXorTabDataSplit,
        ],
    ) -> Union[ImgDataReturnType, TabDataReturnType]:
        """Splits dataloader output.

        Splits it into pieces for categorical, continuous, weights and categories.

        NB: `ignore_classes` is never returned
        """
        tab, sup = cast(ImgXorTabDataSplit, data)
        ignore_cols_for_training = self.datastructure.get_columns_ignored_for_training()
        n_cat = len(
            _calculate_embedding_sizes(
                self.schema.categorical_feature_sizes(ignore_cols_for_training)
            )
        )
        n_cont = len(
            [
                col
                for col in self.schema.feature_names(SemanticType.CONTINUOUS)
                if col not in ignore_cols_for_training
            ]
        )
        # Get items according to the order they are in the tensor
        cat_pos = n_cat
        cont_pos = cat_pos + n_cont
        x_1 = tab[:, :cat_pos].long()  # categorical features
        x_2 = tab[:, cat_pos:cont_pos].float()  # continuous features
        weights = sup[:, 0].float()
        # If category is present, return it, otherwise return None
        category: Optional[torch.Tensor]
        if sup.shape[1] > 2:
            category = sup[:, -1:].long()
        else:
            category = None
        return (x_1.t(), x_2), weights, category

    class _Schema(BasePyTorchModel._Schema, PyTorchClassifierMixIn._Schema):
        @post_load
        def recreate_model(
            self, data: _JSONDict, **kwargs: Any
        ) -> PyTorchTabularClassifier:
            """Recreates a PyTorchTabularClassifier."""
            return PyTorchTabularClassifier(**data)

    @classmethod
    def get_schema(cls) -> Type[PyTorchTabularClassifier._Schema]:
        """Returns the Schema for the model."""
        return cls._Schema


class TabNetClassifier(PyTorchClassifierMixIn, BaseTabNetModel):
    """TabNet Classifier for binary and multiclass tabular classification problems.

    See base class for more information.
    """

    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs)

    def _create_model(self) -> TabNetClassifier_:
        """Create model for Binary or Multiclass classification."""
        self.set_number_of_classes()
        ignore_cols_for_training = self.datastructure.get_columns_ignored_for_training()
        # Only consider the tabular part
        X: pd.DataFrame
        if isinstance(self.train_dl.get_x_dataframe(), tuple):
            X, _ = self.train_dl.get_x_dataframe()
        elif isinstance(self.train_dl.get_x_dataframe(), pd.DataFrame):
            X = cast(pd.DataFrame, self.train_dl.get_x_dataframe())
        cat_idxs = [
            i
            for i, f in enumerate(X.columns)
            if f in self.schema.feature_names(SemanticType.CATEGORICAL)
            if f not in ignore_cols_for_training
        ]

        if self.embedding_sizes is None:
            embedding_sizes = _calculate_embedding_sizes(
                self.schema.categorical_feature_sizes(ignore_cols_for_training)
            )
            self.embedding_sizes = cast(List[int], [i[1] for i in embedding_sizes])
        return TabNetClassifier_(
            cat_idxs=cat_idxs,
            cat_dims=self.schema.categorical_feature_sizes(
                ignore_cols=ignore_cols_for_training
            ),
            cat_emb_dim=self.embedding_sizes,
            optimizer_fn=_OPTIMIZERS[self.optimizer.name],
            optimizer_params=self.optimizer.params,
            scheduler_params=cast(Scheduler, self.scheduler).params,
            scheduler_fn=_SCHEDULERS[cast(Scheduler, self.scheduler).name],
            mask_type=self.mask_type,
            seed=self.seed or DEFAULT_SEED,
        )

    class _Schema(BaseTabNetModel._Schema, PyTorchClassifierMixIn._Schema):
        @post_load
        def recreate_model(self, data: _JSONDict, **kwargs: Any) -> TabNetClassifier:
            """Recreate TabNetClassifier model."""
            return TabNetClassifier(**data)

    @classmethod
    def get_schema(cls) -> Type[TabNetClassifier._Schema]:
        """Returns the Schema for the model."""
        return cls._Schema
