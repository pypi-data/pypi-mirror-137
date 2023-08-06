"""Defines abstract models, mixins, and other common backend-agnostic classes.

Implementations of these abstract models should be located in `bitfount.models.models`
or in the `models` subpackage of a backend.
"""
from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from enum import Enum, auto
import logging
import os
from pathlib import Path
from typing import (
    TYPE_CHECKING,
    Any,
    Callable,
    Dict,
    Generic,
    List,
    MutableMapping,
    Optional,
    Tuple,
    Type,
    TypeVar,
    Union,
    cast,
)

from cryptography.hazmat.primitives.asymmetric.rsa import RSAPrivateKey
import desert
from marshmallow import Schema as MarshmallowSchema
from marshmallow import fields, post_load
import numpy as np

from bitfount.config import BITFOUNT_LOGS_DIR
from bitfount.data.databunch import _BitfountDataBunch
from bitfount.data.datafactory import _BasicDataFactory, _DataFactory
from bitfount.data.dataloader import _BitfountDataLoader
from bitfount.data.datasource import DataSource
from bitfount.data.datastructure import DataStructure
from bitfount.data.schema import BitfountSchema
from bitfount.types import _JSONDict
from bitfount.utils import _add_this_to_list, seed_all

if TYPE_CHECKING:
    from bitfount.metrics import Metric

# Valid pooling functions for Convolutional Neural Networks.
POOLING_FUNCTIONS = ["max", "avg"]


logger = logging.getLogger(__name__)


@dataclass
class LoggerConfig:
    """Configuration for the logger.

    The configured logger will log training events, metrics, model checkpoints, etc. to
    your chosen platform. If no logger configuration is provided, the default logger is
    a Tensorboard logger.

    Args:
        name: The name of the logger. Should be one of the loggers supported by the
            chosen backend
        save_dir: The directory to save the logs. Defaults to `BITFOUNT_LOGS_DIR`
        params: A dictionary of keyword arguments to pass to the logger. Defaults to an
            empty dictionary
    """

    # Desert bug causing incompatability with mypy regarding type assignment
    # (https://github.com/python-desert/desert/issues/101)

    #: same as argument
    name: str
    #: same as argument
    save_dir: Optional[Path] = desert.field(
        fields.Function(
            deserialize=lambda path: path if path is None else Path(path).expanduser()
        ),
        default=BITFOUNT_LOGS_DIR,
    )  # type: ignore[assignment] # Reason: see above
    #: same as argument
    params: Optional[_JSONDict] = desert.field(
        fields.Dict(keys=fields.Str), default_factory=dict
    )  # type: ignore[assignment] # Reason: see above


class ModelContext(Enum):
    """Describes the context (modeller or worker) in which the model is running.

    This is used for models where the model differs depending on if it is on the
    modeller-side or worker-side of the federated process.
    """

    MODELLER = auto()
    WORKER = auto()


ModelType = TypeVar("ModelType", bound="_BaseModel")


class _BaseModel(ABC, Generic[ModelType]):
    """Abstract Base Model from which all other models must inherit.

    This class is designed to be at the very bottom of the inheritance hierarchy.
    The only reason it has a `super().__init__()` call is to call the parent classes of
    other classes defined in other libraries. It also takes kwargs so that we do not
    throw an error if there are unexpected keyword arguments. These unexpected keyword
    arguments will end up in this constructor where they will simply be ignored.
    """

    def __init__(
        self,
        datastructure: DataStructure,
        schema: BitfountSchema,
        seed: Optional[int] = None,
        **kwargs: Any,
    ):
        self.name = type(self).__name__
        self._context: Optional[ModelContext] = None
        self.metrics: Optional[MutableMapping[str, Metric]] = None
        self._model: Optional[ModelType] = None
        self._initialised: bool = False
        self.seed = seed
        seed_all(self.seed)
        self.datastructure = datastructure
        self._databunch: _BitfountDataBunch
        self.schema = schema
        self._objective: str

        # Placeholders for dataloaders
        self.train_dl: _BitfountDataLoader
        self.validation_dl: Optional[_BitfountDataLoader] = None
        self.test_dl: Optional[_BitfountDataLoader] = None

        for unexpected_kwarg in kwargs:
            logger.warning(f"Ignoring unexpected keyword argument {unexpected_kwarg}")

        super().__init__()

    def _set_dataloaders(
        self,
        batch_size: Optional[int] = None,
    ) -> None:
        """Sets train, validation and test dataloaders.

        Args:
            batch_size: The batch size to use for the dataloaders. Defaults to None.
        """
        if self._databunch is None:
            raise ValueError(
                "_set_dataloaders() requires the databunch to be set "
                "before being called."
            )
        self.train_dl = self._databunch.get_train_dataloader(batch_size)
        self.validation_dl = self._databunch.get_validation_dataloader(batch_size)
        self.test_dl = self._databunch.get_test_dataloader(batch_size)

    def _add_datasource_to_schema(
        self,
        datasource: DataSource,
        datafactory: Optional[_DataFactory] = None,
    ) -> None:
        """Adds the datasource to the schema and sets the `_databunch` attribute."""
        # self.datastructure.apply_transformations(datasource)
        # TODO: [BIT-1167] Once we add the transformations we can force the target
        #  to be categorical in the transformations as this can be specified directly
        if datafactory is None:
            datafactory = _BasicDataFactory()
        if self.datastructure.image_cols:
            for image in self.datastructure.image_cols:
                if image not in datasource.data.columns:
                    raise ValueError(f"Could not find {image} in dataset columns")
        # Add the datasource features to the datastructure.
        self.schema.add_datasource_features(
            datasource,
            ignore_cols=self.datastructure.ignore_cols,
            force_stype=self.datastructure._force_stype,
        )
        datasource = self.datastructure.apply_dataset_transformations(datasource)

        # Create the BitfountDataBunch that will be used in training
        self._databunch = _BitfountDataBunch(
            data_structure=self.datastructure,
            schema=self.schema,
            datasource=datasource,
            data_factory=datafactory,
        )

    def initialise_model(
        self,
        data: Optional[DataSource] = None,
        context: Optional[ModelContext] = None,
    ) -> None:
        """Can be implemented to initialise model if necessary.

        This is automatically called by the `fit()` method if necessary.

        Args:
            data: The data used for model training.
            context: Indicates if the model is running as a modeller or worker. If None,
                there is no difference between modeller and worker. Defaults to None.
        """
        self._initialised = True
        if data:
            self._add_datasource_to_schema(
                datasource=data,
            )

    @property
    def initialised(self) -> bool:
        """Returns True if the model has been initialised, otherwise False.

        I.e. whether the `initialise_model` method has been called.
        """
        return self._initialised

    @abstractmethod
    def serialize(self, filename: Union[str, os.PathLike]) -> None:
        """Implement this method to serialise a model."""
        raise NotImplementedError

    @abstractmethod
    def deserialize(self, filename: Union[str, os.PathLike]) -> None:
        """Implement this method to deserialise a model."""
        raise NotImplementedError

    @abstractmethod
    def evaluate(
        self,
        test_dl: Optional[_BitfountDataLoader] = None,
        **kwargs: Any,
    ) -> Tuple[np.ndarray, np.ndarray]:
        """Implement this method to perform inference on the test set.

        Args:
            test_dl: Optional `BitfountDataLoader` object containing test data. If this
                is not provided, the test set from the `DataSource` used to train the
                model should be used if present.

        Returns:
            A tuple of numpy arrays containing the predicted and actual values.
        """
        raise NotImplementedError

    def predict(self, data: DataSource, **kwargs: Any) -> np.ndarray:
        """This method runs inference on the test data, returns predictions.

        Args:
            data: `DataSource` object containing the data to run prediction on.
                Predictions will be generated for the test subset (as defined
                by the `DataSetSplitter`).

        Returns:
            A numpy array containing the prediction values.
        """
        raise NotImplementedError

    @abstractmethod
    def fit(
        self,
        data: Optional[DataSource] = None,
        metrics: Optional[Dict[str, Metric]] = None,
        pod_identifiers: Optional[List[str]] = None,
        private_key_or_file: Optional[Union[RSAPrivateKey, Path]] = None,
        **kwargs: Any,
    ) -> Optional[Dict[str, str]]:
        """Must be implemented to fit the model.

        Args:
            data: The data used for local model training.
            metrics: A dictionary of metrics to use for validation.
            pod_identifiers: A list of pod identifiers to use for federated training.
            private_key_or_file: A private key or path to private key file if doing
                federated training.

        Must call `initialise_model()` within the method if the model needs to be
        initialised.
        """
        raise NotImplementedError

    @property
    @abstractmethod
    def training_needed(self) -> bool:
        """Dictates whether the model needs training."""
        raise NotImplementedError

    class _Schema(MarshmallowSchema):
        name = fields.Str()
        datastructure = fields.Nested(DataStructure._Schema)
        schema = fields.Nested(BitfountSchema._Schema, allow_none=True)
        seed = fields.Integer(allow_none=True)

        @abstractmethod
        @post_load
        def recreate_model(self, data: _JSONDict, **_kwargs: Any) -> _BaseModel:
            """Recreates model using Schema."""
            raise NotImplementedError

    @classmethod
    @abstractmethod
    def get_schema(cls) -> Type[_BaseModel._Schema]:
        """Get the model schema."""
        raise NotImplementedError


class ClassifierMixIn:
    """MixIn for classification problems.

    Classification models must have this class in their inheritance hierarchy.

    Args:
        multilabel: Whether the problem is a multi-label problem. i.e. each datapoint
            belongs to multiple classes

    Attributes:
        multilabel: Whether the problem is a multi-label problem
        n_classes: Number of classes in the problem
    """

    #: set in _BaseModel
    datastructure: DataStructure
    #: set in _BaseModel
    schema: BitfountSchema

    def __init__(self, multilabel: bool = False, **kwargs: Any) -> None:
        super().__init__(**kwargs)
        self.multilabel = multilabel
        self.n_classes: int
        if "n_classes" in kwargs:
            self.n_classes = int(kwargs["n_classes"])
        self._objective = "classification"

    def set_number_of_classes(self) -> None:
        """Sets the target number of classes for the classifier.

        If the data is a multi-label problem, the number of classes is set to the number
        of target columns as specified in the `DataStructure`. Otherwise, the number of
        classes is set to the number of unique values in the target column as specified
        in the `BitfountSchema`. The value is stored in the `n_classes` attribute.
        """
        if self.datastructure.target is None and hasattr(self, "n_classes"):
            logger.warning(
                "No target specified in data. Using explicitly provided n_classes."
                "Note that only inference results will be valid, not training"
                "or evaluation for this model and dataset."
            )
        elif self.datastructure.target is not None:
            self.n_classes = (
                len(self.datastructure.target)
                if self.multilabel
                else self.schema.get_categorical_feature_size(self.datastructure.target)
            )
        else:
            raise ValueError(
                "No target specified in data, and number of classes not specified "
                "explicitly. Not able to determine dimensions of head of model."
            )

    def _add_datasource_to_schema(
        self,
        datasource: DataSource,
        datafactory: Optional[_DataFactory] = None,
    ) -> None:
        """Adds the datasource to the schema and sets the `_databunch` attribute."""
        # Add the datasource features to the datastructure.
        if datafactory is None:
            datafactory = _BasicDataFactory()
        force_categorical: List[str] = []
        force_categorical = _add_this_to_list(
            self.datastructure.target, force_categorical
        )
        force_categorical = _add_this_to_list(
            self.datastructure.multihead_col, force_categorical
        )
        if self.datastructure.image_cols:
            for image in self.datastructure.image_cols:
                if image not in datasource.data.columns:
                    raise ValueError(f"Could not find {image} in dataset columns")

        if "categorical" not in self.datastructure._force_stype.keys():
            self.datastructure._force_stype["categorical"] = force_categorical
        else:
            _add_this_to_list(
                force_categorical, self.datastructure._force_stype["categorical"]
            )

        self.schema.add_datasource_features(
            datasource,
            ignore_cols=self.datastructure.ignore_cols,
            force_stype=self.datastructure._force_stype,
        )
        datasource = self.datastructure.apply_dataset_transformations(datasource)

        # Create the BitfountDataBunch that will be used in training
        self._databunch = _BitfountDataBunch(
            data_structure=self.datastructure,
            schema=self.schema,
            datasource=datasource,
            data_factory=datafactory,
        )

    class _Schema(MarshmallowSchema):
        multilabel = fields.Bool()


class RegressorMixIn:
    """MixIn for regression problems.

    Currently, just used for tagging purposes.
    """

    pass


@dataclass
class NeuralNetworkModelStructure(ABC):
    """Dataclass defining the structure of a neural network model.

    Args:
        layers: List of hidden layer sizes i.e. not including the input/output layers.
            The layer type depends on the specific model structure. Defaults to 2 layers
            with 1000 and 500 nodes respectively.
        dropout_probs: List of dropout probabilities for each layer. Must be the same
            length as `layers`. Defaults to 0.01 and 0.1 respectively.
        mish_activation_function: Whether to use Mish activation function. If False,
            ReLU is used instead. Defaults to True.

    Attributes:
        num_heads: Number of heads for multihead models. I.e. the number of output
            layers.

    Raises:
        ValueError: If `layers` and `dropout_probs` are not the same length.
    """

    #: same as argument
    layers: Optional[List[int]] = None
    #: same as argument
    dropout_probs: Optional[List[float]] = None
    #: same as argument
    mish_activation_function: bool = True

    def __post_init__(self) -> None:
        if self.layers is None:
            self.layers = [1000, 500]

        if self.dropout_probs is None:
            self.dropout_probs = [0.01, 0.1]
        if len(self.layers) != len(self.dropout_probs):
            raise ValueError(
                "Number of neural layers must equal number of dropout layers."
            )
        self.num_heads: int

    def set_num_heads(self, datastructure: DataStructure) -> None:
        """Sets the `num_heads` attribute.

        This is taken from the `multihead_size` attribute of the `datastructure`
        if present. Otherwise, it is set to 1.

        Args:
            datastructure: The data structure the model has been designed for.

        Raises:
            ValueError: If `datastructure.multihead_size` is not a positive integer.

        """
        self.num_heads = (
            datastructure.multihead_size
            if datastructure.multihead_size is not None
            else 1
        )

    class _Schema(MarshmallowSchema):
        layers = fields.List(fields.Int())
        dropout_probs = fields.List(fields.Float())
        mish_activation_function = fields.Bool()


@dataclass
class FeedForwardModelStructure(NeuralNetworkModelStructure):
    """Dataclass defining the structure of a feedforward neural network model.

    This model structure only defines linear and dropout layers.

    Args:
        embedding_dropout: Dropout probability for embedding layer. Defaults to 0.04.
    """

    #: same as argument
    embedding_dropout: float = 0.04

    class _Schema(NeuralNetworkModelStructure._Schema):
        embedding_dropout = fields.Float()

        @post_load
        def recreate_model(
            self, data: _JSONDict, **_kwargs: Any
        ) -> FeedForwardModelStructure:
            """Recreates model using Schema."""
            return FeedForwardModelStructure(**data)


@dataclass
class CNNModelStructure(NeuralNetworkModelStructure):
    """Dataclass defining the structure of a convolutional neural network model.

    This model structure has multiple convolutional layers followed by multiple
    linear and dropout layers.

    Args:
        kernel_size: Kernel size for convolutional layers. Defaults to 5.
        padding: Padding for convolutional layers. Defaults to 2.
        stride: Stride for convolutional layers. Defaults to 1.
        pooling_function: Pooling function for convolutional layers. Options are "max"
            or "avg". Defaults to "max".
        ff_layers: List of linear hidden layer sizes following the convolutional layers.
            Defaults to [1000, 500].
        ff_dropout_probs: List of dropout probabilities for each linear layer. Must be
            the same length as `ff_layers`. Defaults to 0.01 and 0.1 respectively.

    Raises:
        ValueError: If `ff_layers` and `ff_dropout_probs` are not the same length.
        ValueError: If `pooling_function` is not "max" or "avg".
    """

    #: same as argument
    kernel_size: int = 5
    #: same as argument
    padding: int = 2
    #: same as argument
    stride: int = 1
    #: same as argument
    pooling_function: str = "max"
    #: same as argument
    ff_layers: List[int] = field(default_factory=list)
    #: same as argument
    ff_dropout_probs: List[float] = field(default_factory=list)

    def __post_init__(self) -> None:
        if not isinstance(self.layers, list):
            self.layers = [16, 32]
        super().__post_init__()
        if self.pooling_function not in POOLING_FUNCTIONS:
            raise ValueError(
                f"Pooling function can only be one of: {POOLING_FUNCTIONS}"
            )
        self.ff_layers = [1000, 500] if len(self.ff_layers) == 0 else self.ff_layers
        self.ff_dropout_probs = (
            [0.01, 0.1] if len(self.ff_dropout_probs) == 0 else self.ff_dropout_probs
        )
        if len(self.ff_layers) != len(self.ff_dropout_probs):
            raise ValueError(
                "Number of neural layers must equal number of dropout layers."
            )

    class _Schema(NeuralNetworkModelStructure._Schema):

        kernel_size = fields.Int()
        padding = fields.Int()
        stride = fields.Int()
        pooling_function = fields.Str()
        ff_layers = fields.List(fields.Int())
        ff_dropout_probs = fields.List(fields.Float())

        @post_load
        def recreate_model(self, data: _JSONDict, **_kwargs: Any) -> CNNModelStructure:
            """Recreates model using Schema."""
            return CNNModelStructure(**data)


@dataclass
class NeuralNetworkPredefinedModel:
    """This class encompasses what is required to use a predefined model e.g. ResNet.

    The currently supported models are:
        - AlexNet
        - DenseNet{121,161,169,201}
        - ResNet{18,34,50,101,152}
        - SqueezeNet{1_0,1_1}
        - VGG{11,11_bn,13,13_bn,16,16_bn,19,19_bn}
        - TabNet

    Args:
        name: name of the model
        pretrained: flag to denote whether to download the pretrained parameters
        **kwargs: additional arguments to pass to the model constructor
    """

    #: same as argument
    name: str
    #: same as argument
    pretrained: bool = True
    #: same as argument
    kwargs: Optional[Dict[str, bool]] = None

    class _Schema(MarshmallowSchema):
        name = fields.Str()
        pretrained = fields.Bool()
        kwargs = fields.Dict(keys=fields.Str(), values=fields.Bool(), allow_none=True)

        @post_load
        def recreate_model(
            self, data: _JSONDict, **_kwargs: Any
        ) -> NeuralNetworkPredefinedModel:
            """Recreates model using Schema."""
            return NeuralNetworkPredefinedModel(**data)


@dataclass
class Optimizer:
    """Class for specifying the optimizer for a neural network.

    The options for the optimizer will depend on the backend being used.

    Args:
        name: name of the optimizer
        params: dictionary of keyword arguments for the optimizer constructor
    """

    #: same as argument
    name: str
    #: same as argument
    params: Dict[str, Any] = field(default_factory=dict)

    class _Schema(MarshmallowSchema):
        name = fields.String()
        params = fields.Dict()

        @post_load
        def recreate(self, data: _JSONDict, **_kwargs: Any) -> Optimizer:
            """Recreate Optimizer instance from schema."""
            return Optimizer(**data)


@dataclass
class Scheduler:
    """Class for specifying the scheduler for a neural network.

    The options for the scheduler will depend on the backend being used.

    Args:
        name: name of the scheduler
        params: dictionary of keyword arguments for the scheduler constructor
    """

    #: same as argument
    name: str
    #: same as argument
    params: Dict[str, Any] = field(default_factory=dict)

    class _Schema(MarshmallowSchema):
        name = fields.String()
        params = fields.Dict()

        @post_load
        def recreate(self, data: _JSONDict, **_kwargs: Any) -> Scheduler:
            """Recreate Scheduler instance from schema."""
            return Scheduler(**data)


@dataclass
class EarlyStopping:
    """Class for specifying early stopping parameters.

    Args:
        params: dictionary of keyword arguments for the early stopping constructor. The
            parameters will depend on the backend being used.
    """

    #: same as argument
    params: Dict[str, Any] = field(default_factory=dict)

    class _Schema(MarshmallowSchema):
        params = fields.Dict()

        @post_load
        def recreate(self, data: _JSONDict, **_kwargs: Any) -> EarlyStopping:
            """Recreate EarlyStopping instance from schema."""
            return EarlyStopping(**data)


class NeuralNetworkMixIn:
    """Specifies model structure and hyperparameters for neural network models.

    All neural network models must inherit from this class.

    Args:
        model_structure: The structure of the model.
        batch_size: The number of data points in each batch. Defaults to 512.
        epochs: The number of epochs to train for. If `steps` is provided, `epochs`
            cannot be provided. Defaults to None.
        steps: The number of steps to train for. If `epochs` is provided, `steps`
            cannot be provided. Defaults to None.
        optimizer: The optimizer to use. Defaults to "AdamW" with a learning rate of
            0.01.
        scheduler: The scheduler to use. Defaults to None.
        custom_loss_func: A custom loss function to use. Defaults to None.
        early_stopping: Early stopping parameters. Defaults to None.

    Attributes:
        model_structure: The structure of the model.
        batch_size: The number of data points in each batch.
        epochs: The number of epochs to train for.
        steps: The number of steps to train for.
        optimizer: The optimizer to use.
        scheduler: The scheduler to use.
        loss_func: A custom loss function to use.
        early_stopping: Early stopping parameters.

    Raises:
        ValueError: If both `epochs` and `steps` are provided.

    :::caution

    `custom_loss_func` cannot be serialized and therefore cannot be used in Federated
    Learning.

    :::
    """

    #: set in _BaseModel
    datastructure: DataStructure

    def __init__(
        self,
        model_structure: Union[
            NeuralNetworkModelStructure, NeuralNetworkPredefinedModel
        ],
        batch_size: int = 512,
        epochs: Optional[int] = None,
        steps: Optional[int] = None,
        optimizer: Optional[Optimizer] = None,
        scheduler: Optional[Scheduler] = None,
        custom_loss_func: Optional[Callable] = None,
        early_stopping: Optional[EarlyStopping] = None,
        **kwargs: Any,
    ):
        super().__init__(**kwargs)

        if (steps is None and epochs is None) or (
            isinstance(steps, int) and isinstance(epochs, int)
        ):
            raise ValueError("You must specify one (and only one) of steps or epochs.")

        if optimizer is None:
            logger.info("No optimizer provided, using AdamW with learning rate 1e-2.")
            self.optimizer = Optimizer("AdamW", {"lr": 0.01})
        elif isinstance(optimizer, Optimizer):
            self.optimizer = optimizer

        self.model_structure = model_structure
        self.epochs = epochs
        self.steps = steps
        self.batch_size = batch_size
        self.scheduler = scheduler
        self._opt_func: Optional[Callable] = None  # To be set by initialise_model()
        self._scheduler_func: Optional[
            Callable
        ] = None  # To be set by initialise_model()
        self.loss_func: Optional[Callable] = custom_loss_func  # Only works locally
        self.early_stopping = early_stopping

        if isinstance(self.model_structure, NeuralNetworkModelStructure):
            self.model_structure.set_num_heads(self.datastructure)

    @staticmethod
    @abstractmethod
    def _get_optimizer(optimizer: Optimizer) -> Callable:
        """Returns appropriate optimizer class."""
        raise NotImplementedError

    @staticmethod
    @abstractmethod
    def _get_scheduler(scheduler: Scheduler) -> Callable:
        """Returns appropriate scheduler class."""
        raise NotImplementedError

    @property
    def training_needed(self) -> bool:
        """Dictates whether the model needs training.

        Returns:
            bool: True if one of either epochs or steps are > 0.
        """
        return sum(filter(None, (self.epochs, self.steps))) > 0

    class _Schema(MarshmallowSchema):
        model_structure = fields.Method(
            serialize="_nn_model_structure_serialize",
            deserialize="_nn_model_structure_deserialize",
        )
        epochs = fields.Integer(allow_none=True)
        steps = fields.Integer(allow_none=True)
        batch_size = fields.Integer(allow_none=True)
        optimizer = fields.Nested(Optimizer._Schema, allow_none=True)
        scheduler = fields.Nested(Scheduler._Schema, allow_none=True)
        early_stopping = fields.Nested(EarlyStopping._Schema, allow_none=True)
        custom_loss_func = fields.Raw(allow_none=True)

        def _nn_model_structure_serialize(
            self, base_object: NeuralNetworkMixIn
        ) -> _JSONDict:
            """Custom serialization of Neural Network structure.

            Required for the NeuralNetworkMixIn to know which Schema to use
            for serialization.
            """
            class_to_schema = {
                "NeuralNetworkPredefinedModel": NeuralNetworkPredefinedModel._Schema,
                "CNNModelStructure": CNNModelStructure._Schema,
                "FeedForwardModelStructure": FeedForwardModelStructure._Schema,
            }
            try:
                schema: MarshmallowSchema = class_to_schema[
                    base_object.model_structure.__class__.__name__
                ]()
                return cast(_JSONDict, schema.dump(base_object.model_structure))
            except KeyError as e:
                raise KeyError(f"{e}. Schema Object not recognised")

        def _nn_model_structure_deserialize(
            self, object_dict: _JSONDict
        ) -> Union[
            CNNModelStructure, FeedForwardModelStructure, NeuralNetworkPredefinedModel
        ]:
            """Custom deserialization of Neural Network structure.

            Required for the NeuralNetworkMixIn to know which Schema to use
            for deserialization.
            """
            if object_dict.get("kernel_size"):
                cnn_model_structure: CNNModelStructure = (
                    CNNModelStructure._Schema().load(object_dict)
                )
                return cnn_model_structure
            elif object_dict.get("embedding_dropout"):
                ff_model_structure: FeedForwardModelStructure = (
                    FeedForwardModelStructure._Schema().load(object_dict)
                )
                return ff_model_structure
            else:
                predefined_model: NeuralNetworkPredefinedModel = (
                    NeuralNetworkPredefinedModel._Schema().load(object_dict)
                )
                return predefined_model
