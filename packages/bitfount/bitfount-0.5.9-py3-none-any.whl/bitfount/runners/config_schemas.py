"""Dataclasses to hold the configuration details for the runners."""
from __future__ import annotations

from dataclasses import dataclass
import logging
from pathlib import Path
import typing
from typing import Dict, List, MutableMapping, Optional, Union

import desert
from marshmallow import ValidationError, fields
from marshmallow.validate import OneOf
from marshmallow_union import Union as M_Union

from bitfount.config import (
    _DEVELOPMENT_ENVIRONMENT,
    _STAGING_ENVIRONMENT,
    _get_environment,
)
from bitfount.data.types import DataPathModifiers, _SemanticTypeValue
from bitfount.data.utils import DatabaseConnection
from bitfount.federated.authorisation_checkers import (
    DEFAULT_IDENTITY_VERIFICATION_METHOD,
    IDENTITY_VERIFICATION_METHODS,
)
from bitfount.federated.privacy.differential import DPModellerConfig, DPPodConfig
from bitfount.federated.transport.config import (
    _DEV_MESSAGE_SERVICE_PORT,
    _DEV_MESSAGE_SERVICE_TLS,
    _DEV_MESSAGE_SERVICE_URL,
    _STAGING_MESSAGE_SERVICE_URL,
    MessageServiceConfig,
)
from bitfount.hub.api import (
    _DEV_AM_URL,
    _DEV_HUB_URL,
    _DEV_IDP_URL,
    _PRODUCTION_IDP_URL,
    _STAGING_AM_URL,
    _STAGING_HUB_URL,
    _STAGING_IDP_URL,
    PRODUCTION_AM_URL,
    PRODUCTION_HUB_URL,
)
from bitfount.hub.authentication_flow import _DEFAULT_USER_DIRECTORY
from bitfount.models.base_models import (
    EarlyStopping,
    LoggerConfig,
    Optimizer,
    Scheduler,
)
from bitfount.types import _JSONDict

logger = logging.getLogger(__name__)

# MYPY ISSUES
# Due to the use of desert.field to create non-standard fields in these dataclasses,
# mypy complains about incompatible type assignment. This is a known bug in desert
# (https://github.com/python-desert/desert/issues/101) and so we can ignore it
# until the issue is resolved.


def _deserialize_path(path: Optional[str]) -> Optional[Path]:
    """Converts a str into a Path.

    If the input is None, the output is None.
    """
    if path is None:
        return path
    else:
        return Path(path).expanduser()


def _deserialize_model_ref(ref: str) -> Union[Path, str]:
    """Deserializes a model reference.

    If the reference is a path to a file (and that file exists), return a Path
    instance. Otherwise, returns the str reference unchanged.
    """
    path = Path(ref).expanduser()
    if path.is_file():  # also returns False if path doesn't exist
        return path
    else:
        return ref


# COMMON SCHEMAS
@dataclass
class AccessManagerConfig:
    """Configuration for the access manager."""

    url: str = desert.field(  # type: ignore[assignment] # Reason: see top of file
        fields.URL(), default=PRODUCTION_AM_URL
    )


@dataclass
class HubConfig:
    """Configuration for the hub."""

    url: str = desert.field(  # type: ignore[assignment] # Reason: see top of file
        fields.URL(), default=PRODUCTION_HUB_URL
    )


# MODELLER SCHEMAS
@dataclass
class ModellerUserConfig:
    """Configuration for the modeller."""

    username: str = _DEFAULT_USER_DIRECTORY

    identity_verification_method: str = desert.field(
        fields.String(validate=OneOf(IDENTITY_VERIFICATION_METHODS)),
        default=DEFAULT_IDENTITY_VERIFICATION_METHOD,
    )  # type: ignore[assignment] # Reason: see top of file
    private_key_file: Optional[Path] = desert.field(  # type: ignore[assignment] # Reason: see top of file  # noqa: B950
        fields.Function(deserialize=_deserialize_path), default=None
    )
    identity_provider_url: Optional[str] = None

    def __post_init__(self) -> None:
        environment = _get_environment()
        if environment == _STAGING_ENVIRONMENT:
            self.identity_provider_url = _STAGING_IDP_URL
        elif environment == _DEVELOPMENT_ENVIRONMENT:
            self.identity_provider_url = _DEV_IDP_URL
        else:
            self.identity_provider_url = _PRODUCTION_IDP_URL


@dataclass
class ModellerConfig:
    """Full configuration for the modeller."""

    pods: PodsConfig
    data_structure: DataStructureConfig
    task: TaskConfig

    modeller: ModellerUserConfig = desert.field(  # type: ignore[assignment] # Reason: see top of file  # noqa: B950
        fields.Nested(desert.schema_class(ModellerUserConfig)),
        default_factory=ModellerUserConfig,
    )
    hub: HubConfig = desert.field(  # type: ignore[assignment] # Reason: see top of file
        fields.Nested(desert.schema_class(HubConfig)), default_factory=HubConfig
    )
    message_service: MessageServiceConfig = desert.field(
        fields.Nested(desert.schema_class(MessageServiceConfig)),
        default_factory=MessageServiceConfig,
    )  # type: ignore[assignment] # Reason: see top of file

    def __post_init__(self) -> None:
        environment = _get_environment()
        if environment == _STAGING_ENVIRONMENT:
            self.hub.url = _STAGING_HUB_URL
            self.message_service.url = _STAGING_MESSAGE_SERVICE_URL
        elif environment == _DEVELOPMENT_ENVIRONMENT:
            self.hub.url = _DEV_HUB_URL
            self.message_service.url = _DEV_MESSAGE_SERVICE_URL
            self.message_service.port = _DEV_MESSAGE_SERVICE_PORT
            self.message_service.tls = _DEV_MESSAGE_SERVICE_TLS


@dataclass
class ModelStructureConfig:
    """Configuration for the ModelStructure."""

    name: str
    arguments: _JSONDict = desert.field(
        fields.Dict(keys=fields.Str), default_factory=dict
    )  # type: ignore[assignment] # Reason: see top of file


@dataclass
class BitfountModelReferenceConfig:
    """Configuration for BitfountModelReference."""

    model_ref: Union[Path, str] = desert.field(
        fields.Function(deserialize=_deserialize_model_ref)
    )  # type: ignore[assignment] # Reason: see top of file
    username: Optional[str] = None


@dataclass
class ModelConfig:
    """Configuration for the model."""

    # For existing models
    name: Optional[str] = None
    structure: Optional[ModelStructureConfig] = None

    # For custom models
    bitfount_model: Optional[BitfountModelReferenceConfig] = None

    # Other
    hyperparameters: _JSONDict = desert.field(
        fields.Dict(keys=fields.Str), default_factory=dict
    )  # type: ignore[assignment] # Reason: see top of file
    logger_config: Optional[LoggerConfig] = None
    dp_config: Optional[DPModellerConfig] = None
    pretrained_file: Optional[Path] = desert.field(
        fields.Function(deserialize=_deserialize_path), default=None
    )  # type: ignore[assignment] # Reason: see top of file

    def __post_init__(self) -> None:
        # Validate either name or bitfount_model reference provided
        self._name_or_bitfount_model()
        try:
            self.hyperparameters["optimizer"] = Optimizer(
                **self.hyperparameters["optimizer"]
            )
        except KeyError:
            pass
        try:
            self.hyperparameters["early_stopping"] = EarlyStopping(
                **self.hyperparameters["early_stopping"]
            )
        except KeyError:
            pass
        try:
            self.hyperparameters["scheduler"] = Scheduler(
                **self.hyperparameters["scheduler"]
            )
        except KeyError:
            pass

    def _name_or_bitfount_model(self) -> None:
        """Ensures that both `name` and `bitfount_model` can't be set.

        Raises:
            ValidationError: if both `name` and `bitfount_model` are set
        """
        if self.name and self.bitfount_model:
            raise ValidationError("Cannot specify both name and bitfount_model.")
        if not self.name and not self.bitfount_model:
            raise ValidationError("Must specify either name or bitfount_model.")


@dataclass
class PodsConfig:
    """Configuration for the pods to use for the modeller."""

    identifiers: List[str]


@dataclass
class ProtocolConfig:
    """Configuration for the Protocol."""

    name: str
    arguments: _JSONDict = desert.field(
        fields.Dict(keys=fields.Str), default_factory=dict
    )  # type: ignore[assignment] # Reason: see top of file

    def __post_init__(self) -> None:
        # TODO: [BIT-1300] Remove this once custom protocols are supported
        # This is added for convenience so the user doesn't have to be verbose with the
        # protocol name when there are only bitfount protocols available
        if not self.name.startswith("bitfount."):
            self.name = f"bitfount.{self.name}"


@dataclass
class AggregatorConfig:
    """Configuration for the Aggregator."""

    secure: bool


@dataclass
class AlgorithmConfig:
    """Configuration for the Algorithm."""

    name: str
    arguments: _JSONDict = desert.field(
        fields.Dict(keys=fields.Str), default_factory=dict
    )  # type: ignore[assignment] # Reason: see top of file

    def __post_init__(self) -> None:
        # TODO: [BIT-1300] Remove this once custom algorithms are supported
        # This is added for convenience so the user doesn't have to be verbose with the
        # algorithm name when there are only bitfount algorithms available
        if not self.name.startswith("bitfount."):
            self.name = f"bitfount.{self.name}"


@dataclass
class TaskConfig:
    """Configuration for the task."""

    protocol: ProtocolConfig
    algorithm: AlgorithmConfig
    model: ModelConfig
    aggregator: Optional[AggregatorConfig] = None
    transformation_file: Optional[Path] = desert.field(
        fields.Function(deserialize=_deserialize_path), default=None
    )  # type: ignore[assignment] # Reason: see top of file


# POD SCHEMAS
@dataclass
class PodConfig:
    """Full configuration for the pod."""

    pod_name: str
    data: Union[DatabaseConfig, PathConfig]
    data_config: PodDataConfig
    pod_details: PodDetailsConfig
    schema: Optional[Path] = desert.field(
        fields.Function(deserialize=_deserialize_path), default=None
    )  # type: ignore[assignment] # Reason: see top of file
    access_manager: AccessManagerConfig = desert.field(
        fields.Nested(desert.schema_class(AccessManagerConfig)),
        default_factory=AccessManagerConfig,
    )  # type: ignore[assignment] # Reason: see top of file
    hub: HubConfig = desert.field(  # type: ignore[assignment] # Reason: see top of file
        fields.Nested(desert.schema_class(HubConfig)), default_factory=HubConfig
    )
    message_service: MessageServiceConfig = desert.field(
        fields.Nested(desert.schema_class(MessageServiceConfig)),
        default_factory=MessageServiceConfig,
    )  # type: ignore[assignment] # Reason: see top of file
    differential_privacy: Optional[DPPodConfig] = None
    other_pods: Optional[List[str]] = None
    username: str = _DEFAULT_USER_DIRECTORY

    def __post_init__(self) -> None:
        environment = _get_environment()
        if environment == _STAGING_ENVIRONMENT:
            self.hub.url = _STAGING_HUB_URL
            self.access_manager.url = _STAGING_AM_URL
            self.message_service.url = _STAGING_MESSAGE_SERVICE_URL
        elif environment == _DEVELOPMENT_ENVIRONMENT:
            self.hub.url = _DEV_HUB_URL
            self.access_manager.url = _DEV_AM_URL
            self.message_service.url = _DEV_MESSAGE_SERVICE_URL
            self.message_service.port = _DEV_MESSAGE_SERVICE_PORT
            self.message_service.tls = _DEV_MESSAGE_SERVICE_TLS

    @property
    def pod_id(self) -> str:
        """The pod ID of the pod specified."""
        return f"{self.username}/{self.pod_name}"


@dataclass
class PathConfig:
    """Configuration for the path."""

    path: Path = desert.field(
        fields.Function(deserialize=_deserialize_path)
    )  # type: ignore[assignment] # Reason: see top of file


@dataclass
class DatabaseConfig:
    """Configuration for the DatabaseConnection."""

    # This dataclass is a mostly superfluous wrapper around DatabaseConnection.
    # It is needed due to a bug in desert (https://github.com/python-desert/desert/issues/122)  # noqa: B950
    # which causes explicitly Optional Union fields to error out. Our mypy config
    # requires explicit Optional for good practice so rather than corrupt the
    # existing dataclass it makes sense to include a mirror config here so this
    # entire module can be excluded from that mypy check.
    #
    # Once the bug is fixed we can remove this class and replace it with
    # DatabaseConnection directly.

    table_name: str
    con: str
    schema: Optional[str] = None
    index_col: Optional[Union[str, List[str]]] = desert.field(
        M_Union([fields.String(), fields.List(fields.String())]), default=None
    )  # type: ignore[assignment] # Reason: see comment and top of file
    columns: Optional[List[str]] = None

    def get_db_connection(self) -> DatabaseConnection:
        """Returns a DatabaseConnection."""
        return DatabaseConnection(
            self.table_name, self.con, self.schema, self.index_col, self.columns
        )


@dataclass
class DataSplitConfig:
    """Configuration for the data splitter."""

    data_splitter: str = desert.field(
        fields.String(validate=OneOf(["percentage", "predefined"])),
        default="percentage",
    )  # type: ignore[assignment] # Reason: see top of file
    args: _JSONDict = desert.field(
        fields.Dict(keys=fields.Str), default_factory=dict
    )  # type: ignore[assignment] # Reason: see top of file


@dataclass
class PodDataConfig:
    """Configuration for the pod data source and dataset."""

    # There is a bug in desert (https://github.com/python-desert/desert/issues/122)
    # which causes explicitly Optional Union fields to error out. Our mypy config
    # requires explicit Optional for good practice so we currently have to do more
    # involved desert.field() assignments until the issue is fixed.

    ignore_cols: Optional[List[str]] = desert.field(
        fields.List(fields.String()), default=None
    )  # type: ignore[assignment] # Reason: see comment and top of file
    force_stype: Optional[MutableMapping[_SemanticTypeValue, List[str]]] = desert.field(
        fields.Dict(
            keys=fields.String(validate=OneOf(typing.get_args(_SemanticTypeValue))),
            values=fields.List(fields.String()),
        ),
        default=None,
    )  # type: ignore[assignment] # Reason: see comment and top of file
    modifiers: Optional[Dict[str, DataPathModifiers]] = desert.field(
        fields.Dict(
            keys=fields.Str,
            values=fields.Dict(
                keys=fields.String(
                    validate=OneOf(DataPathModifiers.__annotations__.keys())
                )
            ),
            default=None,
        ),
        default=None,
    )  # type: ignore[assignment] # Reason: see comment and top of file
    datasource_args: _JSONDict = desert.field(
        fields.Dict(keys=fields.Str), default_factory=dict
    )  # type: ignore[assignment] # Reason: see top of file
    data_split: DataSplitConfig = desert.field(
        fields.Nested(desert.schema_class(DataSplitConfig)),
        default_factory=DataSplitConfig,
    )  # type: ignore[assignment] # Reason: see top of file


@dataclass
class PodDetailsConfig:
    """Configuration for the pod details.

    Args:
        display_name: The display name of the pod.
        description: The description of the pod.
        is_public: Whether the pod is public. Defaults to False.
    """

    display_name: str
    description: str
    is_public: bool = False


@dataclass
class DataStructureSelectConfig:
    """Configuration for the datastructure select argument."""

    include: List[str] = desert.field(
        fields.List(fields.String()), default_factory=list
    )  # type: ignore[assignment] # Reason: see top of file
    exclude: List[str] = desert.field(
        fields.List(fields.String()), default_factory=list
    )  # type: ignore[assignment] # Reason: see top of file


@dataclass
class DataStructureAssignConfig:
    """Configuration for the datastructure assign argument."""

    target: Union[str, List[str]] = desert.field(
        M_Union([fields.String(), fields.List(fields.String())])
    )  # type: ignore[assignment] # Reason: see top of file
    # When we add more DataStructures, we should make the target an optional argument
    image_cols: Optional[List[str]] = None
    loss_weights_col: Optional[str] = None
    multihead_col: Optional[str] = None
    ignore_classes_col: Optional[str] = None


@dataclass
class DataStructureTransformConfig:
    """Configuration for the datastructure transform argument."""

    dataset: Optional[List[Dict[str, _JSONDict]]] = None
    batch: Optional[List[Dict[str, _JSONDict]]] = None


@dataclass
class DataStructureConfig:
    """Configuration for the modeller schema and dataset options."""

    assign: DataStructureAssignConfig = desert.field(
        fields.Nested(desert.schema_class(DataStructureAssignConfig)),
    )  # type: ignore[assignment] # Reason: see top of file
    select: DataStructureSelectConfig = desert.field(
        fields.Nested(desert.schema_class(DataStructureSelectConfig)),
        default_factory=DataStructureSelectConfig,
    )  # type: ignore[assignment] # Reason: see top of file
    transform: DataStructureTransformConfig = desert.field(
        fields.Nested(desert.schema_class(DataStructureTransformConfig)),
        default_factory=DataStructureTransformConfig,
    )  # type: ignore[assignment] # Reason: see top of file
