"""Classes concerning datasets."""
from abc import ABC, abstractmethod
from typing import (
    Any,
    Dict,
    List,
    Literal,
    Mapping,
    Optional,
    OrderedDict,
    Sequence,
    Tuple,
    Union,
    cast,
)

from databricks import koalas as ks
import numpy as np
import pandas as pd
from skimage import color, io

from bitfount.data.types import (
    _ImageAndTabularEntry,
    _ImageEntry,
    _SemanticTypeValue,
    _SingleOrMulti,
    _TabularEntry,
)
from bitfount.transformations.base_transformation import Transformation
from bitfount.transformations.batch_operations import BatchTimeOperation
from bitfount.transformations.processor import TransformationProcessor
from bitfount.transformations.unary_operations import UnaryOperation
from bitfount.types import _DataFrameType


class _BaseDataset(ABC):
    """Base class for representing a dataset."""

    x_columns: List[str]
    x_var: Tuple[Any, Any, np.ndarray]
    y_columns: List[str]
    y_var: np.ndarray

    embedded_col_names: List[str]
    image_columns: List[str]

    def __init__(
        self,
        data: _DataFrameType,
        weights_col: Optional[str] = None,
        multihead_col: Optional[str] = None,
        ignore_classes_col: Optional[str] = None,
        **kwargs: Any,
    ):
        self.data = data
        self.weights_col = weights_col
        self.multihead_col = multihead_col
        self.ignore_classes_col = ignore_classes_col

    def _get_extra_columns(self) -> np.ndarray:
        """Get auxiliary columns for loss manipulation."""
        if self.weights_col:
            weights = self.data.loc[:, [self.weights_col]].values.astype(np.float32)
            self.x_columns.append(self.weights_col)
        else:
            weights = np.ones(len(self.data), dtype=np.float32)
        weights = weights.reshape(len(weights), 1)

        if self.ignore_classes_col:
            ignore_classes = self.data.loc[:, [self.ignore_classes_col]].values.astype(
                np.int64
            )
        else:
            ignore_classes = -np.ones(len(self.data), dtype=np.int64)
        ignore_classes = ignore_classes.reshape(len(ignore_classes), 1)

        if self.multihead_col:
            category = self.data.loc[:, [self.multihead_col]].values
            category = category.reshape(len(category), 1)
            return cast(
                np.ndarray,
                np.concatenate((weights, ignore_classes, category), axis=1),
            )

        return cast(np.ndarray, np.concatenate((weights, ignore_classes), axis=1))

    @abstractmethod
    def __len__(self) -> int:
        raise NotImplementedError

    @abstractmethod
    def __getitem__(self, idx: Union[int, Sequence[int]]) -> Any:
        raise NotImplementedError


class _Dataset(_BaseDataset):
    """A dataset for supervised tasks.

    When indexed, returns numpy arrays corresponding to
    categorical features, continuous features, weights and target value (and
    optionally category)
    """

    def __init__(
        self,
        data: _DataFrameType,
        selected_cols: Mapping[_SemanticTypeValue, List[str]],
        target: Optional[Union[str, List[str]]] = None,
        batch_transforms: Optional[List[BatchTimeOperation]] = None,
        batch_transformation_step: Optional[Literal["train", "validation"]] = None,
        **kwargs: Any,
    ):
        super().__init__(data=data, **kwargs)

        self.batch_transforms = batch_transforms
        self.batch_transformation_step = batch_transformation_step

        if self.batch_transforms is not None:
            if self.batch_transformation_step is None:
                raise ValueError(
                    "'batch_transformation_step' must be provided "
                    "if 'batch_transformations' are provided"
                )

            # We create a dictionary mapping each image feature to the corresponding
            # list of transformations. This dictionary must be an OrderedDict so that
            # the order of the features is preserved and indexable. Currently, we only
            # support image transformations at batch time.
            feature_transforms: OrderedDict[
                str, List[BatchTimeOperation]
            ] = OrderedDict({i: [] for i in selected_cols["image"]})

            for tfm in self.batch_transforms:
                # Assertion to reassure mypy that `arg` is an attribute
                assert isinstance(tfm, UnaryOperation)  # nosec
                if tfm.arg in feature_transforms:
                    feature_transforms[tfm.arg].append(tfm)

            # Each feature that will be transformed needs to have its own transformation
            # processor. These processors need to correspond to the index of the feature
            # to be transformed because at batch time, the feature name is unavailable -
            # we only have the feature index. Finally, we only leave transformations if
            # the 'step' corresponds to the 'step' of the Dataset. This is to optimise
            # for efficiency only since the processor will ignore transformations that
            # are not relevant to the current step at batch time anyway.
            self.processors: Dict[int, TransformationProcessor] = {
                list(feature_transforms).index(col): TransformationProcessor(
                    [
                        cast(Transformation, i)
                        for i in tfms
                        if i.step == self.batch_transformation_step
                    ],
                )
                for col, tfms in feature_transforms.items()
            }

        self.embedded_col_names = selected_cols["categorical"]

        if target is not None:
            Y = data[target].reset_index(drop=True)
            X = data.drop(columns=target).reset_index(drop=True)
        else:
            # No target specified (only valid for inference case).
            X = data

        # Get the tabular part of the data
        x1_var = X.loc[:, self.embedded_col_names].values.astype(np.int64)
        continuous_cols = X.loc[:, selected_cols["continuous"]]
        x2_var = continuous_cols.values.astype(np.float32)
        self.tabular = np.concatenate((x1_var, x2_var), axis=1)
        # Get the image data
        self.image_columns = selected_cols["image"]
        if self.image_columns != []:
            for (i, col) in enumerate(self.image_columns):
                x_img = np.expand_dims(X.loc[:, col].values, axis=1)
                if i == 0:
                    self.image = x_img

                else:
                    self.image = np.concatenate((self.image, x_img), axis=1)
        else:
            self.image = np.array([])
        self.x_columns = (
            self.embedded_col_names
            + selected_cols["continuous"]
            + selected_cols["image"]
        )
        # Get the support data
        self.support_cols = self._get_extra_columns()
        # Package all together under the x_var
        self.x_var = (self.tabular, self.image, self.support_cols)
        if target is not None:
            self.y_var = data.loc[:, target].values
            self.y_columns = (
                list(Y.columns)
                if isinstance(Y, (pd.DataFrame, ks.DataFrame))
                else [Y.name]
            )

    def __len__(self) -> int:
        return len(self.x_var[0])

    def _transform_image(self, img: np.ndarray, idx: int) -> np.ndarray:
        """Performs image transformations if they have been specified.

        Args:
            img (np.ndarray): The image to be transformed.
            idx (int): The index of the image.

        Returns:
            np.ndarray: Transformed image.

        """
        if not self.batch_transforms:
            return img

        self.batch_transformation_step = cast(
            Literal["train", "validation"], self.batch_transformation_step
        )
        return self.processors[idx].batch_transform(
            img, step=self.batch_transformation_step
        )

    def _load_images(
        self, idx: Union[int, Sequence[int]]
    ) -> Union[np.ndarray, Tuple[np.ndarray, ...]]:
        """Loads images and performs transformations if specified.

        This involves first converting grayscale images to RGB if necessary.

        Args:
            idx (Union[int, Sequence[int]]): The index to be loaded.

        Returns:
            np.ndarray: Loaded and transformed image.

        """
        img_features = self.image[idx]
        imgs: Tuple[np.ndarray, ...] = tuple(
            io.imread(image, plugin="pil") for image in img_features
        )
        imgs = tuple(
            color.gray2rgb(image_array) if len(image_array.shape) < 3 else image_array
            for image_array in imgs
        )
        imgs = tuple(
            self._transform_image(image_array, i) for i, image_array in enumerate(imgs)
        )

        if len(img_features) == 1:
            return imgs[0]

        return imgs

    def __getitem__(
        self, idx: _SingleOrMulti[int]
    ) -> Union[_ImageAndTabularEntry, _TabularEntry, _ImageEntry]:

        image: Union[np.ndarray, Tuple[np.ndarray, ...]]
        tab: np.ndarray
        sup: np.ndarray

        # Set the target, if the dataset has no supervision,
        # choose set the default value to be 0.
        target = self.y_var[idx] if hasattr(self, "y_var") else 0

        # If the Dataset contains both tabular and image data
        if self.image.size and self.tabular.size:
            tab = self.tabular[idx]
            sup = self.support_cols[idx]
            image = self._load_images(idx)
            return (tab, image, sup), target

        # If the Dataset contains only tabular data
        elif self.tabular.size:
            tab = self.tabular[idx]
            sup = self.support_cols[idx]
            return (tab, sup), target

        # If the Dataset contains only image data
        else:
            sup = self.support_cols[idx]
            image = self._load_images(idx)
            return (image, sup), target
