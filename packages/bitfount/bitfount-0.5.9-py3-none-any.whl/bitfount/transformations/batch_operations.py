"""Operations done at batch time defined here."""
from __future__ import annotations

import inspect
from typing import Dict, List, Protocol, Type, Union, cast

import albumentations as A
import albumentations.augmentations as albumentations_augmentations
import albumentations.pytorch as albumentations_pytorch
import attr
import numpy as np

from bitfount.config import _PYTORCH_ENGINE, BITFOUNT_ENGINE
from bitfount.transformations.base_transformation import Transformation
from bitfount.transformations.exceptions import TransformationParsingError
from bitfount.transformations.unary_operations import UnaryOperation
from bitfount.types import _JSONDict

#: Dictionary of available image transformations and their corresponding classes.
IMAGE_TRANSFORMATIONS: Dict[str, Type[A.BasicTransform]] = {
    name: class_
    for name, class_ in vars(albumentations_augmentations).items()
    if inspect.isclass(class_)
    and issubclass(class_, A.BasicTransform)
    and not inspect.isabstract(class_)
}
if BITFOUNT_ENGINE == _PYTORCH_ENGINE:
    IMAGE_TRANSFORMATIONS.update(
        {
            name: class_
            for name, class_ in vars(albumentations_pytorch).items()
            if inspect.isclass(class_)
            and issubclass(class_, A.BasicTransform)
            and not inspect.isabstract(class_)
        }
    )


@attr.dataclass(kw_only=True)
class BatchTimeOperation(Transformation):
    """Class just to denote that transformation will happen at batch time.

    Args:
        step: Either "train" or "validation". Denotes whether transformations should be
            performed at training time or validation time.

    Raises:
        ValueError: If step is not one of "train" or "validation".
    """

    # Can't be a Literal because marshmallow then can't infer the type.
    step: str

    def _validate_args(self) -> None:
        """This method should be called in subclasses to validate the arguments."""
        if self.step not in ["train", "validation"]:
            raise ValueError(
                f"step must be one of 'train' or 'validation'. Got '{self.step}'"
            )


@attr.dataclass(kw_only=True)
class ImageTransformation(UnaryOperation, BatchTimeOperation):
    """Represents image transformations done on a single column at batch time.

    Args:
        transformations: List of transformations to be performed in order as one
            transformation.

    Raises:
        ValueError: If the `output` is set to False.
    """

    _registry_name = "image"

    transformations: List[Union[str, Dict[str, _JSONDict]]]

    def __attrs_post_init__(self) -> None:
        super().__attrs_post_init__()
        self._validate_args()
        if not self.output:
            raise ValueError("`output` cannot be False for a BatchTimeOperation")

    def _load_transformation(
        self, tfm: Union[str, Dict[str, _JSONDict]]
    ) -> A.BasicTransform:
        """Loads and returns transformation in albumentations.

        Args:
            tfm: Albumentations transformation.

        Raises:
            TransformationParsingError: If the transformation name cannot be parsed
                properly.
            ValueError: If the transformation cannot be found.

        Returns:
            The transform loaded in albumentations.
        """
        if isinstance(tfm, dict):
            tfm_keys = list(tfm.keys())
            if len(tfm_keys) > 1:
                raise TransformationParsingError(
                    f"Transformation has supplied multiple names: {tfm_keys}"
                )
            tfm_name = tfm_keys[0]
            tfm_args = tfm[tfm_name]
        else:
            tfm_name = tfm
            tfm_args = {}
        transformation = IMAGE_TRANSFORMATIONS.get(tfm_name)
        if transformation is None:
            raise ValueError(f"Transformation {tfm_name} could not be found.")

        return transformation(**tfm_args)

    def get_callable(self) -> _AlbumentationsAugmentation:
        """Returns callable which performs the transformations.

        Returns:
            The callable to perform transformations.
        """
        list_of_transformations: List[A.BasicTransform] = []
        for tfm in self.transformations:
            a_tfm = self._load_transformation(tfm)
            list_of_transformations.append(a_tfm)

        tfm_callable = A.Compose(list_of_transformations)
        return cast(_AlbumentationsAugmentation, tfm_callable)


class _AlbumentationsAugmentation(Protocol):
    """Protocol for the signature of an albumentations augmentation function."""

    def __call__(self, *, image: np.ndarray) -> Dict[str, np.ndarray]:
        """Call the function.

        `image` must be passed as a kwarg.
        """
        ...
