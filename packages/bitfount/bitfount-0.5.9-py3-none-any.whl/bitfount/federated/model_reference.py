"""References to custom models."""
from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING, Any, Dict, Optional, Type, Union, cast

from marshmallow import Schema as MarshmallowSchema
from marshmallow import fields, post_load

from bitfount.data.datastructure import DataStructure
from bitfount.data.schema import BitfountSchema
from bitfount.federated.logging import _get_federated_logger
from bitfount.federated.shim import BackendTensorShim
from bitfount.types import DistributedModelProtocol
from bitfount.utils import _get_non_abstract_classes_from_module

if TYPE_CHECKING:
    from bitfount.hub.api import BitfountHub
    from bitfount.models.bitfount_model import BitfountModel


logger = _get_federated_logger(__name__)


class BitfountModelReference:
    """Describes a local or remote reference to a `BitfountModel` class.

    Args:
        model_ref: Either path to model file or name of model on hub.
        datastructure: `DataStructure` to be passed to the model when initialised.
        schema: `BitfountSchema` to be passed to the model when initialised.
        username: The username of the model owner. Defaults to bitfount session username
            if not provided.
        hub: Required for upload/download of model. This attribute is set after
            initialisation on the worker side as the hub is not serialized. Defaults to
            None.
        hyperparameters: Hyperparameters to be passed to the model constructor after it
            has been loaded from file or hub. Defaults to None.

    Raises:
        ValueError: If `username` is not provided and `hub` is not provided.

    :::tip

    To use another user's custom model, simply provide that user's username instead of
    your own (along with the name of the model as the `model_ref` argument).

    :::
    """

    def __init__(
        self,
        model_ref: Union[Path, str],
        datastructure: DataStructure,
        schema: Optional[BitfountSchema] = None,
        username: Optional[str] = None,
        hub: Optional[BitfountHub] = None,
        hyperparameters: Optional[Dict[str, Any]] = None,
    ):
        self.name = type(self).__name__
        self.model_ref = model_ref
        self.datastructure = datastructure
        self.schema = schema if schema else BitfountSchema()
        self.username: str
        self.hub = hub
        self.hyperparameters = hyperparameters if hyperparameters is not None else {}

        if username is not None:
            self.username = username
        else:
            if self.hub is not None:
                self.username = self.hub.username
            else:
                raise ValueError("One of hub or username must be set.")

    def _get_model_from_path(self) -> Type[BitfountModel]:
        """Returns model class from path.

        Returns:
            The model class.
        """
        self.model_ref = cast(Path, self.model_ref)
        return _get_non_abstract_classes_from_module(self.model_ref)[
            self.model_ref.stem
        ]

    def _upload_model_to_hub(self) -> None:
        """Uploads model to hub.

        Raises:
            ValueError: if `self.hub` has not been set or if there was a communication
                error with the hub
        """
        # model_ref is path to model code file
        if not self.hub:
            raise ValueError("Please a provide a BitfountHub instance to upload model.")

        self.model_ref = cast(Path, self.model_ref)
        model_sent_status = self.hub.send_model(self.model_ref)
        if not model_sent_status:
            raise ValueError(
                "Could not send model to Hub. Please address issues and try again"
            )

    def _get_model_from_hub(self) -> Type[BitfountModel]:
        """Returns model class from hub.

        Raises:
            ValueError: if `self.hub` has not been set or if the model was not
                successfully received

        Returns:
            The model class.
        """
        # model_ref is the name of a model on the hub
        if not self.hub:
            raise ValueError(
                "Please a provide a BitfountHub instance to download the model."
            )
        self.model_ref = cast(str, self.model_ref)
        model_cls = self.hub.get_model(self.username, self.model_ref)

        # Check that the model has been retrieved correctly
        if not model_cls:
            raise ValueError(
                "Unable to retrieve model from hub, check logs for details."
            )
        return model_cls

    def get_model(self) -> Type[BitfountModel]:
        """Gets the model referenced.

        If the model is a Path to a `BitfountModel`, it will upload it to BitfountHub
        and return the model class. If it is a name of a model on the hub, it will
        download the model from the hub and return the model class.

        Returns:
            The model class.

        Raises:
            TypeError: If the model is not a Path or a string.
            TypeError: If the model does not implement `DistributedModelProtocol`.
            ValueError: If a `BitfountHub` instance has not been provided or if there
                was a communication error with the hub.
        """
        if isinstance(self.model_ref, Path):
            model_cls = self._get_model_from_path()

            # Check that chosen model is compatible with federation by checking if it
            # implements `DistributedModelProtocol`. The only way to do this is to
            # instantiate the model and perform an `isinstance` check.
            model = model_cls(
                datastructure=self.datastructure,
                schema=self.schema,
                **self.hyperparameters,
            )
            # Mypy thinks that a subclass of "BitfountModel" and
            # "DistributedModelProtocol" cannot exist but it can so we can ignore the
            # errors.
            if not isinstance(model, DistributedModelProtocol):  # type: ignore[unreachable] # Reason: see above # noqa: B950
                raise TypeError(
                    f"Model {self.model_ref.stem} does not implement "
                    f"DistributedModelProtocol."
                )

            self._upload_model_to_hub()  # type: ignore[unreachable] # Reason: see above

            # self.model_ref is set to the name of the model so that the model doesn't
            # get unnecessarily re-uploaded if `get_model` is called multiple times
            self.model_ref = self.model_ref.stem
        elif isinstance(self.model_ref, str):
            model_cls = self._get_model_from_hub()
        else:
            raise TypeError(f"Model of type {type(self.model_ref)} not recognised.")

        return model_cls

    def backend_tensor_shim(self) -> BackendTensorShim:
        """Returns backend tensor shim from underlying model.

        This method is exposed here so that the shim can be used to create the
        Aggregator (if required by the Protocol) when the Protocol is deserialized on
        the Worker side.

        Returns:
            The shim for performing tensor operations.

        Raises:
            TypeError: If referenced model doesn't support backend_tensor_shim().
        """
        model = self.get_model()
        if not hasattr(model, "backend_tensor_shim"):
            raise TypeError("Referenced model doesn't support backend_tensor_shim().")
        else:
            # Above check ensures we have backend_tensor_shim() attribute
            return cast(BackendTensorShim, model.backend_tensor_shim())  # type: ignore[attr-defined] # Reason: hasattr check # noqa: B950

    @classmethod
    def get_schema(cls) -> Type[BitfountModelReference._Schema]:
        """Returns the Schema for BitfountModelReference."""
        return cls._Schema

    class _Schema(MarshmallowSchema):
        name = fields.Str()
        username = fields.Str(allow_none=True)
        model_ref = fields.Method(
            serialize="get_model_ref", deserialize="load_model_ref"
        )
        datastructure = fields.Nested(DataStructure._Schema)
        hyperparameters = fields.Dict(keys=fields.Str())
        # BitfountModelReference.{hub,schema} should not be serialized; will be need to
        # be manually set on the created instance later.

        @staticmethod
        def get_model_ref(bfmr: BitfountModelReference) -> str:
            """Returns the model_ref, ready for serialization."""
            model_ref = bfmr.model_ref
            # Try as path first
            try:
                return model_ref.stem  # type: ignore[union-attr]  # Reason: captured by AttributeError below  # noqa: B950
            except AttributeError as ae:
                # Check if class name only, return if is
                if Path(model_ref).stem == str(model_ref):
                    return str(model_ref)
                # Otherwise error
                raise TypeError(
                    f"Unable to serialise model_ref; "
                    f"expected python file path Path or model name str, "
                    f"got {type(model_ref)} with value {model_ref}"
                ) from ae

        @staticmethod
        def load_model_ref(value: str) -> Union[Path, str]:
            """Deserialize the model_ref value."""
            try:
                new_value = Path(value).expanduser()
                if new_value.stem == str(new_value):  # i.e. is just a class name
                    return str(value)
                return new_value
            except TypeError:
                return str(value)

        @post_load
        def recreate_bitfountmodelreference(
            self, data: dict, **_kwargs: Any
        ) -> BitfountModelReference:
            """Recreates a BitfountModelReference from this schema."""
            # Note that hub won't be set, will need to be set by the controlling code.
            return BitfountModelReference(**data)
