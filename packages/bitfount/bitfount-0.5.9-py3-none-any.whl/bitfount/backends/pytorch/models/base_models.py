"""Base models and helper classes using PyTorch as the backend."""
from __future__ import annotations

from abc import abstractmethod
import contextlib
from functools import partial
import inspect
from itertools import chain
import logging
import os
from typing import (
    Any,
    Callable,
    Dict,
    Generic,
    Iterator,
    List,
    Literal,
    MutableMapping,
    Optional,
    Tuple,
    Type,
    TypeVar,
    Union,
    cast,
)

from marshmallow import fields
import numpy as np
from opacus import PrivacyEngine
from opacus.dp_model_inspector import DPModelInspector, IncompatibleModuleException
from opacus.utils import module_modification
import pandas as pd
import pytorch_lightning as pl
from pytorch_lightning.callbacks.early_stopping import EarlyStopping
from pytorch_lightning.loggers import LightningLoggerBase, TensorBoardLogger
import pytorch_tabnet as tabnet
import torch
from torch import Tensor
from torch import nn as nn

# Convention is to import functional as F
# noinspection PyPep8Naming
from torch.nn import functional as F
import torch.optim as optimizers
import torch.optim.lr_scheduler as schedulers
from torch.utils.data import DataLoader
import torch_optimizer as torch_optimizers

from bitfount.backends.pytorch.data.datafactory import _PyTorchDataFactory
from bitfount.backends.pytorch.federated.models import _PyTorchDistributedModelMixIn
from bitfount.backends.pytorch.types import (
    ImgAndTabBatch,
    ImgAndTabDataSplit,
    ImgDataReturnType,
    ImgFwdTypes,
    ImgXorTabDataSplit,
    TabDataReturnType,
    TabFwdTypes,
    TabxorImgBatch,
    _AdaptorForPyTorchTensor,
)
from bitfount.backends.pytorch.utils import LoggerType, _autodetect_gpu
from bitfount.config import BITFOUNT_LOGS_DIR
from bitfount.data.dataloader import _BitfountDataLoader
from bitfount.data.datasets import _Dataset
from bitfount.data.datasource import DataSource
from bitfount.data.types import _SingleOrMulti
from bitfount.federated.privacy.differential import (
    DPModellerConfig,
    _DifferentiallyPrivate,
)
from bitfount.metrics import Metric, MetricCollection
from bitfount.models.base_models import (
    ClassifierMixIn,
    LoggerConfig,
    ModelContext,
    NeuralNetworkMixIn,
    NeuralNetworkPredefinedModel,
    Optimizer,
    Scheduler,
    _BaseModel,
)
from bitfount.types import T_DTYPE, _JSONDict, _TensorLike
from bitfount.utils import _merge_list_of_dicts

logger = logging.getLogger(__name__)

_OptimizerType = Union[torch_optimizers.Optimizer, optimizers.Optimizer]

_OPTIMIZERS: Dict[str, Type[_OptimizerType]] = {
    name: class_
    # If there are name clashes, preference is given to the original torch version
    for name, class_ in dict(
        chain.from_iterable(
            d.items() for d in (vars(torch_optimizers), vars(optimizers))
        )
    ).items()
    if inspect.isclass(class_)
    and issubclass(class_, (optimizers.Optimizer, torch_optimizers.Optimizer))
    and not inspect.isabstract(class_)
    and name != "Optimizer"
}

_SCHEDULERS: Dict[str, Type[schedulers._LRScheduler]] = {
    name: class_
    for name, class_ in vars(schedulers).items()
    if inspect.isclass(class_)
    and issubclass(class_, schedulers._LRScheduler)
    and not inspect.isabstract(class_)
    and name != "_LRScheduler"
}

_TORCH_DTYPES: Dict[int, torch.dtype] = {
    16: torch.float16,
    32: torch.float32,
    64: torch.float64,
}
_STEP_OUTPUT = Union[torch.Tensor, Dict[str, Any]]  # From pl.LightningModule


def _calculate_embedding_sizes(
    categorical_feature_sizes: List[int],
) -> List[Tuple[int, int]]:
    """Calculate embedding sizes.

    The formula for determining the size of the embeddings is determined by
    empirical evidence alone and borrowed from the fast.ai library.
    """
    embedding_sizes = [
        (n_categories, min(600, round(1.6 * n_categories**0.56)))
        for n_categories in categorical_feature_sizes
    ]
    return embedding_sizes


class PyTorchClassifierMixIn(ClassifierMixIn):
    """MixIn for PyTorch classification problems.

    PyTorch classification models must have this class in their inheritance hierarchy.
    """

    def _do_output_activation(self, output: torch.Tensor) -> torch.Tensor:
        """Perform final activation function on output."""
        if self.multilabel:
            return torch.sigmoid(output)
        else:
            return F.softmax(output, dim=1)


class _PyTorchNeuralNetworkMixIn(NeuralNetworkMixIn):
    """All Pytorch Neural Networks must inherit from this abstract class.

    Specifies model structure and hyperparameters.
    """

    @staticmethod
    def _get_optimizer(optimizer: Optimizer) -> Callable[..., _OptimizerType]:
        """Returns appropriate optimizer class."""
        if optimizer.name in _OPTIMIZERS:
            return partial(_OPTIMIZERS[optimizer.name], **optimizer.params)

        raise ValueError(
            "Optimizer not supported.",
            "Please provide one supported by 'torch' or 'torch_optimizer'.",
        )

    @staticmethod
    def _get_scheduler(scheduler: Scheduler) -> Callable[..., schedulers._LRScheduler]:
        """Returns appropriate scheduler class."""
        if scheduler.name in _SCHEDULERS:
            return partial(_SCHEDULERS[scheduler.name], **scheduler.params)

        raise ValueError(
            "Scheduler not supported.",
            "Please provide one supported by 'torch'.",
        )

    @staticmethod
    def _get_early_stopping_callback(
        early_stopping_params: Optional[Dict[str, Any]] = None,
    ) -> EarlyStopping:
        """Returns EarlyStopping Callback."""
        if early_stopping_params is None:
            early_stopping_params = dict(
                monitor="validation_loss",
                min_delta=0.00,
                patience=2,
                verbose=True,
                mode="min",
            )

        return EarlyStopping(**early_stopping_params)


T_PYTORCH = TypeVar("T_PYTORCH", bound="BasePyTorchModel")


class BasePyTorchModel(
    _PyTorchDistributedModelMixIn,
    _PyTorchNeuralNetworkMixIn,
    pl.LightningModule,
    _DifferentiallyPrivate,
    _BaseModel,
    Generic[T_PYTORCH],
):
    """Implements a Neural Network in PyTorch Lightning.

    Args:
        model_name: Used for tensorboard logging. Model name will be left blank and
            default to "default" if none provided. Optional.
        model_version: Used for tensorboard logging.If version is not specified the
            logger inspects the save directory for existing versions, then automatically
            assigns the next available version. If it is a string then it is used as the
            run-specific subdirectory name, otherwise 'version_${version}' is used.
            Optional.
        stochastic_weight_avg: Whether to use [Stochastic Weight Averaging (SWA)](
            https://pytorch.org/blog/pytorch-1.6-now-includes-stochastic-\
weight-averaging).
        logger_config: Logger configuration. Optional. Will default to Tensorboard if
            not provided.

    Attributes:
        model_name: Name of the model.
        model_version: Version of the model.
        stochastic_weight_avg: Whether to use Stochastic Weight Averaging (SWA).
    """

    # Train/validate attributes
    _train_loss: float
    _validation_loss: float
    _metrics_results: Dict[str, str]

    # Test attributes
    _test_preds: Optional[List[np.ndarray]]
    _test_targets: Optional[List[np.ndarray]]

    def __init__(
        self,
        model_name: Optional[str] = None,
        model_version: Optional[Union[int, str]] = None,
        stochastic_weight_avg: bool = False,
        logger_config: Optional[LoggerConfig] = None,
        **kwargs: Any,
    ):
        super().__init__(**kwargs)

        self.model_name = model_name
        self.model_version = model_version
        self.stochastic_weight_avg = stochastic_weight_avg
        # Set training attributes
        self._model: Optional[nn.Module] = None  # actual underlying model
        self._pl_logger = self._get_logger_from_config(logger_config)
        self._pl_trainer: pl.Trainer = self.trainer_init()  # cannot be "self.trainer"
        self._trained_on_previous_batch: bool = False
        self._total_num_batches_trained: int = 0

        # Set placeholder for DP
        self._dp_engine: Optional[PrivacyEngine] = None

    @abstractmethod
    def _create_model(self) -> nn.Module:
        """Creates and returns model."""
        raise NotImplementedError

    @abstractmethod
    def _split_dataloader_output(
        self,
        data: Union[
            ImgAndTabDataSplit,
            ImgXorTabDataSplit,
        ],
    ) -> Union[ImgDataReturnType, TabDataReturnType]:
        """Splits the data from the dataloader into X, y."""
        raise NotImplementedError

    @abstractmethod
    def _do_output_activation(self, output: torch.Tensor) -> torch.Tensor:
        """Perform final activation function on output.

        Should be provided by MixIn class.
        """
        raise NotImplementedError

    class _Schema(
        _PyTorchNeuralNetworkMixIn._Schema,
        _DifferentiallyPrivate._Schema,
        _BaseModel._Schema,
    ):
        """No extra parameters to serialize here."""

        @abstractmethod
        def recreate_model(self, data: _JSONDict, **kwargs: Any) -> T_PYTORCH:
            """Recreates model."""
            raise NotImplementedError

    def tensor_precision(self) -> T_DTYPE:
        """Returns tensor dtype used by Pytorch Lightning Trainer.

        Returns:
            Pytorch tensor dtype.

        :::note

        Currently only 32-bit training is supported.

        :::
        """
        # TODO: [BIT-727] support non-32 bit training
        return cast(T_DTYPE, _TORCH_DTYPES[cast(int, self._pl_trainer.precision)])

    def initialise_model(
        self,
        data: Optional[DataSource] = None,
        context: Optional[ModelContext] = None,
    ) -> None:
        """Any initialisation of models/dataloaders to be done here.

        Initialises the dataloaders and sets `self._model` to be the output from
        `self.create_model`. Any initialisation ahead of federated or local training,
        serialization or deserialization should be done here.

        Args:
            data: The datasource for model training. Defaults to None.
            context: Indicates if the model is running as a modeller or worker.
                If None, there is no difference between modeller and worker.
        """
        self._initialised = True
        # Set initialisation context
        self._context = context
        if data is not None:
            self._add_datasource_to_schema(
                datasource=data, datafactory=_PyTorchDataFactory()
            )
            # Initialise model details
            if self._context != ModelContext.MODELLER:
                self._set_dataloaders(self.batch_size)
        self._opt_func: Callable[..., _OptimizerType] = self._get_optimizer(
            self.optimizer
        )
        self._scheduler_func: Optional[Callable[..., schedulers._LRScheduler]] = None
        if isinstance(self.scheduler, Scheduler):
            self._scheduler_func = self._get_scheduler(self.scheduler)

        self._model = self._create_model()

        # Initialise DP if requested
        self._initialise_differential_privacy()

    def _get_logger_from_config(
        self, logger_config: Optional[LoggerConfig]
    ) -> LightningLoggerBase:
        """Initialises the logger for the model."""
        if logger_config is None:
            logger = TensorBoardLogger(
                name=self.model_name,
                version=self.model_version,
                save_dir=str(BITFOUNT_LOGS_DIR),
            )
        else:
            if logger_config.name == "Neptune":
                logger = LoggerType[logger_config.name].value(**logger_config.params)
            else:
                if logger_config.save_dir is None:
                    logger_config.save_dir = BITFOUNT_LOGS_DIR
                logger = LoggerType[logger_config.name].value(
                    save_dir=logger_config.save_dir, **logger_config.params
                )
        return logger

    def _initialise_differential_privacy(self) -> None:
        """Initialises the Differential Privacy Engine if requested."""
        conf = self._dp_config
        if conf:
            # Check DP can be used with model
            dp_inspector = DPModelInspector(should_throw=True)
            try:
                dp_inspector.validate(self)
            except IncompatibleModuleException as e:
                # If autofix, try to do so
                if conf.auto_fix:
                    logger.warning(f"Incompatible modules detected in model: {e}")
                    logger.warning("Attempting to autofix.")

                    # Convert batchnorm to groupnorm
                    module_modification.convert_batchnorm_modules(self)

                    # Check again
                    dp_inspector.validate(self)
                else:
                    raise e

            # Create engine if not on modeller
            if self._context != ModelContext.MODELLER:
                self._dp_engine = PrivacyEngine(
                    module=self,  # use self rather than self._model
                    batch_size=self.batch_size,
                    sample_size=len(self._databunch.train_ds),
                    max_grad_norm=conf.max_grad_norm,
                    noise_multiplier=conf.noise_multiplier,
                    alphas=conf.alphas,
                    secure_rng=False,  # TODO: [BIT-511] check need for True
                    target_delta=conf.target_delta,
                    loss_reduction=conf.loss_reduction,
                )

    def _privacy_guarantees_exceeded(self) -> bool:
        """Checks whether the privacy spent exceeds the allowed max.

        Returns: True if maximum privacy budget exceeded, False if not or if DP not
            being checked.
        """
        # If monitoring DP, perform checks
        if self._dp_engine:
            epsilon, _ = self._dp_engine.get_privacy_spent()

            # Check privacy constraints
            if epsilon >= cast(DPModellerConfig, self._dp_config).max_epsilon:
                return True

        # If not exceeded or not being checked
        return False

    def trainer_init(self) -> pl.Trainer:
        """Initialises the Lightning Trainer for this model.

        Documentation for pytorch-lightning trainer can be found here:
        https://pytorch-lightning.readthedocs.io/en/stable/common/trainer.html

        Returns:
            The pytorch lightning trainer.
        """
        callbacks = []

        if self.early_stopping:
            callbacks.append(
                self._get_early_stopping_callback(self.early_stopping.params)
            )

        trainer = pl.Trainer(
            max_epochs=self.epochs,
            max_steps=self.steps,
            progress_bar_refresh_rate=1,
            deterministic=True,
            stochastic_weight_avg=self.stochastic_weight_avg,
            auto_lr_find=True,
            logger=self._pl_logger,
            callbacks=callbacks,
            gpus=_autodetect_gpu(),  # will be 1 (first GPU) or 0 (CPU)
        )
        return trainer

    def train_dataloader(self) -> Optional[_BitfountDataLoader]:  # type: ignore[override] # Reason: see below  # noqa: B950
        """Returns training dataloader."""
        # We override the dataloader return annotation as the LightningModule
        # expects a pytorch DataLoader, and we return PyTorchBitfountDataLoader
        return self.train_dl

    def val_dataloader(self) -> Optional[_BitfountDataLoader]:  # type: ignore[override] # Reason: see below  # noqa: B950
        """Returns validation dataloader."""
        # We override the dataloader return annotation as the LightningModule
        # expects a pytorch DataLoader, and we returnPyTorchBitfountDataLoader
        return self.validation_dl

    def test_dataloader(self) -> Optional[_BitfountDataLoader]:  # type: ignore[override] # Reason: see below  # noqa: B950
        """Returns test dataloader."""
        # We override the dataloader return annotation as the LightningModule
        # expects a pytorch DataLoader, and we return PyTorchBitfountDataLoader
        return self.test_dl

    def serialize(self, filename: Union[str, os.PathLike]) -> None:
        """Serialize model to file with provided `filename`.

        Args:
            filename: Path to file to save serialized model.
        """
        if not self._initialised:
            logger.info("Model not yet initialised. Auto-initialising model.")
            self.initialise_model()
        # Model has been initialised, assuring mypy of this
        assert self._model is not None  # nosec
        torch.save(self._model.state_dict(), filename)

    def deserialize(self, filename: Union[str, os.PathLike]) -> None:
        """Deserialize model.

        Args:
            filename: Path to file containing serialized model.

        :::danger

        This should not be used on a model file that has been received across a
        trust boundary due to underlying use of `pickle` by `torch`.

        :::
        """
        if not self._initialised:
            logger.info("Model not yet initialised. Auto-initialising model.")
            self.initialise_model()
        # Model has been initialised, assuring mypy of this
        assert self._model is not None  # nosec
        self._model.load_state_dict(torch.load(filename))

    @staticmethod
    def _get_layer_sizes(
        layers: List[int], input_size: int
    ) -> Tuple[Tuple[int, int], ...]:
        """Converts layer sizes to in a tuple of # in and out parameters."""
        layer_sizes = []
        for idx, size in enumerate(layers):
            if idx == 0:
                layer_sizes.append((input_size, size))
            else:
                layer_sizes.append((layers[idx - 1], size))

        return tuple(layer_sizes)

    def _get_loss(
        self,
        output: torch.Tensor,
        target: torch.Tensor,
        loss_modifiers: Tuple[torch.Tensor, ...],
    ) -> Tensor:
        """Computes the appropriate (weighted) loss."""
        sample_weight: torch.Tensor = loss_modifiers[0]
        categories: torch.Tensor = loss_modifiers[1]
        criterion = cast(Callable, self.loss_func)(reduction="none")
        # Handle categorical classification
        output = self._handle_categories_or_tuple(output, categories)

        if self.loss_func == nn.CrossEntropyLoss:
            loss = criterion(output, target.long())
        elif self.loss_func == nn.BCEWithLogitsLoss:
            loss = criterion(output, target.type_as(output))
            loss = loss.mean(dim=1)
        else:
            raise ValueError(
                f"Loss function {type(self.loss_func).__name__} is unsupported."
            )

        loss = loss * sample_weight.squeeze() / sample_weight.squeeze().sum()
        return cast(torch.Tensor, loss.sum())

    @staticmethod
    def _handle_categories_or_tuple(
        output: Union[torch.Tensor, Tuple[torch.Tensor, torch.Tensor]],
        categories: Optional[torch.Tensor] = None,
    ) -> torch.Tensor:
        """Handles conversion of output if categorical or tensor."""
        if categories is not None:
            # get output corresponding to right head depending on label
            categories = categories.unsqueeze(dim=1)
            output_to_stack: Tuple[Tensor, ...]
            if not isinstance(output, tuple):
                output_to_stack = (output,)
            else:
                output_to_stack = output
            stacked_output = torch.stack(output_to_stack, 1)
            categories = categories.expand_as(stacked_output)
            output = stacked_output.gather(1, categories)[:, 1]
        # Handle tuple output
        elif isinstance(output, tuple):
            output = output[0]
        return output

    def _compute_training_metrics(
        self,
        outputs: np.ndarray,
        targets: np.ndarray,
        training_metrics: Optional[MutableMapping[str, Metric]] = None,
    ) -> Dict[str, str]:
        """Computes metrics to be printed whilst training."""
        m = MetricCollection.create_from_model(self, training_metrics)
        results = m.compute(targets, outputs, threshold=0.5)
        self.log_dict(results, on_epoch=True, logger=True)
        results_with_str_values: Dict[str, str] = {}
        for k, v in results.items():
            results_with_str_values[k] = str(v)
        return results_with_str_values

    def configure_optimizers(
        self,
    ) -> Union[
        _OptimizerType, Tuple[List[_OptimizerType], List[schedulers._LRScheduler]]
    ]:
        """Configures the optimizer(s) and scheduler(s) for backpropagation.

        Returns:
            Either the optimizer of your choice or a tuple of optimizers and learning
            rate schedulers.
        """
        parameters = filter(lambda p: p.requires_grad, self.parameters())
        optimizer: _OptimizerType = self._opt_func(parameters)

        # Attach PrivacyEngine if present
        if self._dp_engine:
            self._dp_engine.attach(optimizer)

        if self._scheduler_func:
            scheduler = self._scheduler_func(optimizer)
            return [optimizer], [scheduler]

        return optimizer

    def forward(self, x: Union[ImgFwdTypes, TabFwdTypes]) -> Any:  # type: ignore[override] # reason: see below # noqa: B950
        """Performs a forward pass of the underlying model.

        Args:
            x: Input to the model.

        Returns:
            Output of the model.

        """
        # Signature incompatible with pl.LightningModule:
        # Superclass: def forward(self, *args: Any, **kwargs: Any) -> Any
        # Subclass: def forward(self, x: Union[ImgFwdTypes, TabFwdTypes]) -> Any
        return self._model(x)  # type: ignore[misc] # reason: the model is set by this stage # noqa: B950

    def _skip_training_batch(self, batch_idx: int) -> bool:
        """Checks if the current batch from the training set should be skipped.

        This is a workaround for the fact that PyTorch Lightning starts the Dataloader
        iteration from the beginning every time `fit` is called. This means that if we
        are training in steps, we are always training on the same batches. So this
        method needs to be called at the beginning of every `training_step` to skip
        to the right batch index.

        Args:
            batch_idx: the index of the batch from `training_step`.

        Returns:
            True if the batch should be skipped, otherwise False.
        """
        # TODO: [BIT-1237] remove this code block and find a better way to do this that
        # doesn't involve loading every batch into memory until we get to the right one
        if self.steps:
            # If we have trained on the previous batch, we can avoid the checks because
            # it means we have already reached the target start batch.
            if not self._trained_on_previous_batch:
                # mypy cannot see that the trainer has this attribute due to how it is set in pytorch lightning # noqa: B950
                if (self.steps != self._pl_trainer.max_steps) and (  # type: ignore[attr-defined] # Reason: see above # noqa: B950
                    batch_idx < (self._total_num_batches_trained % len(self.train_dl))
                ):
                    return True
                else:
                    self._trained_on_previous_batch = True

            # `_total_num_batches_trained` hasn't been incremented yet so we need to add
            # 1 here to get the correct batch number.
            # mypy cannot see that the trainer has this attribute due to how it is set in pytorch lightning # noqa: B950
            if self._total_num_batches_trained + 1 == self._pl_trainer.max_steps:  # type: ignore[attr-defined] # Reason: see above # noqa: B950
                self._trained_on_previous_batch = False

        if not self._pl_trainer.sanity_checking:
            self._total_num_batches_trained += 1

        return False

    def training_step(self, batch: Tuple[Union[TabxorImgBatch, ImgAndTabBatch], torch.Tensor], batch_idx: int) -> Optional[torch.Tensor]:  # type: ignore[override] # Reason: see below # noqa: B950
        """Training step.

        Args:
            batch: The batch to be trained on.
            batch_idx: The index of the batch to be trained on from the train
                dataloader.

        Returns:
            The loss from this batch as a `torch.Tensor`.
        """
        # Override the pl.lightning method, as it requires *args
        # and **kwargs as arguments whereas we will always have
        # the batch and the batch_idx as args.
        # `data` contains the X batch and often some additional information.
        # This can be split into relevant chunks by the `split_dataloader_output()`
        # method, which details how to perform that split.

        if self._skip_training_batch(batch_idx):
            # Returning `None` to skip this batch
            return None

        data, y = batch
        x, *loss_modifiers = self._split_dataloader_output(data)
        # Perform forward pass and get loss
        y_hat = self(x)
        loss = self._get_loss(
            output=y_hat,
            target=y,
            loss_modifiers=cast(Tuple[torch.Tensor, ...], loss_modifiers),
        )

        self.log(
            "train_loss", loss, on_step=True, on_epoch=True, prog_bar=True, logger=True
        )
        return loss

    def on_train_batch_start(  # type: ignore[override] # reason: incompatible with supertype return type # noqa: B950
        self,
        batch: _SingleOrMulti[_SingleOrMulti[np.ndarray]],
        batch_idx: int,
        dataloader_idx: int,
    ) -> Optional[Literal[-1]]:
        """Checks if any privacy guarantees have been exceeded and stops training if so.

        Args:
            batch: The batch to be trained on.
            batch_idx: The index of the batch to be trained on from the train
                dataloader.
            dataloader_idx: The index of the dataloader from which the batch was
                taken. This is useful for multi-dataloader training.

        Returns:
            -1 if the entire epoch should be skipped, otherwise None.
        """
        # Check privacy constraints and set stopping criterion as needed
        if self._privacy_guarantees_exceeded():
            self._pl_trainer.should_stop = True  # stops later epochs from running
            return -1  # this skips training for the rest of the current epoch
        else:
            return None

    def training_epoch_end(self, outputs: List[Dict[str, torch.Tensor]]) -> None:  # type: ignore[override] # Reason: see below # noqa: B950
        """Called at the end of the training epoch with all training step outputs.

        Ensures that the losses from a training epoch are aggregated and stored.

        Args:
            outputs: List of outputs from each training step.
        """
        # Override the pl.lightning method, as it requires a different type for outputs.
        merged_outputs: Dict[str, List[torch.Tensor]] = _merge_list_of_dicts(outputs)
        avg_train_loss = torch.mean(torch.stack(merged_outputs["loss"]))
        self._train_loss = avg_train_loss.item()

    def validation_step(self, batch: Tuple[Union[TabxorImgBatch, ImgAndTabBatch], torch.Tensor], batch_idx: int) -> Dict[str, Tensor]:  # type: ignore[override] # Reason: see below # noqa: B950
        """Validation step.

        Args:
            batch: The batch to be evaluated.
            batch_idx: The index of the batch to be evaluated from the validation
                dataloader.

        Returns:
            A dictionary of strings and values that should be averaged at the end of
            every epoch and logged e.g. `{"validation_loss": loss}`. These will be
            passed to the `validation_epoch_end` method.
        """
        # Override the pl.lightning method, as it requires
        # *args and **kwargs as arguments whereas we will
        # always have the batch and the batch_idx as args
        # Extract X, y and other data from batch
        data, y = batch
        x, *loss_modifiers = self._split_dataloader_output(data)
        # Get validation output and loss
        y_hat = self(x)
        loss = self._get_loss(
            output=y_hat,
            target=y,
            loss_modifiers=cast(Tuple[torch.Tensor, ...], loss_modifiers),
        )
        # Handle categorical data
        categories = loss_modifiers[-1]
        y_hat = self._handle_categories_or_tuple(y_hat, categories)

        y_hat = self._do_output_activation(y_hat)

        # Log and return desired outputs
        self.log("validation_loss", loss, on_epoch=True, prog_bar=True, logger=True)
        return {"validation_loss": loss, "outputs": y_hat, "targets": y}

    def validation_epoch_end(  # type: ignore[override] # Reason: see below
        self, outputs: List[Dict[str, Tensor]]
    ) -> None:
        """Called at the end of the validation epoch with all validation step outputs.

        Ensures that the average metrics from a validation epoch is stored. Logs results
        and also appends to `self.val_stats`.

        Args:
            outputs: List of outputs from each validation step.
        """
        # Override the pl.lightning method, as it requires a different type for outputs.
        # Merge outputs into singular lists rather than a list of dicts
        merged_outputs: Dict[str, List[torch.Tensor]] = _merge_list_of_dicts(outputs)
        # Calculate val loss average
        avg_val_loss = torch.mean(torch.stack(merged_outputs["validation_loss"]))
        self._validation_loss = avg_val_loss.item()

        # Calculate metrics from outputs. This will also log them out to self.log().
        self._metrics_results: Dict[str, str] = self._compute_training_metrics(
            outputs=np.asarray([i.cpu().numpy() for i in merged_outputs["outputs"]]),
            targets=np.asarray([i.cpu().numpy() for i in merged_outputs["targets"]]),
            training_metrics=self.metrics,
        )

    def test_step(self, batch: Tuple[Union[TabxorImgBatch, ImgAndTabBatch], torch.Tensor], batch_idx: int) -> Dict[str, Any]:  # type: ignore[override] # Reason: see below # noqa: B950
        """Make sure to set self.preds and self.targs before returning in this method.

        They will be returned by the `evaluate` method.

        Args:
            batch: The batch to be evaluated.
            batch_idx: The index of the batch to be evaluated from the test
                dataloader.

        Returns:
            A dictionary of predictions and targets. These will be passed to the
            `test_epoch_end` method.
        """
        # Override the pl.lightning method, as it requires
        # *args and **kwargs as arguments whereas we will
        # always have the batch and the batch_idx as args
        # Extract X, y and other data from batch
        data, y = batch
        x, *loss_modifiers = self._split_dataloader_output(data)

        # Get validation output and loss
        y_hat = self(x)

        # Handle categorical or tuple output
        categories = loss_modifiers[-1]
        y_hat = self._handle_categories_or_tuple(y_hat, categories)

        y_hat = self._do_output_activation(y_hat)
        # Output targets and prediction for later
        return {"predictions": y_hat, "targets": y}

    def test_epoch_end(self, outputs: List[Dict[str, torch.Tensor]]) -> None:  # type: ignore[override] # Reason: see below # noqa: B950
        """Aggregates the predictions and targets from the test set.

        Args:
            outputs: List of outputs from each test step.
        """
        # Override the pl.lightning method, as it requires a different type for outputs.
        merged_outputs: Dict[str, List[torch.Tensor]] = _merge_list_of_dicts(outputs)
        self._test_preds = [i.cpu().numpy() for i in merged_outputs["predictions"]]
        self._test_targets = [i.cpu().numpy() for i in merged_outputs["targets"]]

    def _fit_local(
        self,
        data: DataSource,
        metrics: Optional[MutableMapping[str, Metric]] = None,
        **kwargs: Any,
    ) -> Dict[str, str]:
        """Fits the model.

        Args:
            data: The data source to be used for training the model.
            metrics: Validation metrics to print during training. Defaults to None and
                will instead use metrics appropriate to the task. Optional.

        Returns:
            Validation metrics for the final epoch
        """
        # Check model initialisation
        if self._initialised:
            logger.debug("Model already initialised, will not reinitialise.")
        else:
            logger.info("Model not yet initialised. Auto-initialising model.")
            self.initialise_model(data)

        # TODO: [BIT-499] Check DP privacy guarantees before we even start; return NULL
        #       state if exceeded.

        self._reset_train_val_attrs()
        with self._use_metrics(metrics):
            # will perform self.epochs or self.steps of local training
            self._pl_trainer.fit(self)
        # Set validation loss in metric dict
        self._metrics_results["validation_loss"] = f"{self._validation_loss:.4f}"

        # Add DP metrics
        if self._dp_engine:
            epsilon, alpha = self._dp_engine.get_privacy_spent()
            self._metrics_results["alpha"] = str(alpha)
            self._metrics_results["epsilon"] = str(epsilon)

        return self._metrics_results

    def _reset_train_val_attrs(self) -> None:
        """Resets train/val attributes to None."""
        self._train_loss = None  # type: ignore[assignment] # Reason: see below
        self._validation_loss = None  # type: ignore[assignment] # Reason: see below
        self._metrics_results = None  # type: ignore[assignment] # Reason: see below
        # The whole point of this function is to reset this variables
        # to None, so ignore the assignment here

    @contextlib.contextmanager
    def _use_metrics(
        self, metrics: Optional[MutableMapping[str, Metric]] = None
    ) -> Iterator[None]:
        """Context manager which temporarily sets `metrics` to `self.metrics`.

        Args:
            metrics: Validation metrics to print during training. Defaults to None and
                will instead use metrics appropriate to the task. Optional.

        Returns:
            Empty Iterator.
        """
        # Stash the old metrics if new ones provided
        if metrics:
            metrics_store = self.metrics
            self.metrics = metrics
        try:
            yield None
        finally:
            # Restore the old metrics if new ones were provided
            if metrics:
                self.metrics = metrics_store

    def evaluate(
        self, test_dl: Optional[_BitfountDataLoader] = None, **kwargs: Any
    ) -> Tuple[np.ndarray, np.ndarray]:
        """This method runs inference on the test dataloader.

        This is done by calling `self.test_step` under the hood.
        Args:
            test_dl: Optional dataloader to run inference on which takes precedence over
                the dataloader returned by `self.test_dataloader`.

        Returns:
            A tuple of predictions and targets as numpy arrays.
        """
        # Reset metrics
        self._reset_test_attrs()

        self._pl_trainer.test(model=self, test_dataloaders=cast(DataLoader, test_dl))
        return cast(np.ndarray, self._test_preds), cast(np.ndarray, self._test_targets)

    def predict(self, data: DataSource, **kwargs: Any) -> np.ndarray:
        """This method runs inference on the test data, returns predictions.

        This is done by calling `test_step` under the hood. Customise this method as you
        please but it must return a list of predictions and a list of targets. Note that
        as this is the prediction function, only the predictions are returned.

        Returns:
            A numpy array containing the prediction values.

        Raises:
            ValueError: If no data is provided to test with.
        """
        self._add_datasource_to_schema(data, datafactory=_PyTorchDataFactory())
        test_dl = self._databunch.get_test_dataloader(self.batch_size)
        if isinstance(test_dl, _BitfountDataLoader):
            logger.info(
                f"Using test portion of dataset for inference - this has"
                f"{len(test_dl)} records."
            )
        else:
            raise ValueError("No data provided to run inference for the model on.")

        self._pl_trainer.test(model=self, test_dataloaders=cast(DataLoader, test_dl))
        return cast(np.ndarray, self._test_preds)

    def _reset_test_attrs(self) -> None:
        """Resets test attributes to None."""
        self._test_preds = None
        self._test_targets = None


class BaseTabNetModel(
    _PyTorchDistributedModelMixIn, _PyTorchNeuralNetworkMixIn, _BaseModel
):
    """TabNet Model as described in https://arxiv.org/abs/1908.07442.

    This is a wrapper around the implementation from DreamQuark. Documentation can be
    found here: https://dreamquark-ai.github.io/tabnet.

    Args:
        virtual_batch_size: Virtual batch size used for ghost batch
            normalization.
        patience: Number of epochs before early stopping.
        scheduler: Learning rate scheduler. Defaults to None.
        scheduler_params: Learning rate scheduler params. Defaults to None.
        embedding_sizes: Embeddings sizes. Defaults to None.
        num_workers: Number of workers for torch DataLoader. Defaults to 0.
        inverse_class_weights: Inverse class weights (only for classification problems).
            Defaults to True.
        mask_type: Mask type. Defaults to "sparsemax".
        decision_prediction_layer_size: Final feedforward layer size. Defaults to 8.
        attention_embedding_layer_size: Attention embedding layer size. Defaults to 8.
        num_steps: Number of steps. Defaults to 3.

    Raises:
        ValueError: If virtual batch size > batch size.
        ValueError: If the `model_structure` does not match the TabNet model.
        ValueError: If training is specified in `steps` rather than `epochs`. Training
            steps are not supported.
    """

    def __init__(
        self,
        virtual_batch_size: int = 64,
        patience: int = 2,
        embedding_sizes: Optional[Union[int, List[int]]] = None,
        num_workers: int = 0,
        inverse_class_weights: bool = True,
        mask_type: str = "sparsemax",
        decision_prediction_layer_size: int = 8,
        attention_embedding_layer_size: int = 8,
        num_steps: int = 3,
        **kwargs: Any,
    ):
        super().__init__(**kwargs)

        if self.steps:
            raise ValueError(
                "TabNet does not support steps. Training must be specified in epochs."
            )

        if virtual_batch_size > self.batch_size:
            raise ValueError("Virtual batch size must be smaller than batch size.")

        if (
            not isinstance(self.model_structure, NeuralNetworkPredefinedModel)
            or self.model_structure.name != "TabNet"
        ):
            raise ValueError(
                "Please provide the appropriate Model Structure.",
                "TabNet model can only create TabNet models.",
            )

        self.virtual_batch_size = virtual_batch_size
        self.patience = patience
        if not self.scheduler:
            self.scheduler = Scheduler("StepLR", {"step_size": 50, "gamma": 0.9})
        self.embedding_sizes = embedding_sizes
        self.num_workers = num_workers
        self.inverse_class_weights = inverse_class_weights
        self.mask_type = mask_type
        self.decision_prediction_layer_size = decision_prediction_layer_size
        self.attention_embedding_layer_size = attention_embedding_layer_size
        self.num_steps = num_steps

        # TODO: [BIT-1152] support FederatedAveraging by fixing initialisation
        logger.warning("TabNet model currently does not support FederatedAveraging.")

    class _Schema(_PyTorchNeuralNetworkMixIn._Schema, _BaseModel._Schema):
        """Marshmallow Schema."""

        virtual_batch_size = fields.Integer()
        patience = fields.Integer()
        embedding_sizes = fields.Integer(allow_none=True)
        num_workers = fields.Integer()
        inverse_class_weights = fields.Bool()
        mask_type = fields.String()
        decision_prediction_layer_size = fields.Integer()
        attention_embedding_layer_size = fields.Integer()
        num_steps = fields.Integer()

        @abstractmethod
        def recreate_model(self, data: _JSONDict, **kwargs: Any) -> BaseTabNetModel:
            """Recreates model."""
            raise NotImplementedError

    @abstractmethod
    def _create_model(self) -> None:
        """Returns appropriate model."""
        raise NotImplementedError

    def get_param_states(self) -> Dict[str, _TensorLike]:
        """See base class."""
        aux = dict(self._model.network.state_dict())  # type: ignore[union-attr] # Reason: _model is initialised in subclass # noqa: B950

        return {key: _AdaptorForPyTorchTensor(value) for key, value in aux.items()}

    def initialise_model(
        self,
        data: Optional[DataSource] = None,
        context: Optional[ModelContext] = None,
    ) -> None:
        """Any initialisation of models/dataloaders to be done here.

        Initialises the dataloaders and sets `self._model` to be the output from
        `self.create_model`. Any initialisation ahead of federated or local training,
        serialization or deserialization should be done here.

        Args:
            data: The datasource for model training. Defaults to None.
            context: Indicates if the model is running as a modeller or worker.
                If None, there is no difference between modeller and worker.
        """
        self._context = context
        self._initialised = True

        if data is not None:
            self._add_datasource_to_schema(data)

        # TODO: [BIT-1152] initialise model without setting dataloaders
        if self._context != ModelContext.MODELLER:
            self._set_dataloaders(batch_size=self.batch_size)
        self._model = self._create_model()
        # Make sure we only use the tabular part of the data.
        train_x_df_aux = self.train_dl.get_x_dataframe()
        if isinstance(train_x_df_aux, tuple):
            train_x_df, _ = train_x_df_aux
            train_x_df = train_x_df
        else:
            train_x_df = train_x_df_aux
        # 'Train' with 0 epochs just to set model parameters
        self._model.fit(  # type: ignore[attr-defined] # reason: the model should be set by the time we fit it # noqa: B950
            train_x_df.values,
            self.train_dl.get_y_dataframe()[self.datastructure.target].values,
            max_epochs=0,
            virtual_batch_size=self.virtual_batch_size,
            num_workers=self.num_workers,
            weights=int(self.inverse_class_weights),
            drop_last=False,
        )

    def evaluate(
        self, test_dl: Optional[_BitfountDataLoader] = None, **kwargs: Any
    ) -> Tuple[np.ndarray, np.ndarray]:
        """This method runs inference on the test dataloader.

        This is done by calling `self.test_step` under the hood.
        Args:
            test_dl: Optional dataloader to run inference on which takes precedence over
                the dataloader returned by `self.test_dataloader`.

        Returns:
            A tuple of predictions and targets as numpy arrays.
        """
        if test_dl is None:
            if isinstance(self.test_dl, _BitfountDataLoader):
                test_dl = self.test_dl
            else:
                raise ValueError("There is no test data to evaluate the model on.")
        X_aux = test_dl.get_x_dataframe()
        if isinstance(X_aux, tuple):
            X, _ = X_aux
        elif isinstance(X_aux, pd.DataFrame):
            X = X_aux
        X = X.values
        Y = test_dl.get_y_dataframe()[self._databunch.target].values
        preds = self._model.predict_proba(  # type:ignore[union-attr] # reason: the model should be set by the time we evaluate this function # noqa: B950
            X
        )

        return preds, Y

    def serialize(self, filename: Union[str, os.PathLike]) -> None:
        """Serialize model to file with provided `filename`.

        Args:
            filename: Path to file to save serialized model.
        """
        if not self._initialised:
            # TODO: [BIT-1152] initialise model here instead of logging an error
            logger.error(
                "Can't serialize uninitialized model. "
                "Model can't be initialised without data."
            )
            return
        torch.save(self._model.network.state_dict(), filename)  # type: ignore[union-attr] # reason: model is initialised # noqa: B950

    def deserialize(self, filename: Union[str, os.PathLike]) -> None:
        """Deserialize model.

        Args:
            filename: Path to file containing serialized model.

        :::danger

        This should not be used on a model file that has been received across a
        trust boundary due to underlying use of `pickle` by `torch`.

        :::
        """
        if not self._initialised:
            # TODO: [BIT-1152] initialise model here instead of logging an error
            logger.error(
                "Can't deserialize uninitialized model. "
                "Model can't be initialised without data."
            )
            return

        self._model.network.load_state_dict(torch.load(filename))  # type: ignore[union-attr] # reason: model is initialised # noqa: B950

    def _fit_local(
        self,
        data: DataSource,
        metrics: Optional[tabnet.metrics.Metric] = None,
        **kwargs: Any,
    ) -> Dict[str, str]:
        """Fit model and return results.

        Args:
            data: The data used for model training.
            metrics (List[Union[str, pytorch_tabnet.metrics.Metric]]): list of metrics
                to use on validation set every epoch. Last metric in this list is the
                one to use for early stopping
        """
        if self._initialised:
            logger.debug("Model already initialised, will not reinitialise.")
        else:
            logger.info("Model not yet initialised. Auto-initialising model.")
            self.initialise_model(data=data)
        if metrics is None:
            metrics = ["logloss"]
        elif "logloss" not in metrics:
            metrics.insert(0, "logloss")

        # Make sure we only use the tabular part of the data.
        train_x_df_aux = self.train_dl.get_x_dataframe()
        if isinstance(train_x_df_aux, tuple):
            train_x_df, _ = train_x_df_aux
            train_x_df = train_x_df
        else:
            train_x_df = train_x_df_aux

        if not isinstance(self.validation_dl, _BitfountDataLoader):
            empty_df = pd.DataFrame(columns=train_x_df.columns)
            self.validation_dl = _BitfountDataLoader(
                _Dataset(
                    empty_df,
                    target=self._databunch.target,
                    selected_cols=self.datastructure.selected_cols_w_types,
                )
            )
        val_x_df_aux = self.validation_dl.get_x_dataframe()
        if isinstance(val_x_df_aux, tuple):
            val_x_df, _ = val_x_df_aux
        else:
            val_x_df = val_x_df_aux

        self._model.fit(  # type: ignore[union-attr] # reason: the model should be set by the time we fit it # noqa: B950
            train_x_df.values,
            self.train_dl.get_y_dataframe()[self._databunch.target].values,
            eval_set=[
                (
                    val_x_df.values,
                    self.validation_dl.get_y_dataframe()[self._databunch.target].values,
                )
            ],
            eval_metric=metrics,
            max_epochs=self.epochs,
            patience=self.patience,
            batch_size=self.batch_size,
            virtual_batch_size=self.virtual_batch_size,
            num_workers=self.num_workers,
            weights=int(self.inverse_class_weights),
            drop_last=False,
        )

        metrics_results = {
            "validation_loss": "%.4f"
            % self._model.history["val_0_logloss"][-1]  # type: ignore[union-attr] # reason: see below # noqa: B950
            # The model should be set by the time we retrieve metrics
        }

        return metrics_results
