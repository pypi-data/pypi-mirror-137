"""Tests model_reference.py module."""
import logging
from pathlib import Path
import re
import sys
from typing import Generator, cast
from unittest.mock import MagicMock

import pytest
from pytest import fixture
from pytest_mock import MockerFixture

from bitfount.data.datastructure import DataStructure
from bitfount.data.schema import BitfountSchema
from bitfount.federated.model_reference import BitfountModelReference
from bitfount.utils import seed_all
from tests.bitfount import TEST_SECURITY_FILES
from tests.utils.helper import create_datastructure, unit_test

logging.basicConfig(level=logging.INFO, stream=sys.stdout)

PUBLIC_KEY_PATH = TEST_SECURITY_FILES / "test_public.testkey"
PRIVATE_KEY_PATH = TEST_SECURITY_FILES / "test_private.testkey"

seed_all(43)


@unit_test
class TestBitfountModelReference:
    """Tests for BitfountModelReference class."""

    @fixture
    def datastructure(self) -> DataStructure:
        """Fixture for datastructure."""
        return create_datastructure()

    @fixture
    def model_ref(
        self,
        bitfount_model_correct_structure: str,
        datastructure: DataStructure,
        tmp_path: Path,
    ) -> Generator[BitfountModelReference, None, None]:
        """A BitfountModelReference for use in tests with ref as path."""
        model_file = tmp_path / "MyModel.py"
        model_file.touch()
        model_file.write_text(bitfount_model_correct_structure)
        hub_mock = MagicMock()
        hub_mock.send_model.return_value = True
        model_ref = BitfountModelReference(
            username="test",
            datastructure=datastructure,
            schema=BitfountSchema(),
            model_ref=model_file,
            hub=hub_mock,
            hyperparameters={"param1": 1, "param2": 2},
        )
        yield model_ref

    def test_get_model_hub_is_none(self, model_ref: BitfountModelReference) -> None:
        """Tests exception raised if hub not provided."""
        model_ref.hub = None
        with pytest.raises(ValueError):
            model_ref.get_model()

    def test_username_hub_cant_both_be_none(self, datastructure: DataStructure) -> None:
        """Checks that BitfountModelReference needs one of username or hub."""
        with pytest.raises(ValueError):
            BitfountModelReference(
                model_ref="Test", datastructure=datastructure, schema=BitfountSchema()
            )

    def test_get_model_model_sending_unsuccessful(
        self, model_ref: BitfountModelReference
    ) -> None:
        """Tests exception raised if method upload fails."""
        model_ref.hub = cast(MagicMock, model_ref.hub)
        model_ref.hub.send_model.return_value = False
        with pytest.raises(ValueError):
            model_ref.get_model()
        model_ref.hub.send_model.assert_called_once()

    def test_get_model_correctly(self, model_ref: BitfountModelReference) -> None:
        """Tests model uploaded and model class retrieved."""
        model_ref.hub = cast(MagicMock, model_ref.hub)
        model_class = model_ref.get_model()
        assert model_class is not None
        assert isinstance(model_class, type)  # i.e. is a class, not an instance
        model_ref.hub.send_model.assert_called_once()

    def test_get_model_as_string(self, model_ref: BitfountModelReference) -> None:
        """Tests model retrieval if model ref is a str."""
        model_ref.hub = cast(MagicMock, model_ref.hub)
        model_ref.hub.get_model.return_value = object
        model_ref.model_ref = "MyModel"
        model_class = model_ref.get_model()
        assert model_class is not None
        assert isinstance(model_class, type)
        model_ref.hub.get_model.assert_called_once()
        model_ref.hub.send_model.assert_not_called()

    def test_get_model_not_recognised(self, model_ref: BitfountModelReference) -> None:
        """Tests exception raised if model ref isn't path or str."""
        model_ref.hub = cast(MagicMock, model_ref.hub)
        model_ref.model_ref = 1123  # type: ignore[assignment]  # Reason: this is the purpose of the test  # noqa: B950
        with pytest.raises(TypeError):
            model_ref.get_model()
        model_ref.hub.send_model.assert_not_called()

    def test_get_model_with_model_that_doesnt_implement_distributed_model_protocol(
        self,
        bitfount_model_incorrect_structure: str,
        mocker: MockerFixture,
        model_ref: BitfountModelReference,
    ) -> None:
        """Tests model not implementing `DistributedModelProtocol` raises TypeError.

        Also ensures that the model doesn't get uploaded to the Hub.
        """
        mock_upload_model_to_hub = mocker.patch.object(
            model_ref, "_upload_model_to_hub"
        )
        assert isinstance(model_ref.model_ref, Path)
        model_ref.model_ref.write_text(bitfount_model_incorrect_structure)
        with pytest.raises(
            TypeError,
            match="Model MyModel does not implement DistributedModelProtocol.",
        ):
            model_ref.get_model()
        mock_upload_model_to_hub.assert_not_called()

    def test_serialize_deserialize(self, model_ref: BitfountModelReference) -> None:
        """Checks that model reference serialization and deserialization works."""
        schema = model_ref._Schema()
        # Pre-serialization asserts
        assert model_ref.hub is not None
        assert isinstance(model_ref.model_ref, Path)
        assert model_ref.hyperparameters == {"param1": 1, "param2": 2}

        # Serialization asserts
        dumped = schema.dump(model_ref)
        assert "hub" not in dumped
        dumped.pop("name")

        # Post-deserialization asserts
        loaded = schema.load(dumped)
        assert loaded.hub is None
        assert isinstance(loaded.model_ref, str)
        assert loaded.model_ref == "MyModel"
        assert model_ref.username == loaded.username
        assert model_ref.hyperparameters == loaded.hyperparameters

    def test_serialize_deserialize_set_hub_value_works_correctly(
        self, model_ref: BitfountModelReference
    ) -> None:
        """Checks that hub attribute is not serialized and can be set correctly."""
        schema = model_ref._Schema()

        # Serialization asserts
        dumped = schema.dump(model_ref)
        assert "hub" not in dumped
        dumped.pop("name")

        # Post-deserialization asserts
        loaded = schema.load(dumped)
        assert loaded.hub is None

        # Post-hub-setting asserts
        loaded.hub = model_ref.hub
        assert loaded.hub is not None
        assert isinstance(loaded.hub, MagicMock)

    def test_serialization_deserialization_of_model_name_ref(
        self, model_ref: BitfountModelReference
    ) -> None:
        """Tests serialization of model when contains model name, not path."""
        schema = model_ref._Schema()
        model_str = "ModelClassName"
        model_ref.model_ref = model_str  # explicitly set as class name str

        # Serialization asserts - model_ref unchanged
        dumped = model_ref._Schema().dump(model_ref)
        assert dumped["model_ref"] == model_str
        assert "hub" not in dumped
        dumped.pop("name")

        # Post-deserialization asserts
        loaded = schema.load(dumped)
        assert loaded.model_ref == model_str
        assert loaded.hub is None

    @pytest.mark.parametrize(
        "ref_str", ["MyModel.py", "/home/MyModel.py", "/home/MyModel"]
    )
    def test_serialization_of_incorrect_model_ref_fails(
        self, model_ref: BitfountModelReference, ref_str: str
    ) -> None:
        """Tests exception raised if model reference isn't a path.

        Tests with:
            - Basic file name as a string
            - Fuller file path as a string
            - Fuller file path ending in potential class name
        """
        model_ref.model_ref = ref_str  # looks like a path but is a string
        with pytest.raises(
            TypeError,
            match="Unable to serialise model_ref; "
            "expected python file path Path or model name str, "
            f"got <class 'str'> with value {ref_str}",
        ):
            model_ref._Schema().dump(model_ref)

    def test_empty_hyperparameters(self, datastructure: DataStructure) -> None:
        """Tests an empty dict of hyperparameters is created if none are specified."""
        bfmr = BitfountModelReference(
            model_ref="test",
            datastructure=datastructure,
            schema=BitfountSchema(),
            username="test",
        )
        assert bfmr.hyperparameters == {}

    def test_backend_tensor_shim(
        self, mocker: MockerFixture, model_ref: BitfountModelReference
    ) -> None:
        """Tests extraction of the model's BackendTensorShim works."""
        mock_get_model = mocker.patch.object(model_ref, "get_model")

        shim = model_ref.backend_tensor_shim()

        assert shim == mock_get_model.return_value.backend_tensor_shim.return_value
        # Check model method called
        mock_get_model.return_value.backend_tensor_shim.assert_called_once()

    def test_backend_tensor_shim_fails(
        self, mocker: MockerFixture, model_ref: BitfountModelReference
    ) -> None:
        """Tests extraction of the model's BackendTensorShim fails correctly."""
        mock_get_model = mocker.patch.object(model_ref, "get_model")
        # Remove backend_tensor_shim attribute
        del mock_get_model.return_value.backend_tensor_shim

        with pytest.raises(
            TypeError,
            match=re.escape("Referenced model doesn't support backend_tensor_shim()."),
        ):
            model_ref.backend_tensor_shim()
