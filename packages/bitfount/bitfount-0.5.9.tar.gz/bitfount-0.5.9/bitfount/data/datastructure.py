"""Classes concerning data structures.

DataStructures provide information about the columns of a DataSource for a specific
Modelling Job.
"""
from __future__ import annotations

from dataclasses import dataclass
import logging
from os import PathLike
from typing import TYPE_CHECKING, Any, Dict, List, MutableMapping, Optional, Union, cast

import desert
from marshmallow import Schema as MarshmallowSchema
from marshmallow import fields, post_load
import yaml

from bitfount.data.types import SemanticType, _SemanticTypeValue
from bitfount.transformations.batch_operations import BatchTimeOperation
from bitfount.transformations.parser import TransformationsParser
from bitfount.types import _JSONDict
from bitfount.utils import _add_this_to_list

if TYPE_CHECKING:
    from bitfount.data.datasource import DataSource
    from bitfount.data.schema import BitfountSchema
    from bitfount.runners.config_schemas import (
        DataStructureAssignConfig,
        DataStructureSelectConfig,
        DataStructureTransformConfig,
    )

logger = logging.getLogger(__name__)

DEFAULT_IMAGE_TRANSFORMATIONS: List[Union[str, _JSONDict]] = [
    {"Resize": {"height": 224, "width": 224}},
    "Normalize",
    "ToTensorV2",
]


@dataclass
class DataStructure:
    """Information about the columns of a DataSource.

    This component provides the desired structure of data
    to be used by discriminative machine learning models.


    Args:
        target: The training target column or list of columns.
        ignore_cols: A list of columns to ignore when getting the
            data. Defaults to None.
        selected_cols: A list of columns to select when getting the
            data. Defaults to None.
        loss_weights_col: A column name which provides a weight to be given
            to each sample in loss function. Defaults to None.
        multihead_col: A categorical column whereby the number of unique values
            will determine number of heads in a Neural Network. Used
            for multitask training. Defaults to None.
        multihead_size: The number of uniques values in the `multihead_col`.
            Used for multitask training. Required if `multihead_col` is
            provided. Defaults to None.
        ignore_classes_col: A column name denoting which classes to ignore
            in a multilabel multiclass classification problem. Each value is
            expected to contain a list of numbers corresponding to the indices of
            the classes to be ignored as per the order provided in `target`.
            E.g. [0,2,3]. An empty list can be provided (e.g. []) to avoid ignoring
            any classes for some samples. Defaults to None.
        batch_transforms: A dictionary of transformations to apply to batches.
            Defaults to None.
        dataset_transforms: A dictionary of transformations to apply to
            the whole dataset. Defaults to None.

    Raises:
        ValueError: If both `ignore_cols` and `selected_cols` are provided.
        ValueError: If the `multihead_col` is provided without `multihead_size`.
    """

    target: Optional[Union[str, List[str]]] = None
    # Mypy errors ignored below. For more details see `config_schemas.py`
    ignore_cols: List[str] = desert.field(  # type: ignore[assignment] # Reason: above
        fields.List(fields.String()), default_factory=list
    )
    selected_cols: List[str] = desert.field(  # type: ignore[assignment] # Reason: above
        fields.List(fields.String()), default_factory=list
    )
    loss_weights_col: Optional[str] = None
    multihead_col: Optional[str] = None
    multihead_size: Optional[int] = None
    ignore_classes_col: Optional[str] = None
    image_cols: Optional[List[str]] = None
    batch_transforms: Optional[List[Dict[str, _JSONDict]]] = None
    dataset_transforms: Optional[List[Dict[str, _JSONDict]]] = None

    def __post_init__(self) -> None:
        # Only one of selected_cols and ignore_cols can be provided
        if self.selected_cols and self.ignore_cols:
            raise ValueError(
                "Please provide either columns to select or to ignore, not both."
            )
        if self.multihead_col and self.multihead_size is None:
            raise ValueError("Please provide the size of the multihead column.")
        if self.dataset_transforms is not None:
            self.set_columns_after_transformations(self.dataset_transforms)
        self._force_stype: MutableMapping[_SemanticTypeValue, List[str]] = {}
        if self.image_cols:
            self._force_stype["image"] = self.image_cols

        if self.batch_transforms is None and self.image_cols:
            default_image_transformations = []
            for col in self.image_cols:
                for step in ["train", "validation"]:
                    default_image_transformations.append(
                        {
                            "Image": {
                                "arg": col,
                                "output": True,
                                "transformations": DEFAULT_IMAGE_TRANSFORMATIONS,
                                "step": step,
                            }
                        }
                    )
            self.batch_transforms = default_image_transformations

    @classmethod
    def create_datastructure(
        cls,
        select: DataStructureSelectConfig,
        transform: DataStructureTransformConfig,
        assign: DataStructureAssignConfig,
    ) -> DataStructure:
        """Creates a datastructure based on the yaml config.

        Args:
            select: The configuration for columns to be included/excluded
                from the `DataStructure`.
            transform: The configuration for dataset and batch transformations
                to be applied to the data.
            assign: The configuration for special columns in the `DataStructure`.

        Returns:
              A `DataStructure` object.
        """
        if select.include and select.exclude:
            raise ValueError(
                "Please provide either columns to include or to exclude from data"
                ", not both."
            )
        ignore_cols = select.exclude if select.exclude is not None else []
        selected_cols = select.include if select.include is not None else []
        return cls(
            target=assign.target,
            ignore_cols=ignore_cols,
            selected_cols=selected_cols,
            loss_weights_col=assign.loss_weights_col,
            multihead_col=assign.multihead_col,
            ignore_classes_col=assign.ignore_classes_col,
            image_cols=assign.image_cols,
            batch_transforms=transform.batch,
            dataset_transforms=transform.dataset,
        )

    @classmethod
    def load_from_file(cls, file_path: Union[str, PathLike]) -> DataStructure:
        """Loads DataStructure from yaml file.

        Args:
            file: A yaml file with the `DataStructure` configuration.

        Returns:
            The loaded `DataStructure`.
        """
        with open(file_path, "r") as f:
            datastructure_yaml = yaml.safe_load(f)
        datastructure: DataStructure = cls._Schema().load(datastructure_yaml)
        return datastructure

    def get_columns_ignored_for_training(self) -> List[str]:
        """Adds all the extra columns that will not be used in model training.

        Returns:
            ignore_cols_aux: A list of columns that will be ignored when
                training a model.
        """
        ignore_cols_aux = self.ignore_cols[:]
        ignore_cols_aux = _add_this_to_list(self.target, ignore_cols_aux)
        ignore_cols_aux = _add_this_to_list(self.loss_weights_col, ignore_cols_aux)
        ignore_cols_aux = _add_this_to_list(self.ignore_classes_col, ignore_cols_aux)
        return ignore_cols_aux

    def set_training_input_size(self, schema: BitfountSchema) -> None:
        """Get the input size for model training."""
        self.input_size = len(
            [
                col
                for col in schema.feature_names()
                if col not in self.get_columns_ignored_for_training()
                and col not in schema.feature_names(SemanticType.TEXT)
            ]
        )

    def set_training_column_split_by_semantic_type(
        self, schema: BitfountSchema
    ) -> None:
        """Sets the column split by type from the schema.

        This method splits the selected columns from the dataset
        based on their semantic type.

        Args:
            schema: The `BitfountSchema` for the data.
        """
        if not self.selected_cols and not self.ignore_cols:
            # If neither selected_cols or ignore_cols are provided,
            # select all columns from schema,
            self.selected_cols = schema.feature_names()
        elif self.selected_cols:
            # Make sure we set self.ignore_cols
            self.ignore_cols = [
                feature
                for feature in schema.feature_names()
                if feature not in self.selected_cols
            ]

        # Get the list of all columns ignored for training
        ignore_cols_aux = self.get_columns_ignored_for_training()

        # Create mapping of all feature names used in training
        # together with the corresponding semantic type
        self.selected_cols_w_types: Dict[_SemanticTypeValue, List[str]] = {}
        for stype, features in schema.features.items():
            columns_stype_list: List[_SemanticTypeValue] = list(features.keys())  # type: ignore[attr-defined] # Reason: the features will always be a FeaturesDict # noqa: B950
            self.selected_cols_w_types[cast(_SemanticTypeValue, stype)] = [
                col for col in columns_stype_list if col not in ignore_cols_aux
            ]
        # Add mapping to empty list for all stypes not present
        # in the current datastructure
        all_stypes = [stype.value for stype in SemanticType]
        for stype in all_stypes:
            if stype not in self.selected_cols_w_types.keys():
                self.selected_cols_w_types[cast(_SemanticTypeValue, stype)] = []

        # Get the number of images present in the datastructure.
        self.number_of_images = len(self.image_cols) if self.image_cols else 0

    def set_columns_after_transformations(
        self, transforms: List[Dict[str, _JSONDict]]
    ) -> None:
        """Updates the selected/ignored columns based on the transformations applied.

        It updates `self.selected_cols` by adding on the new names of columns after
        transformations are applied, and removing the original columns unless
        explicitly specified to keep.

        Args:
            transforms: A list of transformations to be applied to the data.
        """
        for tfm in transforms:
            for key, value in tfm.items():
                if key == "convert_to":
                    # Column name doesn't change if we only convert type.
                    pass
                else:
                    # Check to see if any original columns are marked to keep
                    original_cols_to_keep = value.get("keep_original", [])

                    # Make a list of all the columns to be discarded
                    if isinstance(value["col"], str):
                        value["col"] = [value["col"]]
                    discard_columns = [
                        col for col in value["col"] if col not in original_cols_to_keep
                    ]
                    new_columns = [f"{col}_{key}" for col in value["col"]]
                    self.selected_cols.extend(new_columns)
                    self.ignore_cols.extend(discard_columns)
                    self.selected_cols = [
                        col for col in self.selected_cols if col not in discard_columns
                    ]

    def apply_dataset_transformations(self, datasource: DataSource) -> DataSource:
        """Applies transformations to whole dataset.

        Args:
            datasource: The `DataSource` object to be transformed.

        Returns:
            datasource: The transformed datasource.
        """
        if self.dataset_transforms:
            # TODO: [BIT-1167] Process dataset transformations
            raise NotImplementedError()

        return datasource

    def get_batch_transformations(self) -> Optional[List[BatchTimeOperation]]:
        """Returns batch transformations to be performed as callables.

        Returns:
            A list of batch transformations to be passed to
                TransformationProcessor.
        """
        if self.batch_transforms is not None:
            parser = TransformationsParser()
            transformations, _ = parser.deserialize_transformations(
                self.batch_transforms
            )
            return cast(List[BatchTimeOperation], transformations)
        return None

    class _Schema(MarshmallowSchema):

        target = fields.Raw(required=True)
        ignore_cols = fields.List(fields.Str(), allow_none=True)
        loss_weights_col = fields.Str(allow_none=True)
        multihead_col = fields.Str(allow_none=True)
        ignore_classes_col = fields.Str(allow_none=True)
        batch_transforms = fields.List(
            fields.Dict(
                keys=fields.Str(),
                values=fields.Dict(keys=fields.Str()),
            ),
            allow_none=True,
        )
        dataset_transforms = fields.List(
            fields.Dict(
                keys=fields.Str(),
                values=fields.Dict(keys=fields.Str()),
            ),
            allow_none=True,
        )

        @post_load
        def recreate_datastructure(
            self, data: _JSONDict, **_kwargs: Any
        ) -> DataStructure:
            """Recreates DataStructure."""
            return DataStructure(**data)
