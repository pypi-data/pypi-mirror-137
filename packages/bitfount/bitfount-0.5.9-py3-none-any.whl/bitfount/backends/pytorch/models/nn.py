"""Neural Network classes and helper functions for PyTorch."""
from abc import ABC
from typing import Any, Iterable, List, Tuple, Type, Union, cast

import torch
import torch.nn as nn
import torchvision.models as tv_models

from bitfount.backends.pytorch.models.torch_functions.mish import Mish
from bitfount.models.nn import _ConvNeuralNet, _FeedForwardNeuralNet, _NeuralNet

TORCHVISION_CLASSIFICATION_MODELS = {
    name: func
    for name, func in vars(tv_models).items()
    if callable(func) and not isinstance(func, type)
}


class _PyTorchNeuralNet(nn.Module, _NeuralNet, ABC):
    """Base abstract class for all PyTorch-implemented neural networks."""

    pass


class _PyTorchConvNeuralNet(_PyTorchNeuralNet, _ConvNeuralNet):
    """Simple convolutional neural network architecture in PyTorch."""

    def __init__(
        self,
        layer_sizes: Iterable[Tuple[int, int]],
        dropout_probs: List[float],
        mish: bool,
        head_sizes: Iterable[Tuple[int, int]],
        ff_layer_sizes: Iterable[Tuple[int, int]],
        ff_dropout_probs: List[float],
        kernel_size: int,
        padding: int,
        stride: int,
        pooling_function: str,
    ):
        super().__init__()
        # CONVOLUTIONAL BLOCKS
        self.layers = nn.ModuleList(
            [
                nn.Conv2d(
                    in_, out_, kernel_size=kernel_size, stride=stride, padding=padding
                )
                for in_, out_ in layer_sizes
            ]
        )
        activation_function = Mish if mish else nn.ReLU
        self.activations = nn.ModuleList([activation_function() for _ in layer_sizes])
        self.batch_norms = nn.ModuleList(
            [nn.BatchNorm2d(size) for _, size in layer_sizes]
        )
        self.dropouts = nn.ModuleList([nn.Dropout2d(i) for i in dropout_probs])
        pooling_module: Union[Type[nn.AvgPool2d], Type[nn.MaxPool2d]]
        if pooling_function == "max":
            pooling_module = nn.MaxPool2d
        elif pooling_function == "avg":
            pooling_module = nn.AvgPool2d

        self.pooling_functions = nn.ModuleList(
            [pooling_module(kernel_size=2) for _ in layer_sizes]
        )

        # FEEDFORWARD LAYERS
        self.ff_layers = nn.ModuleList(
            [nn.Linear(in_, out_) for in_, out_ in ff_layer_sizes]
        )
        self.ff_activations = nn.ModuleList(
            [activation_function() for _ in ff_layer_sizes]
        )
        self.ff_batch_norms = nn.ModuleList(
            [nn.BatchNorm1d(size) for _, size in ff_layer_sizes]
        )
        self.ff_dropouts = nn.ModuleList([nn.Dropout(i) for i in ff_dropout_probs])

        # OUTPUT LAYER
        self.heads = nn.ModuleList([nn.Linear(in_, out_) for in_, out_ in head_sizes])

    def forward(self, x: torch.Tensor) -> Tuple[torch.Tensor, ...]:
        """Forward pass in model."""
        for layer, activation, batchnorm, dropout, pooling_function in zip(
            self.layers,
            self.activations,
            self.batch_norms,
            self.dropouts,
            self.pooling_functions,
        ):
            x = layer(x)
            x = activation(x)
            x = batchnorm(x)
            x = dropout(x)
            x = pooling_function(x)

        x = x.view(x.size(0), -1)

        for layer, activation, batchnorm, dropout in zip(
            self.ff_layers, self.ff_activations, self.ff_batch_norms, self.ff_dropouts
        ):
            x = layer(x)
            x = activation(x)
            x = batchnorm(x)
            x = dropout(x)

        return tuple(head(x) for head in self.heads)


class _PyTorchFeedForwardNeuralNet(_PyTorchNeuralNet, _FeedForwardNeuralNet):
    """Simple feedforward neural network architecture in PyTorch."""

    def __init__(
        self,
        embedding_sizes: Iterable[Tuple[int, int]],
        emb_dropout: float,
        n_cont: int,
        layer_sizes: Iterable[Tuple[int, int]],
        dropout_probs: List[float],
        mish: bool,
        head_sizes: Iterable[Tuple[int, int]],
    ):
        super().__init__()

        # INPUT LAYER
        self.embeddings = nn.ModuleList(
            [nn.Embedding(categories, size) for categories, size in embedding_sizes]
        )
        self.emb_drop = nn.Dropout(emb_dropout)
        self.bn_cont = nn.BatchNorm1d(n_cont)
        self.n_cont = n_cont
        # HIDDEN LAYERS
        self.layers = nn.ModuleList([nn.Linear(in_, out_) for in_, out_ in layer_sizes])
        activation_function = Mish if mish else nn.ReLU
        self.activations = nn.ModuleList([activation_function() for _ in layer_sizes])
        self.batch_norms = nn.ModuleList(
            [nn.BatchNorm1d(size) for _, size in layer_sizes]
        )
        self.dropouts = nn.ModuleList([nn.Dropout(i) for i in dropout_probs])

        # OUTPUT LAYER
        self.heads = nn.ModuleList([nn.Linear(in_, out_) for in_, out_ in head_sizes])

    def forward(self, x: torch.Tensor) -> Tuple[torch.Tensor, ...]:
        """Forward pass in model."""
        x_cat, x_cont = x
        if x_cont.nelement() != 0 and x_cat.nelement() != 0:
            fwd_pass_cat = [
                cast(torch.Tensor, embedding(x_cat[idx]))
                for idx, embedding in enumerate(self.embeddings)
            ]
            fwd_pass = torch.cat(fwd_pass_cat, 1)
            fwd_pass = self.emb_drop(fwd_pass)
            fwd_pass2 = self.bn_cont(x_cont)
            fwd_pass = torch.cat([fwd_pass, fwd_pass2], 1)
        elif x_cont.nelement() != 0:
            fwd_pass = self.bn_cont(x_cont)
        elif x_cat.nelement() != 0:
            fwd_pass_cat = [
                cast(torch.Tensor, embedding(x_cat[idx]))
                for idx, embedding in enumerate(self.embeddings)
            ]
            fwd_pass = torch.cat(fwd_pass_cat, 1)
            fwd_pass = self.emb_drop(fwd_pass)

        for layer, activation, batchnorm, dropout in zip(
            self.layers, self.activations, self.batch_norms, self.dropouts
        ):
            fwd_pass = layer(fwd_pass)
            fwd_pass = activation(fwd_pass)
            fwd_pass = batchnorm(fwd_pass)
            fwd_pass = dropout(fwd_pass)

        return tuple(head(fwd_pass) for head in self.heads)


def _get_torchvision_classification_model(
    model_name: str, pretrained: bool, num_classes: int, **kwargs: Any
) -> nn.Module:
    """Returns a pre-existing torchvision model.

    This function returns the torchvision classification model corresponding to
    `model_name`. Importantly, it resizes the final layer to make it appropriate
    for the task. Since this is different for every model, this must be hard-coded

    Adapted from pytorch docs/tutorials
    """
    # Convert model name for consistency
    model_name = model_name.lower()

    if "resnet" in model_name:
        model = TORCHVISION_CLASSIFICATION_MODELS[model_name](
            pretrained=pretrained, **kwargs
        )
        num_ftrs = model.fc.in_features
        model.fc = nn.Linear(num_ftrs, num_classes)
    elif ("alexnet" in model_name) or ("vgg" in model_name):
        model = TORCHVISION_CLASSIFICATION_MODELS[model_name](
            pretrained=pretrained, **kwargs
        )
        num_ftrs = model.classifier[6].in_features
        model.classifier[6] = nn.Linear(num_ftrs, num_classes)
    elif "squeezenet" in model_name:
        model = TORCHVISION_CLASSIFICATION_MODELS[model_name](
            pretrained=pretrained, **kwargs
        )
        model.classifier[1] = nn.Conv2d(
            512, num_classes, kernel_size=(1, 1), stride=(1, 1)
        )
        model.num_classes = num_classes
    elif "densenet" in model_name:
        model = TORCHVISION_CLASSIFICATION_MODELS[model_name](
            pretrained=pretrained, **kwargs
        )
        num_ftrs = model.classifier.in_features
        model.classifier = nn.Linear(num_ftrs, num_classes)
    elif model_name in TORCHVISION_CLASSIFICATION_MODELS:
        raise ValueError("Model reshaping not implemented yet. Choose another model.")
    else:
        raise ValueError("Model name not recognised")

    return cast(nn.Module, model)
