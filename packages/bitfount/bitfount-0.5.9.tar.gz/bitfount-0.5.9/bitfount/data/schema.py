"""Classes concerning data schemas."""
from __future__ import annotations

import collections
import copy
import logging
from os import PathLike
from typing import (
    Any,
    Dict,
    List,
    Mapping,
    MutableMapping,
    Optional,
    Sequence,
    Tuple,
    Union,
    cast,
)

from PIL import Image
import databricks.koalas as ks
from marshmallow import fields, post_dump, post_load, pre_dump, pre_load
import numpy as np
import pandas as pd
from pandas._typing import Dtype
from pandas.core.dtypes.common import is_numeric_dtype
import yaml

import bitfount
from bitfount.data.datasource import DataSource
from bitfount.data.types import (
    CategoricalRecord,
    ContinuousRecord,
    ImageRecord,
    SemanticType,
    TextRecord,
    _CamelCaseSchema,
    _FeatureDict,
    _SemanticTypeRecord,
    _SemanticTypeValue,
)
from bitfount.data.utils import _hash_str
from bitfount.exceptions import BitfountError
from bitfount.types import _DataFrameLib, _DataFrameType, _JSONDict
from bitfount.utils import _add_this_to_list, _get_df_library_type

logger = logging.getLogger(__name__)


class _BitfountSchemaMarshmallowMixIn:
    """MixIn class for Schema serialization."""

    def dump(self, file_path: PathLike) -> None:
        """Dumps the schema as a yaml file.

        Args:
            file_path: The path where the file should be saved

        Returns:
            none
        """
        with open(file_path, "w") as file:
            file.write(self.dumps())

    def dumps(self) -> Any:
        """Produces the YAML representation of the schema object.

        Returns:
            str: The YAML representation of the schema
        """
        return yaml.dump(self.to_json(), sort_keys=False)

    def to_json(self) -> _JSONDict:
        """Turns a schema object into a JSON compatible dictionary.

        Returns:
            dict: A simple JSON compatible representation of the Schema
        """
        # Our self._Schema() objects are dumped as JSON-compatible dicts
        return cast(_JSONDict, self._Schema().dump(self))

    @classmethod
    def load(cls, data: Mapping) -> BitfountSchema:
        """Loads the schema from a dictionary.

        Args:
            data: The data to load the schema from.

        Returns:
            BitfountSchema: A _Schema instance corresponding to the dictionary.
        """
        # @post_load guarantees this will be a BitfountSchema
        schema: BitfountSchema = cls._Schema().load(data)
        return schema

    @classmethod
    def load_from_file(cls, file_path: Union[str, PathLike]) -> BitfountSchema:
        """Loads the schema from a yaml file.

        This contains validation errors to help fix an invalid YAML file.
        """
        with open(file_path, "r") as f:
            schema_as_yaml = yaml.safe_load(f)
        return cls.load(schema_as_yaml)

    class _Schema(_CamelCaseSchema):
        categorical_features = fields.List(fields.Nested(CategoricalRecord._Schema))
        continuous_features = fields.List(fields.Nested(ContinuousRecord._Schema))
        image_features = fields.List(fields.Nested(ImageRecord._Schema))
        text_features = fields.List(fields.Nested(TextRecord._Schema))

        # TODO: [BIT-1057] Consider moving metadata to be a separate part of the
        #       output YAML.
        # To maintain backwards compatibility with schemas that may not contain
        # metadata we use a default value.
        metadata = fields.Method(
            serialize="dump_metadata", deserialize="load_metadata", load_default=dict
        )

        @staticmethod
        def dump_metadata(obj: BitfountSchema) -> Dict[str, str]:
            """Creates and dumps metadata for the schema."""
            return {"bitfount_version": bitfount.__version__, "hash": obj.hash}

        @staticmethod
        def load_metadata(value: Dict[str, str]) -> Dict[str, str]:
            """Loads the metadata dict."""
            return value

        @pre_dump
        def dump_feature_values(
            self, data: BitfountSchema, **_kwargs: Any
        ) -> BitfountSchema:
            """Modifies features to dump features as a list instead of dictionaries.

            To ensure our YAML is clear, we pre-process our object into lists before
            dumping it. We don't want to modify the actual schema object, as it will
            affect its use, so we create a temporary one just for dumping to YAML.
            """
            temp_schema = copy.deepcopy(data)
            for stype in data.features:
                setattr(
                    temp_schema,
                    f"{stype}_features",
                    list(data.features[cast(_SemanticTypeValue, stype)].values()),
                )

            return temp_schema

        @post_load
        def recreate_schema(self, data: _JSONDict, **_kwargs: Any) -> BitfountSchema:
            """Recreates Schema."""
            new_schema = BitfountSchema()

            for key in data:
                if key.endswith("_features"):
                    stype = key.replace("_features", "")
                    new_schema.features[cast(_SemanticTypeValue, stype)] = {
                        feature.feature_name: feature for feature in data[key]
                    }

            # Ensure existing datasources hash is loaded if present
            new_schema._orig_hash = data["metadata"].get("hash")

            return new_schema

        @post_dump
        def combine_features(self, data: _JSONDict, **kwargs: Any) -> _JSONDict:
            """Combines features belonging to different semantic types under one key.

            After combining the features into one list, it also sorts all the features
            by featureName.
            """
            new_data = {}
            new_data["features"] = [
                item for key in data if key.endswith("Features") for item in data[key]
            ]
            # sort features alphabetically
            # Type ignore due to this bug: https://github.com/python/mypy/issues/9656
            new_data["features"] = sorted(
                new_data["features"], key=lambda d: d["featureName"]  # type: ignore[no-any-return] # Reason: see comment above # noqa: B950
            )
            new_data["metadata"] = data["metadata"]
            return new_data

        @pre_load
        def split_features(self, data: _JSONDict, **kwargs: Any) -> _JSONDict:
            """Splits features back into a dictionary of lists by semantic type."""
            result = collections.defaultdict(list)
            features: List[_JSONDict] = data.pop("features")
            for d in features:
                result[d.pop("semanticType")].append(d)

            for semantic_type in result:
                data[f"{semantic_type}Features"] = result[semantic_type]

            return data


class BitfountSchema(_BitfountSchemaMarshmallowMixIn):
    """A schema that defines the features of a dataframe.

    It lists all the (categorical, continuous, image, and
    text) features found in the dataframe.

    Args:
        datasource: A `DataSource` to be provided to the
            constructor instead of to the `add_datasource_features()`
            method for brevity. Optional argument. Defaults to None.
        **datasource_kwargs: Additional keyword arguments to pass to
            `add_datasource_features()` alongside the datasource.

    Attributes:
           features: An ordered dictionary of features (column names).
    """

    def __init__(
        self, datasource: Optional[DataSource] = None, **datasource_kwargs: Any
    ):
        # ordered dictionaries of features (column names)
        self.features: _FeatureDict = _FeatureDict()

        # self._orig_hash is used to store the hash when loading a previously
        # generated schema.
        self._orig_hash: Optional[str] = None
        self._datasource_hashes: List[str] = []
        # Used to stop any more datasources from being added
        self._frozen: bool = False

        if datasource is not None:
            self.add_datasource_features(datasource, **datasource_kwargs)

    @property
    def hash(self) -> str:
        """The hash of this schema.

        This relates to the DataSource(s) that were used in the generation of this
        schema to assure that this schema is used against compatible data sources.

        Returns:
            A sha256 hash of the `_datasource_hashes`.
        """
        # Must be sorted to ensure ordering of DataSources being added doesn't
        # change things.
        frozen_hashes: str = str(sorted(self._datasource_hashes))
        return _hash_str(frozen_hashes)

    @staticmethod
    def _dtype_based_stype_split(
        data: _DataFrameType, ignore_cols: Optional[Sequence[str]] = None
    ) -> Dict[SemanticType, List[str]]:
        """Returns dictionary of Semantic types and the corresponding columns in `data`.

        We first call `convert_dtypes` on the data to convert older pandas dtypes to
        newer ones. This call is idempotent and allows us to identify the data type of
        columns with the `object` dtype.
        """
        converted_data = data
        if ignore_cols:
            converted_data = converted_data.drop(columns=ignore_cols, errors="ignore")
        dataframe_lib = _get_df_library_type(data)

        if dataframe_lib == _DataFrameLib.PANDAS:
            converted_data = converted_data.convert_dtypes()
        else:
            # TODO: [BIT-1095] have a pyspark workaround for this `convert_dtypes` call
            # when we switch to pyspark from koalas
            # https://issues.apache.org/jira/browse/SPARK-37334
            pass

        semantic_types: Dict[SemanticType, List[str]] = {
            stype: [] for stype in SemanticType
        }

        for col, typ in converted_data.dtypes.items():
            if isinstance(typ, pd.StringDtype):
                semantic_types[SemanticType.TEXT].append(col)
            elif isinstance(typ, pd.BooleanDtype) or typ == bool:
                semantic_types[SemanticType.CATEGORICAL].append(col)
            elif is_numeric_dtype(typ):
                # Booleans get interpereted as continuous so we must define them as
                # categorical before this function is called
                semantic_types[SemanticType.CONTINUOUS].append(col)
            else:
                # By default everything else will be interpreted as categorical.
                # This should only happen for columns which remain as `object` because
                # pandas is having trouble deciphering their true type
                semantic_types[SemanticType.CATEGORICAL].append(col)

        return {k: v for k, v in semantic_types.items() if len(v) > 0}

    def feature_names(self, semantic_type: Optional[SemanticType] = None) -> List[str]:
        """Returns the names of all the features in the schema.

        Args:
            semantic_type (SemanticType, optional): if semantic type is provided, only
                the feature names corresponding to the semantic type are returned.
                Defaults to None.

        Returns:
            features: A list of feature names.
        """
        if semantic_type is not None:
            stype = cast(_SemanticTypeValue, semantic_type.value)
            if stype in self.features:
                features = list(self.features[stype])
            else:
                logger.debug(f"There are no features with semantic type {stype}")
                features = []

        else:
            features = [
                feature_name
                for stype in self.features
                for feature_name in self.features[cast(_SemanticTypeValue, stype)]
            ]
        return features

    def get_categorical_feature_size(self, var: Union[str, List[str]]) -> int:
        """Gets the column dimensions.

        Args:
            var: A column name or a list of column names for which
                to get the dimensions.

        Returns:
            The number of unique value in the categorical column.
        """
        if isinstance(var, list):
            var = var[0]

        if "categorical" not in self.features:
            raise ValueError("No categorical features.")
        elif var not in self.features["categorical"]:
            raise ValueError(f"{var} feature not found in categorical features.")

        return self.features["categorical"][var].encoder.size

    def _add_categorical_feature(
        self,
        name: str,
        values: Union[np.ndarray, pd.Series, ks.Series],
        dtype: Optional[Union[Dtype, np.dtype]] = None,
        description: Optional[str] = None,
    ) -> None:
        """Adds the given categorical, with list of values to the schema."""
        if (
            "categorical" not in self.features
            or name not in self.features["categorical"]
        ):

            CategoricalRecord.add_record_to_schema(
                self,
                feature_name=name,
                dtype=dtype,
                description=description,
            )
        self.features["categorical"][name].encoder.add_values(values)

    def _combine_existing_stypes_with_forced_stypes(
        self,
        existing_stypes: MutableMapping[SemanticType, List[str]],
        forced_stype: MutableMapping[_SemanticTypeValue, List[str]],
        dataframe: _DataFrameType,
    ) -> MutableMapping[SemanticType, List[str]]:
        """Combine the exiting semantic types with the forced semantic types."""
        for new_stype, feature_list in forced_stype.items():
            try:
                stype = SemanticType(new_stype)

                if stype not in existing_stypes.keys():
                    existing_stypes[stype] = []
                existing_stypes[stype] = _add_this_to_list(
                    feature_list, existing_stypes[stype]
                )
            except ValueError:
                logger.warning(
                    f"Given semantic type {new_stype} is not currently supported. "
                    f"Defaulting to split based on dtype."
                )
                dtype_features = self._dtype_based_stype_split(
                    dataframe[feature_list], []
                )
                stype = list(dtype_features.keys())[0]
                if stype not in existing_stypes.keys():
                    existing_stypes[stype] = []
                existing_stypes[stype] = _add_this_to_list(
                    feature_list, existing_stypes[stype]
                )
        return existing_stypes

    def _add_dataframe_features(
        self,
        dataframe: _DataFrameType,
        ignore_cols: List[str],
        force_stype: MutableMapping[_SemanticTypeValue, List[str]],
        descriptions: Mapping[str, str],
    ) -> None:
        """Add given dataframe to the schema.

        Adds all the features in the dataframe to the schema, using the dtype to decide
        the semantic type of the feature.
        """
        for item in force_stype.values():
            ignore_cols = _add_this_to_list(item, ignore_cols)
        inferred_semantic_types = self._dtype_based_stype_split(dataframe, ignore_cols)
        semantic_types = self._combine_existing_stypes_with_forced_stypes(
            inferred_semantic_types, force_stype, dataframe
        )
        for stype, features in semantic_types.items():
            # Sort the list of features.
            # This ensures they are added in deterministic order.
            features.sort()
            for feature_name in features:
                dtype = dataframe.dtypes[feature_name]
                description = descriptions.get(feature_name)
                if stype == SemanticType.TEXT:
                    if feature_name not in self.feature_names():
                        TextRecord.add_record_to_schema(
                            self,
                            feature_name=feature_name,
                            dtype=dtype,
                            description=description,
                        )
                elif stype == SemanticType.CONTINUOUS:
                    if feature_name not in self.feature_names():
                        ContinuousRecord.add_record_to_schema(
                            self,
                            feature_name=feature_name,
                            dtype=dtype,
                            description=description,
                        )

                elif stype == SemanticType.CATEGORICAL:
                    self._add_categorical_feature(
                        name=feature_name,
                        dtype=dtype,
                        values=dataframe[feature_name],
                        description=description,
                    )
                elif stype == SemanticType.IMAGE:
                    if (
                        "image" not in self.features
                        or feature_name not in self.features["image"]
                    ):
                        ImageRecord.add_record_to_schema(
                            self,
                            feature_name=feature_name,
                            dtype=dataframe.dtypes[feature_name],
                            description=descriptions.get(feature_name),
                        )
                    record = self.features["image"][feature_name]
                    for img in dataframe[feature_name]:
                        im = Image.open(img)
                        record.dimensions[im.size] += 1
                        record.modes[im.mode] += 1
                        record.formats[im.format] += 1

    def categorical_feature_sizes(
        self, ignore_cols: Optional[Union[str, List[str]]] = None
    ) -> List[int]:
        """Returns a list of categorical feature sizes.

        Args:
            ignore_cols: The column(s) to be ignored from the schema.
        """
        if not ignore_cols:
            ignore_cols = []
        elif isinstance(ignore_cols, str):
            ignore_cols = [ignore_cols]
        return [
            self.get_categorical_feature_size(var)
            for var in self.feature_names(SemanticType.CATEGORICAL)
            if var not in ignore_cols
        ]

    def _expand_dataframe(self, dataframe: _DataFrameType) -> _DataFrameType:
        """Expands dataframe to include missing columns specified in the schema.

        Simply adds columns populated with default values: 'nan' for categorical
        and text columns and '0' for continuous columns.

        Args:
            dataframe (DataFrameType): dataframe without all the required columns

        Returns:
            DataFrameType: dataframe that includes all the required columns

        Raises:
            BitfountSchemaError: if there is a missing image column as this cannot be
                replicated.
        """
        missing_categorical_value = "nan"
        missing_text_value = "nan"
        missing_continuous_value = 0
        columns = list(dataframe.columns)

        for stype in self.features:
            # Iterate through semantic types
            for feature_name in self.features[cast(_SemanticTypeValue, stype)]:
                # Iterate through each feature in given semantic type
                if feature_name not in columns:
                    # If feature is not present in the given dataframe, add that feature
                    # with a dummy value to the dataframe
                    logger.debug(
                        f"Feature present in schema but missing in data: {feature_name}"
                    )
                    if stype == SemanticType.IMAGE.value:
                        raise BitfountSchemaError(
                            f"Missing image feature {feature_name} in dataframe. "
                            "Unable to apply schema to this dataframe"
                        )
                    elif stype == SemanticType.TEXT.value:
                        dataframe[feature_name] = missing_text_value
                    elif stype == SemanticType.CONTINUOUS.value:
                        dataframe[feature_name] = missing_continuous_value
                    elif stype == SemanticType.CATEGORICAL.value:
                        dataframe[feature_name] = missing_categorical_value
                        # adds the missing categorical value (i.e. 'nan') to the encoder
                        # for the missing categorical feature
                        self._add_categorical_feature(
                            name=feature_name,
                            values=np.array([missing_categorical_value]),
                        )
        return dataframe

    def _reduce_dataframe(
        self, dataframe: _DataFrameType, keep_cols: Optional[List[str]] = None
    ) -> _DataFrameType:
        """Drops any columns that are not part of the schema.

        Args:
            dataframe (DataFrameType): dataframe which includes extra columns
            keep_cols (Optional[List[str]]): optional list of columns to keep even if
                they are not part of the schema. Defaults to None.

        Returns:
            DataFrameType: dataframe with extra columns removed
        """
        cols_to_keep = self.feature_names()
        cols_to_keep = _add_this_to_list(keep_cols, cols_to_keep)
        return dataframe[cols_to_keep]

    def _apply_types(self, dataframe: _DataFrameType) -> _DataFrameType:
        """Applies the prescribed feature types to the dataframe.

        Args:
            dataframe (DataFrameType): dataframe with varied types

        Returns:
            DataFrameType: dataframe with types that are specified in the schema
        """
        types: Dict[str, Union[Dtype, np.dtype]] = {
            feature_name: record.dtype
            for stype in self.features
            for feature_name, record in self.features[
                cast(_SemanticTypeValue, stype)
            ].items()
        }

        if "categorical" in self.features:
            types.update(
                {
                    feature_name: record.encoder.dtype
                    for feature_name, record in self.features["categorical"].items()
                }
            )

        return dataframe.astype(types)

    def _encode_dataframe(self, data: _DataFrameType) -> _DataFrameType:
        """Encodes the dataframe categorical columns according to the schema.

        Args:
            data (DataFrameType): the dataframe to be encoded

        Raises:
            ValueError: if the encoder fails to encode a particular column

        Returns:
            DataFrameType: the dataframe with the categorical columns encoded
        """
        if "categorical" in self.features:
            for feature_name, record in self.features["categorical"].items():
                if feature_name not in data:
                    logger.warning(
                        f"Column {feature_name} is not in the dataframe. "
                        "Skipping encoding"
                    )
                    continue
                try:
                    data[feature_name] = record.encoder.transform(data[feature_name])
                except ValueError as err:
                    raise ValueError(
                        f"Could not encode column {feature_name}: {str(err)}"
                    )
        else:
            logger.info("No encoding to be done as there are no categorical features.")

        return data

    def freeze(self) -> None:
        """Freezes the schema, ensuring no more datasources can be added.

        If this schema was loaded from an already generated schema, this will
        also check that the schema is compatible with the datasources set.
        """
        self._frozen = True
        if self._orig_hash and self.hash != self._orig_hash:
            raise BitfountSchemaError(
                "This schema was generated against a different set of datasources "
                "and is incompatible with those selected. This may be due to "
                "changing column names or types. Please generate a new schema."
            )

    def unfreeze(self) -> None:
        """Unfreezes the schema, allowing more datasources to be added."""
        self._frozen = False

    def add_datasource_features(
        self,
        datasource: DataSource,
        ignore_cols: Optional[Sequence[str]] = None,
        force_stype: Optional[MutableMapping[_SemanticTypeValue, List[str]]] = None,
        descriptions: Optional[Mapping[str, str]] = None,
    ) -> None:
        """Adds datasource features to schema.

        Args:
            datasource: The `DataSource` whose features this method adds.
            ignore_cols: Columns to ignore from the `DataSource`. Defaults to None.
            force_stype: Columns for which to change the semantic type.
                Format: semantictype: [columnnames]. Defaults to None.
                Example: {'categorical': ['target_column'],
                        'continuous': ['age', 'salary']}
            descriptions: Descriptions of the features. Defaults to None.

        Raises:
            BitfountSchemaError: if the schema is already frozen
        """
        if not self._frozen:
            # Add this datasource to the hash computation list
            self._datasource_hashes.append(datasource.hash)

            if ignore_cols is None:
                ignore_cols_aux = []
            else:
                ignore_cols_aux = list(ignore_cols)

            if force_stype is None:
                force_stype = {}

            for dataframe in [
                datasource.train_set,
                datasource.validation_set,
                datasource.test_set,
            ]:
                self._add_dataframe_features(
                    dataframe=dataframe,
                    ignore_cols=ignore_cols_aux,
                    force_stype=force_stype,
                    descriptions=descriptions if descriptions is not None else {},
                )
        else:
            raise BitfountSchemaError(
                "This schema is frozen. No more datasources can be added."
            )

    def apply(
        self, dataframe: _DataFrameType, keep_cols: Optional[List[str]] = None
    ) -> _DataFrameType:
        """Applies the schema to a dataframe and returns the transformed dataframe.

        Sequentially adds missing columns to the dataframe, removes superfluous columns
        from the dataframe, changes the types of the columns in the dataframe and
        finally encodes the categorical columns in the dataframe before returning the
        transformed dataframe.

        Args:
            dataframe: The dataframe to transform.
            keep_cols: A list of columns to keep even if
                they are not part of the schema. Defaults to None.

        Returns:
            The dataframe with the transformations applied.
        """
        dataframe = self._expand_dataframe(dataframe)
        dataframe = self._reduce_dataframe(dataframe, keep_cols=keep_cols)
        dataframe = self._apply_types(dataframe)
        dataframe = self._encode_dataframe(dataframe)

        return dataframe

    def __eq__(self, other: Any) -> bool:
        """Compare two BitfountSchema objects for equality.

        For two schemas to be equal they must have the same set of features,
        including names and types. This does not require them to have come from
        the same data source though (i.e. their hashes might be different).

        Args:
            other: The other object to compare against.

        Returns:
            True if equal, False otherwise.
        """
        # Check if exact same object
        if self is other:
            return True

        # Check comparable types
        if not isinstance(other, BitfountSchema):
            return False

        def extract_features_and_types(
            schema: BitfountSchema,
        ) -> Dict[str, Dict[str, Tuple[Union[Dtype, np.dtype], SemanticType]]]:
            # Extract types from features
            return {
                feature_type: {
                    feature_name: (record.dtype, record.semantic_type)
                    for feature_name, record in cast(
                        Dict[str, _SemanticTypeRecord], records_dict
                    ).items()
                }
                for feature_type, records_dict in schema.features.items()
            }

        # Check features and their types
        if extract_features_and_types(self) != extract_features_and_types(other):
            return False

        # Otherwise, equal for our purposes
        return True


class BitfountSchemaError(BitfountError):
    """Errors related to BitfountSchema."""

    pass
