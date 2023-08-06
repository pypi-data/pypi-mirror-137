"""PyTorch implementations for the Bitfount framework."""

from typing import List

from bitfount.backends.pytorch.federated.models import PyTorchBackendTensorShim
from bitfount.backends.pytorch.models.base_models import PyTorchClassifierMixIn
from bitfount.backends.pytorch.models.bitfount_model import PyTorchBitfountModel
from bitfount.backends.pytorch.models.models import (
    PyTorchImageClassifier,
    PyTorchTabularClassifier,
    TabNetClassifier,
)
from bitfount.backends.pytorch.models.torch_functions.mish import Mish
from bitfount.backends.pytorch.utils import LoggerType

__all__: List[str] = [
    "LoggerType",
    "Mish",
    "PyTorchBackendTensorShim",
    "PyTorchBitfountModel",
    "PyTorchClassifierMixIn",
    "PyTorchImageClassifier",
    "PyTorchTabularClassifier",
    "TabNetClassifier",
]

# See top level `__init__.py` for an explanation
__pdoc__ = {}
for _obj in __all__:
    __pdoc__[_obj] = False
