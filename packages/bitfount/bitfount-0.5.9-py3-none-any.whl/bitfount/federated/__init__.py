"""Manages the federated communication and training of models."""
from typing import List

from bitfount.federated.aggregators.aggregator import Aggregator
from bitfount.federated.aggregators.secure import SecureAggregator
from bitfount.federated.algorithms.column_avg import ColumnAverage
from bitfount.federated.algorithms.model_algorithms.evaluate import ModelEvaluation
from bitfount.federated.algorithms.model_algorithms.federated_training import (
    FederatedModelTraining,
)
from bitfount.federated.algorithms.model_algorithms.train_and_evaluate import (
    ModelTrainingAndEvaluation,
)
from bitfount.federated.authorisation_checkers import IdentityVerificationMethod
from bitfount.federated.early_stopping import FederatedEarlyStopping
from bitfount.federated.exceptions import (
    BitfountTaskStartError,
    MessageHandlerNotFoundError,
    MessageRetrievalError,
    PodConnectFailedError,
    PodRegistrationError,
    SecureShareError,
)
from bitfount.federated.model_reference import BitfountModelReference
from bitfount.federated.modeller import Modeller
from bitfount.federated.pod import Pod
from bitfount.federated.pod_keys_setup import PodKeys
from bitfount.federated.privacy.differential import DPModellerConfig, DPPodConfig
from bitfount.federated.protocols.fed_avg import FederatedAveraging
from bitfount.federated.protocols.results_only import ResultsOnly
from bitfount.federated.roles import Role
from bitfount.federated.secure import SecureShare
from bitfount.federated.shim import BackendTensorShim
from bitfount.federated.transport import MAXIMUM_GRPC_MESSAGE_SIZE_BYTES
from bitfount.federated.transport.config import (
    PRODUCTION_MESSAGE_SERVICE_URL,
    MessageServiceConfig,
)
from bitfount.federated.types import AggregatorType, AlgorithmType, ProtocolType

__all__: List[str] = [
    "Aggregator",
    "AggregatorType",
    "AlgorithmType",
    "BackendTensorShim",
    "BitfountModelReference",
    "BitfountTaskStartError",
    "ColumnAverage",
    "DPModellerConfig",
    "DPPodConfig",
    "FederatedAveraging",
    "FederatedEarlyStopping",
    "FederatedModelTraining",
    "IdentityVerificationMethod",
    "MAXIMUM_GRPC_MESSAGE_SIZE_BYTES",
    "MessageHandlerNotFoundError",
    "MessageRetrievalError",
    "MessageServiceConfig",
    "ModelEvaluation",
    "ModelTrainingAndEvaluation",
    "Modeller",
    "Pod",
    "PodConnectFailedError",
    "PodKeys",
    "PodRegistrationError",
    "ProtocolType",
    "PRODUCTION_MESSAGE_SERVICE_URL",
    "ResultsOnly",
    "Role",
    "SecureAggregator",
    "SecureShare",
    "SecureShareError",
]

# See top level `__init__.py` for an explanation
__pdoc__ = {}
for _obj in __all__:
    __pdoc__[_obj] = False
