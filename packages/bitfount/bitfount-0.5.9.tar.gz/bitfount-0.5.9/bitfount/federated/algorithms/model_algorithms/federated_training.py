"""Algorithm to train a model remotely and return its parameters."""
from __future__ import annotations

from typing import TYPE_CHECKING, Any, Dict, Mapping, Optional, Tuple, Type, cast

from marshmallow import Schema as MarshmallowSchema
from marshmallow import fields, post_load

from bitfount.data.datasource import DataSource
from bitfount.federated.algorithms.base import _BaseAlgorithmFactory
from bitfount.federated.algorithms.model_algorithms.base import (
    _BaseModelAlgorithm,
    _BaseModelAlgorithmFactory,
    _BaseModellerModelAlgorithm,
    _BaseWorkerModelAlgorithm,
)
from bitfount.federated.logging import _get_federated_logger
from bitfount.federated.shim import BackendTensorShim
from bitfount.hub.api import BitfountHub
from bitfount.types import DistributedModelProtocol, _SerializedWeights, _WeightDict

if TYPE_CHECKING:
    from bitfount.types import _DistributedModelTypeOrReference

logger = _get_federated_logger(__name__)


class _BaseModelTrainingMixIn(_BaseModelAlgorithm):
    """Shared methods/attributes for both modeller and worker."""

    # This is set in the base model algorithm
    model: DistributedModelProtocol

    def __init__(self, **kwargs: Any):
        super().__init__(**kwargs)

    @property
    def epochs(self) -> Optional[int]:
        """Returns model epochs."""
        return self.model.epochs

    @property
    def steps(self) -> Optional[int]:
        """Returns model steps."""
        return self.model.steps

    def get_param_states(self) -> _WeightDict:
        """Returns the current parameters of the underlying model."""
        return self.model.get_param_states()

    def apply_update(self, update: _WeightDict) -> _WeightDict:
        """Applies a parameter update to the underlying model."""
        return self.model.apply_weight_updates([update])

    def update_params(self, params: _WeightDict) -> None:
        """Updates model parameters."""
        return self.model.update_params(params)


class _ModellerSide(
    _BaseModelTrainingMixIn,
    _BaseModellerModelAlgorithm,
):
    """Modeller side of the FederatedModelTraining algorithm."""

    def __init__(
        self,
        *,
        model: DistributedModelProtocol,
        **kwargs: Any,
    ):
        super().__init__(model=model, **kwargs)

    def run(
        self,
        update: Optional[_WeightDict] = None,
        validation_metrics: Optional[Mapping[str, float]] = None,
    ) -> _SerializedWeights:
        """Takes a weight update, applies it and returns the new model parameters."""
        if update is not None:
            self.apply_update(update)
        nn_params: Dict[str, Any] = self.get_param_states()
        backend_tensor_shim: BackendTensorShim = self.model.backend_tensor_shim()
        for name, param in nn_params.items():
            nn_params[name] = backend_tensor_shim.to_list(param)
        if validation_metrics:
            for key, value in validation_metrics.items():
                self.model.log_(key, value, on_epoch=True, prog_bar=True, logger=True)
        return cast(_SerializedWeights, nn_params)


class _WorkerSide(
    _BaseModelTrainingMixIn,
    _BaseWorkerModelAlgorithm,
):
    """Worker side of the FederatedModelTraining algorithm."""

    def __init__(
        self,
        *,
        model: DistributedModelProtocol,
        **kwargs: Any,
    ):
        super().__init__(model=model, **kwargs)

    def run(
        self,
        data: DataSource,
        model_params: _SerializedWeights,
        iterations: int,
    ) -> Tuple[_WeightDict, Optional[Dict[str, str]]]:
        """Takes the model parameters, trains and returns the parameter update."""
        backend_tensor_shim: BackendTensorShim = self.model.backend_tensor_shim()
        for name, param in model_params.items():
            model_params[name] = backend_tensor_shim.to_tensor(param)

        tensor_model_params = cast(_WeightDict, model_params)
        self.update_params(tensor_model_params)

        # Train for one federated round - `iterations` many steps or epochs
        # TODO: [BIT-1228] look into combining these two method calls when we upgrade
        # pytorch lightning
        self.model.set_model_training_iterations(iterations)
        self.model.reset_trainer()
        validation_metrics: Optional[Dict[str, str]] = self.model.fit(data)
        return self.get_param_states(), validation_metrics

    def save_final_parameters(self, model_params: _SerializedWeights) -> None:
        """Saves the final global model parameters.

        Args:
            model_params: The final global model parameters.

        :::note

        This method saves the final global model to a file called `model.pt`.

        :::
        """
        backend_tensor_shim: BackendTensorShim = self.model.backend_tensor_shim()
        for name, param in model_params.items():
            model_params[name] = backend_tensor_shim.to_tensor(param)

        tensor_model_params = cast(_WeightDict, model_params)
        self.update_params(tensor_model_params)
        # TODO: [BIT-1043]: pass filename for serialization
        self.model.serialize("model.pt")


class FederatedModelTraining(
    _BaseModelAlgorithmFactory,
):
    """Algorithm for training a model remotely and returning its updated parameters.

    This algorithm is designed to be compatible with the `FederatedAveraging` protocol.

    Args:
        model: The model to train on remote data.

    Attributes:
        name: The name of the algorithm.
        model: The model to train on remote data.
    """

    def __init__(
        self,
        *,
        model: _DistributedModelTypeOrReference,
        **kwargs: Any,
    ):
        super().__init__(model=model, **kwargs)

    def modeller(self, **kwargs: Any) -> _ModellerSide:
        """Returns the modeller side of the FederatedModelTraining algorithm."""
        model = self._get_model_from_reference()
        return _ModellerSide(model=model, **kwargs)

    def worker(self, hub: BitfountHub, **kwargs: Any) -> _WorkerSide:
        """Returns the worker side of the FederatedModelTraining algorithm.

        Args:
            hub: `BitfountHub` object to use for communication with the hub.
        """
        model = self._get_model_from_reference(hub=hub)
        return _WorkerSide(model=model, **kwargs)

    @staticmethod
    def get_schema(
        model_schema: Type[MarshmallowSchema], **kwargs: Any
    ) -> Type[MarshmallowSchema]:
        """Returns the schema for FederatedModelTraining.

        Args:
            model_schema: The schema for the underlying model.
        """

        class Schema(_BaseAlgorithmFactory._Schema):

            model = fields.Nested(model_schema)

            @post_load
            def recreate_factory(
                self, data: dict, **_kwargs: Any
            ) -> FederatedModelTraining:
                return FederatedModelTraining(**data)

        return Schema
