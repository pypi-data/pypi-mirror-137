"""Tests PyTorch NeuralNetwork-based classes."""
import pytest

from bitfount.backends.pytorch.models.nn import _get_torchvision_classification_model
from tests.utils.helper import backend_test, integration_test


@backend_test
@integration_test
class TestTorchvisionClassificationModels:
    """Tests retrieval of existing Torchvision models."""

    def test_unimplemented_model(self) -> None:
        """Tests error thrown if model exists but not supported."""
        with pytest.raises(
            ValueError,
            match="Model reshaping not implemented yet. Choose another model.",
        ):
            _get_torchvision_classification_model("googlenet", False, 2)

    def test_unrecognised_model(self) -> None:
        """Tests error thrown if model name not recognized."""
        with pytest.raises(ValueError, match="Model name not recognised"):
            _get_torchvision_classification_model("blahblahmodel", False, 2)

    def test_resnet(self) -> None:
        """Tests resnet* retrieval."""
        model = _get_torchvision_classification_model("resnet18", False, 2)
        assert model.fc.out_features == 2  # type: ignore[union-attr]  # Reason: test will fail if wrong type  # noqa: B950

    def test_alexnet(self) -> None:
        """Tests alexnet retrieval."""
        model = _get_torchvision_classification_model("alexnet", False, 2)
        assert model.classifier[6].out_features == 2  # type: ignore[index,union-attr]  # Reason: test will fail if wrong type  # noqa: B950

    def test_vgg(self) -> None:
        """Tests vgg* retrieval."""
        model = _get_torchvision_classification_model("vgg16", False, 2)
        assert model.classifier[6].out_features == 2  # type: ignore[index,union-attr]  # Reason: test will fail if wrong type  # noqa: B950

    def test_densenet(self) -> None:
        """Tests densenet* retrieval."""
        model = _get_torchvision_classification_model("densenet169", False, 2)
        assert model.classifier.out_features == 2  # type: ignore[union-attr]  # Reason: test will fail if wrong type  # noqa: B950

    def test_squeezenet(self) -> None:
        """Tests squeezenet* retrieval."""
        model = _get_torchvision_classification_model("squeezenet1_0", False, 2)
        assert model.classifier[1].out_channels == 2  # type: ignore[index,union-attr]  # Reason: test will fail if wrong type  # noqa: B950
        assert model.num_classes == 2
