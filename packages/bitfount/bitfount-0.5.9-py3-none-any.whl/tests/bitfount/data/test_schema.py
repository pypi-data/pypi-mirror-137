"""Tests schema.py."""
import copy
from pathlib import Path
import re
from typing import Dict, List, MutableMapping, cast
from unittest.mock import Mock, PropertyMock, create_autospec

from marshmallow import ValidationError
import numpy as np
import pandas as pd
from pandas.core.dtypes.common import pandas_dtype
from pandas.testing import assert_frame_equal
import pytest
from pytest import fixture
from pytest_mock import MockerFixture
import yaml

import bitfount
from bitfount.data.datasource import DataSource
from bitfount.data.schema import BitfountSchema, BitfountSchemaError
from bitfount.data.types import (
    CategoricalRecord,
    ContinuousRecord,
    SemanticType,
    _SemanticTypeValue,
)
from bitfount.data.utils import _hash_str
from tests.utils.helper import create_dataset, unit_test

SCHEMA_DUMP_PATH: str = "schema_dump_test.yaml"


@fixture
def data() -> pd.DataFrame:
    """Returns dataset."""
    return cast(pd.DataFrame, create_dataset())


@fixture
def datasource(data: pd.DataFrame) -> DataSource:
    """Returns datasource."""
    return DataSource(data, seed=420)


@fixture
def image_datasource() -> DataSource:
    """Datasource with image_col for testing."""
    data = create_dataset(image=True)
    return DataSource(data, image_col=["image"])


@fixture
def schema() -> BitfountSchema:
    """An EMPTY BitfountSchema object."""
    return BitfountSchema()


@fixture
def schema_with_data(datasource: DataSource, schema: BitfountSchema) -> BitfountSchema:
    """Schema with datasource already set."""
    schema.add_datasource_features(datasource)
    return schema


@unit_test
class TestBitfountSchemaMarshmallowMixIn:
    """Tests we can save and load schema as yaml."""

    @fixture
    def empty_schema_hash(self) -> str:
        """The expected hash for a schema with no datasources."""
        empty_list: list = []
        return _hash_str(str(empty_list))

    @fixture
    def bitfount_version(self) -> str:
        """The bitfount version."""
        return bitfount.__version__

    @fixture
    def empty_schema_metadata(
        self, bitfount_version: str, empty_schema_hash: str
    ) -> Dict[str, str]:
        """The expected metadata for a schema with no datasources."""
        return {"bitfount_version": bitfount_version, "hash": empty_schema_hash}

    def test_schema_dump_load(
        self, datasource: DataSource, schema: BitfountSchema, tmp_path: Path
    ) -> None:
        """Tests dumping and loading data schema."""
        schema.add_datasource_features(datasource)
        file_path = tmp_path / SCHEMA_DUMP_PATH
        schema.dump(file_path)
        loaded_schema = BitfountSchema.load_from_file(file_path)

        assert (
            yaml.safe_load(schema.dumps())["features"]
            == yaml.safe_load(loaded_schema.dumps())["features"]
        )

    def test_dump_produces_metadata(
        self, bitfount_version: str, empty_schema_hash: str, schema: BitfountSchema
    ) -> None:
        """Tests that metadata is output in the schema dump."""
        dumped = schema.dumps()
        loaded_yaml = yaml.safe_load(dumped)
        assert loaded_yaml["metadata"] == {
            "hash": empty_schema_hash,
            "bitfount_version": bitfount_version,
        }

    def test_load_works_without_metadata(
        self, datasource: DataSource, schema: BitfountSchema, tmp_path: Path
    ) -> None:
        """Tests loading works if metadata tag not present."""
        schema.add_datasource_features(datasource)
        dumped = schema.dumps()

        # Remove metadata from dumped schema and save to file
        loaded_yaml = yaml.safe_load(dumped)
        del loaded_yaml["metadata"]
        assert "metadata" not in loaded_yaml
        file_path = tmp_path / "schema.yaml"
        with open(file_path, "w") as f:
            yaml.dump(loaded_yaml, f)

        # Load as BitfountSchema
        loaded_schema = BitfountSchema.load_from_file(file_path)

        # Check orig_hash not set (outcome of metadata loading)
        assert loaded_schema._orig_hash is None

    def test_schema_dump_load_sorts_keys_alphabetically(
        self, datasource: DataSource, tmp_path: Path
    ) -> None:
        """Tests that key ordering is made alphabetical by dump and load."""
        schema = BitfountSchema()
        schema.add_datasource_features(datasource)

        file_path = tmp_path / SCHEMA_DUMP_PATH
        schema.dump(file_path)
        loaded_schema = BitfountSchema.load_from_file(file_path)

        for stype in schema.features:
            semantic_type = SemanticType(stype)
            original_feature_names = schema.feature_names(semantic_type)
            loaded_feature_names = loaded_schema.feature_names(semantic_type)
            assert sorted(original_feature_names) == loaded_feature_names

    def test_schema_json_dump_has_correct_casing(
        self, empty_schema_metadata: Dict[str, str]
    ) -> None:
        """Tests camelCased output of JSON dump.

        We don't want to be changing the casing of fields that are from our dataset,
        i.e. feature names, categorical classes, but we do want python variable names
        to be camelCased so that they are consistent with the JSON format.
        """
        schema = BitfountSchema()
        schema.features["continuous"] = {
            "snake_cased_name2": ContinuousRecord(
                "snake_cased_name2", pandas_dtype("float32")
            ),
            "camelCasedName2": ContinuousRecord(
                "camelCasedName2", pandas_dtype("float32")
            ),
        }

        record_with_encoder_one = CategoricalRecord(
            feature_name="snake_cased_name1", dtype=pd.StringDtype()
        )
        record_with_encoder_two = CategoricalRecord(
            feature_name="camelCasedName1", dtype=pd.StringDtype()
        )

        record_with_encoder_one.encoder.add_values(
            np.array(["these_are", "snake_cased"])
        )
        record_with_encoder_two.encoder.add_values(np.array(["theseAre", "camelCased"]))

        schema.features["categorical"] = {
            "snake_cased_name1": record_with_encoder_one,
            "camelCasedName1": record_with_encoder_two,
        }

        dumped_schema = schema.dumps()
        expected_schema = yaml.dump(
            {
                "features": [
                    {
                        "featureName": "camelCasedName1",
                        "description": None,
                        "dtype": "string",
                        "encoder": {"classes": {"camelCased": 0, "theseAre": 1}},
                        "semanticType": "categorical",
                    },
                    {
                        "featureName": "camelCasedName2",
                        "description": None,
                        "dtype": "float32",
                        "semanticType": "continuous",
                    },
                    {
                        "featureName": "snake_cased_name1",
                        "description": None,
                        "dtype": "string",
                        "encoder": {"classes": {"snake_cased": 0, "these_are": 1}},
                        "semanticType": "categorical",
                    },
                    {
                        "featureName": "snake_cased_name2",
                        "description": None,
                        "dtype": "float32",
                        "semanticType": "continuous",
                    },
                ],
                "metadata": empty_schema_metadata,
            },
            sort_keys=False,
        )
        assert dumped_schema == expected_schema

    def test_schema_load_invalid_stype(
        self, datasource: DataSource, tmp_path: Path
    ) -> None:
        """Tests that semantic types must be predefined in the Enum."""
        schema = BitfountSchema()
        schema.add_datasource_features(datasource)
        file_path = tmp_path / SCHEMA_DUMP_PATH
        schema.dump(file_path)

        # Read in the file
        with open(file_path, "r") as file:
            filedata = file.read()

        # Replace the target string
        filedata = filedata.replace("continuous", "not_real_stype")

        # Write the file out again
        with open(file_path, "w") as file:
            file.write(filedata)

        with pytest.raises(ValidationError, match="['Unknown field.']"):
            BitfountSchema.load_from_file(file_path)

    def test_schema_load_invalid_dtype(
        self, datasource: DataSource, tmp_path: Path
    ) -> None:
        """Tests schema load fails if invalid dtype.

        Tests that a custom error message is reported when an invalid dtype is
        provided to a ContinuousRecord.
        """
        schema = BitfountSchema()
        schema.add_datasource_features(datasource)

        schema.features["continuous"]["A"].dtype = "THIS_IS_NOT_A_VALID_DTYPE"

        file_path = tmp_path / SCHEMA_DUMP_PATH
        schema.dump(file_path)
        with pytest.raises(
            ValidationError,
            match="Continuous record `dtype` expected a valid np.dtype or a pandas"
            + " dtype but received: `THIS_IS_NOT_A_VALID_DTYPE`.",
        ):
            BitfountSchema.load_from_file(file_path)

    def test_schema_with_image_dump_load(
        self, image_datasource: DataSource, schema: BitfountSchema, tmp_path: Path
    ) -> None:
        """Tests dumping and (re)loading a schema gives equal item."""
        file_path = tmp_path / SCHEMA_DUMP_PATH
        schema.add_datasource_features(image_datasource)
        schema.dump(file_path)
        loaded_schema = BitfountSchema.load_from_file(file_path)

        assert (
            yaml.safe_load(schema.dumps())["features"]
            == yaml.safe_load(loaded_schema.dumps())["features"]
        )


@unit_test
class TestBitfountSchema:
    """Tests BitfountSchema class."""

    def test_schema_add_datasource(
        self, datasource: DataSource, schema: BitfountSchema
    ) -> None:
        """Checks ability to add a dataset."""
        schema.add_datasource_features(datasource)
        assert len(schema.feature_names()) == len(datasource.data.columns)

        assert "I" in schema.features["text"]  # I's values are letters of alphabet
        assert (
            schema.features["categorical"]["M"].encoder.size == 2
        )  # M's values are boolean

    def test_schema_expand_dataframe_str(self, schema: BitfountSchema) -> None:
        """Checks we can add extend when columns have string types."""
        data1 = pd.DataFrame([["a", "b"], ["c", "d"]], columns=["A", "B"])
        data2 = pd.DataFrame([["a", "b"], ["c", "d"]], columns=["B", "C"])
        expect1 = pd.DataFrame(
            [["a", "b", "nan"], ["c", "d", "nan"]], columns=["A", "B", "C"]
        )
        expect2 = pd.DataFrame(
            [["a", "b", "nan"], ["c", "d", "nan"]], columns=["B", "C", "A"]
        )
        schema.add_datasource_features(DataSource(data1))
        schema.add_datasource_features(DataSource(data2))
        data1_exp = schema._expand_dataframe(data1)
        data2_exp = schema._expand_dataframe(data2)
        assert_frame_equal(data1_exp, expect1)
        assert_frame_equal(data2_exp, expect2)

    def test_schema_expand_dataframe_bool(self, schema: BitfountSchema) -> None:
        """Checks we can add extend when columns have bool types."""
        data1 = pd.DataFrame([[True, False], [True, False]], columns=["A", "B"])
        data2 = pd.DataFrame([[True, False], [True, False]], columns=["B", "C"])
        expect1 = pd.DataFrame(
            [[True, False, "nan"], [True, False, "nan"]],
            columns=["A", "B", "C"],
        )
        expect2 = pd.DataFrame(
            [[True, False, "nan"], [True, False, "nan"]],
            columns=["B", "C", "A"],
        )

        schema.add_datasource_features(DataSource(data1))
        schema.add_datasource_features(DataSource(data2))
        data1_exp = schema._expand_dataframe(data1)
        data2_exp = schema._expand_dataframe(data2)
        assert_frame_equal(data1_exp, expect1)
        assert_frame_equal(data2_exp, expect2)

    def test_schema_expand_dataframe_float(self, schema: BitfountSchema) -> None:
        """Checks we can add extend when columns have float types."""
        data1 = pd.DataFrame([[1.0, 2.0], [3.0, 4.0]], columns=["A", "B"])
        data2 = pd.DataFrame([[1.0, 2.0], [3.0, 4.0]], columns=["B", "C"])
        expect1 = pd.DataFrame([[1.0, 2.0, 0], [3.0, 4.0, 0]], columns=["A", "B", "C"])
        expect2 = pd.DataFrame([[1.0, 2.0, 0], [3.0, 4.0, 0]], columns=["B", "C", "A"])

        schema.add_datasource_features(DataSource(data1))
        schema.add_datasource_features(DataSource(data2))
        data1_exp = schema._expand_dataframe(data1)
        data2_exp = schema._expand_dataframe(data2)
        assert_frame_equal(data1_exp, expect1)
        assert_frame_equal(data2_exp, expect2)

    def test_schema_expand_dataframe_int(self, schema: BitfountSchema) -> None:
        """Checks we can add extend when columns have float types."""
        data1 = pd.DataFrame([[1, 2], [3, 4]], columns=["A", "B"])
        data2 = pd.DataFrame([[1, 2], [3, 4]], columns=["B", "C"])
        expect1 = pd.DataFrame([[1, 2, 0], [3, 4, 0]], columns=["A", "B", "C"])
        expect2 = pd.DataFrame([[1, 2, 0], [3, 4, 0]], columns=["B", "C", "A"])
        schema.add_datasource_features(DataSource(data1))
        schema.add_datasource_features(DataSource(data2))
        data1_exp = schema._expand_dataframe(data1)
        data2_exp = schema._expand_dataframe(data2)
        assert_frame_equal(data1_exp, expect1)
        assert_frame_equal(data2_exp, expect2)

    def test_schema_add_datasource_with_image(
        self, image_datasource: DataSource, schema: BitfountSchema
    ) -> None:
        """Tests add_datasource_features works correctly."""
        schema.add_datasource_features(
            image_datasource, force_stype={"image": ["image"]}
        )
        assert len(schema.feature_names()) == len(image_datasource.data.columns)
        assert schema.features["categorical"]["M"].encoder.size == 2
        assert list(schema.features["image"].keys()) == ["image"]
        image_feature = schema.features["image"]["image"]
        assert dict(image_feature.dimensions) == {(50, 50): 4000}
        assert "RGB" in image_feature.modes
        assert "L" in image_feature.modes
        assert dict(image_feature.formats) == {"PNG": 4000}

    def test_schema_add_datasource_without_force_stype_doesnt_contain_image_col(
        self,
        image_datasource: DataSource,
        schema: BitfountSchema,
    ) -> None:
        """Tests that image col is not added to images."""
        schema.add_datasource_features(image_datasource)
        assert "image" not in schema.features

    def test_force_stypes(
        self, image_datasource: DataSource, schema: BitfountSchema
    ) -> None:
        """Tests that all force_stypes are added to schema."""
        force_stype: MutableMapping[_SemanticTypeValue, List[str]]
        force_stype = {
            "categorical": ["M", "J"],
            "continuous": ["A"],
            "text": ["N"],
            "image": ["image"],
            "blah": ["B"],  # type: ignore[dict-item] # Reason: see below.
        }
        # Added the 'blah' dict key to check that if a value is given a semantic type
        # which we don't support, it defaults to the semantic value based
        # on dtype.
        schema.add_datasource_features(image_datasource, force_stype=force_stype)
        assert "M" in schema.features["categorical"]
        assert "J" in schema.features["categorical"]
        assert "A" in schema.features["continuous"]
        assert "N" in schema.features["text"]
        assert "B" in schema.features["continuous"]
        assert "image" in schema.features["image"]

    def test_stype_images(self) -> None:
        """Tests multiple images added to schema."""
        data = create_dataset(classification=False, multiimage=True, img_size=2)
        ds = DataSource(data[["image1", "image2", "TARGET"]])
        force_stype: MutableMapping[_SemanticTypeValue, List[str]]
        force_stype = {"image": ["image1", "image2"], "text": ["TARGET"]}
        schema = BitfountSchema()
        schema.add_datasource_features(ds, force_stype=force_stype)
        assert "image1" in schema.features["image"]
        assert "image2" in schema.features["image"]
        assert "TARGET" in schema.features["text"]

    def test_encode_dataframe(self, schema: BitfountSchema) -> None:
        """Tests schema encodes dataframe correctly."""
        data = pd.DataFrame([["a", "b"], ["c", "d"]], columns=["A", "B"])
        schema.add_datasource_features(
            DataSource(data), force_stype={"categorical": ["A", "B"]}
        )
        expect = pd.DataFrame(
            [
                [
                    schema.features["categorical"]["A"].encoder.classes["a"],
                    schema.features["categorical"]["B"].encoder.classes["b"],
                ],
                [
                    schema.features["categorical"]["A"].encoder.classes["c"],
                    schema.features["categorical"]["B"].encoder.classes["d"],
                ],
            ],
            columns=["A", "B"],
        )
        data_exp = schema._encode_dataframe(data)
        assert_frame_equal(data_exp, expect)

    def test_reduce_dataframe(self, schema: BitfountSchema) -> None:
        """Tests reduce_dataframe removes appropriate columns."""
        data = pd.DataFrame([["a", "b"], ["c", "d"]], columns=["A", "B"])
        schema.add_datasource_features(DataSource(data))
        data2 = pd.DataFrame(
            [["a", "b", "c"], ["d", "e", "f"]], columns=["A", "B", "C"]
        )
        expect = pd.DataFrame([["a", "b"], ["d", "e"]], columns=["A", "B"])
        data_exp = schema._reduce_dataframe(data2)
        data_exp = data_exp.reindex(sorted(data_exp.columns), axis=1)
        assert_frame_equal(data_exp, expect)

    def test_apply_types(self, schema: BitfountSchema) -> None:
        """Tests apply_types changes types of columns appropriately."""
        data = pd.DataFrame([[1.0, 2.0], [3.0, 4.0]], columns=["A", "B"])
        schema.add_datasource_features(DataSource(data))
        data2 = pd.DataFrame([[5, 6], [7, 8]], columns=["A", "B"])
        expect = pd.DataFrame([[5.0, 6.0], [7.0, 8.0]], columns=["A", "B"])
        data_exp = schema._apply_types(data2)
        assert_frame_equal(data_exp, expect)

    def test_schema_not_frozen_when_created(self, schema: BitfountSchema) -> None:
        """Test that a newly created schema is not frozen."""
        assert schema._frozen is False

    def test_schema_freeze(self, schema: BitfountSchema) -> None:
        """Test that BitfountSchema.freeze() freezes."""
        schema.freeze()
        assert schema._frozen is True

    def test_schema_unfreeze(self, schema: BitfountSchema) -> None:
        """Test that BitfountSchema.unfreeze() unfreezes."""
        schema.freeze()
        assert schema._frozen is True
        schema.unfreeze()
        assert schema._frozen is False

    def test_datasource_cannot_be_added_when_frozen(
        self, datasource: DataSource, schema: BitfountSchema
    ) -> None:
        """Tests that add_datasource_features() fails when the schema is frozen."""
        schema.freeze()
        with pytest.raises(
            BitfountSchemaError,
            match=re.escape("This schema is frozen. No more datasources can be added."),
        ):
            schema.add_datasource_features(datasource)

    def test_hash(self, schema: BitfountSchema) -> None:
        """Tests that hash generation works."""
        schema._datasource_hashes = ["world", "hello"]

        # Should sort the stored "hashes"
        assert schema.hash == _hash_str(str(["hello", "world"]))

    def test_freeze_raises_exception_if_hash_mismatch(
        self, schema: BitfountSchema
    ) -> None:
        """Tests that freeze raises an exception if previous hash doesn't match."""
        schema._orig_hash = "not_the_same_hash"
        with pytest.raises(
            BitfountSchemaError,
            match=re.escape(
                "This schema was generated against a different set of datasources "
                "and is incompatible with those selected. This may be due to "
                "changing column names or types. Please generate a new schema."
            ),
        ):
            schema.freeze()

    def test_add_datasource_features_adds_to_hash_list(
        self, datasource: DataSource, mocker: MockerFixture, schema: BitfountSchema
    ) -> None:
        """Checks add_datasource_features() adds to hash list.

        Each added datasource needs to be recorded, so we use the hash list to
        achieve this.
        """
        # Mock out datasource.hash
        mock_hash = PropertyMock(return_value="datasource_hash")
        mocker.patch.object(DataSource, "hash", mock_hash)

        assert schema._datasource_hashes == []

        schema.add_datasource_features(datasource)

        assert schema._datasource_hashes == ["datasource_hash"]
        mock_hash.assert_called_once()

    def test_categorical_feature_sizes_with_no_ignore_cols(
        self, schema: BitfountSchema
    ) -> None:
        """Schema returns all categorical sizes if no ignore_cols provided."""
        data = pd.DataFrame([[True, False], [False, True]], columns=["A", "B"])
        schema.add_datasource_features(DataSource(data))
        assert schema.categorical_feature_sizes() == [2, 2]

    def test_categorical_feature_sizes_with_ignore_cols(
        self, schema: BitfountSchema
    ) -> None:
        """Schema returns correct categorical sizes when ignore_cols is categorical."""
        data = pd.DataFrame([[True, False], [False, True]], columns=["A", "B"])
        schema.add_datasource_features(DataSource(data))
        assert schema.categorical_feature_sizes(ignore_cols="A") == [2]

    def test_get_categorical_feature_size_raises_value_error_when_there_are_no_categorical_features(  # noqa: B950
        self, schema: BitfountSchema
    ) -> None:
        """Tests that `get_categorical_feature_size` raises a ValueError appropriately.

        When there are no categorical features.
        """
        with pytest.raises(ValueError, match="No categorical features."):
            schema.get_categorical_feature_size("feature")

    def test_get_categorical_feature_size_raises_value_error_when_missing(
        self, schema: BitfountSchema
    ) -> None:
        """Tests that `get_categorical_feature_size` raises a ValueError appropriately.

        When it is missing from the list of categorical features.
        """
        schema.features["categorical"] = {"feature_1": Mock(), "feature_2": Mock()}
        with pytest.raises(
            ValueError,
            match="missing_feature feature not found in categorical features.",
        ):
            schema.get_categorical_feature_size("missing_feature")

    def test_get_categorical_feature_with_list(self, schema: BitfountSchema) -> None:
        """Tests that `get_categorical_feature_size` works properly with a list.

        If a list of features is provided, we only return the size of the encoder for
        the first element.
        """
        schema.features["categorical"] = {
            "feature_1": Mock(encoder=Mock(size=5)),
            "feature_2": Mock(),
        }
        assert schema.get_categorical_feature_size(["feature_1", "feature_2"]) == 5

    def test__eq__passes_same_item(self, schema: BitfountSchema) -> None:
        """Test __eq__ passes when items are exact same."""
        assert schema == schema

    def test__eq__passes_same_features(self, schema_with_data: BitfountSchema) -> None:
        """Test __eq__ passes when items have same features and types."""
        other_schema = copy.deepcopy(schema_with_data)

        # Check unique objects
        assert schema_with_data is not other_schema
        # Check still viewed as equal
        assert schema_with_data == other_schema

    def test__eq__fails_not_schema(self, schema: BitfountSchema) -> None:
        """Test __eq__ fails when other is not a BitfountSchema."""
        assert schema != object()

    def test__eq__fails_diff_feature_names(
        self, schema_with_data: BitfountSchema
    ) -> None:
        """Test __eq__ fails when feature names differ."""
        other_schema = copy.deepcopy(schema_with_data)

        # Remove a categorical feature
        cat_features = other_schema.features["categorical"]
        cat_features.pop(list(cat_features.keys())[0])

        assert schema_with_data != other_schema

    def test__eq__fails_diff_feature_dtypes(
        self, schema_with_data: BitfountSchema
    ) -> None:
        """Test __eq__ fails when feature dtypes differ."""
        other_schema = copy.deepcopy(schema_with_data)

        # Extract and replace dtype of a categorical feature
        cat_features = other_schema.features["categorical"]
        record = list(cat_features.values())[0]
        if record.dtype is not np.uint8:
            record.dtype = np.uint8
        else:
            record.dtype = np.uint16

        assert schema_with_data != other_schema

    def test__eq__fails_diff_feature_stypes(
        self, schema_with_data: BitfountSchema
    ) -> None:
        """Test __eq__ fails when feature stypes differ."""
        other_schema = copy.deepcopy(schema_with_data)

        # Extract and replace stype of a categorical feature
        cat_features = other_schema.features["categorical"]
        feature_name, record = list(cat_features.items())[0]
        # Create mock record with a different stype
        mock_record = create_autospec(record)
        type(mock_record).semantic_type = PropertyMock(return_value="diff_stype")
        # Set as feature
        cat_features[feature_name] = mock_record

        assert schema_with_data != other_schema


@unit_test
class TestSplittingByDtype:
    """Tests the dtype_based_stype_split static method on BitfountSchema."""

    def test_float_dtype(self) -> None:
        """Tests that floats are given the correct semantic type."""
        data = pd.DataFrame([1.0, 2.0], columns=["A"], dtype=np.float32)
        types = BitfountSchema._dtype_based_stype_split(data)
        assert types == {SemanticType.CONTINUOUS: ["A"]}

    def test_int_dtype(self) -> None:
        """Tests that integers are given the correct semantic type."""
        data = pd.DataFrame([1, 2], columns=["A"], dtype=np.int32)
        types = BitfountSchema._dtype_based_stype_split(data)
        assert types == {SemanticType.CONTINUOUS: ["A"]}

    def test_str_dtype(self) -> None:
        """Tests that strings are given the correct semantic type."""
        data = pd.DataFrame(["1", "2"], columns=["A"])
        types = BitfountSchema._dtype_based_stype_split(data)
        assert types == {SemanticType.TEXT: ["A"]}

    def test_bool_dtype(self) -> None:
        """Tests that booleans are given the correct semantic type."""
        data = pd.DataFrame([True, False], columns=["A"])
        types = BitfountSchema._dtype_based_stype_split(data)
        assert types == {SemanticType.CATEGORICAL: ["A"]}

    def test_object_dtype(self) -> None:
        """Tests that objects are given the correct semantic type."""

        class ComplexObject:
            ...

        data = pd.DataFrame([ComplexObject(), ComplexObject()], columns=["A"])
        types = BitfountSchema._dtype_based_stype_split(data)
        assert types == {SemanticType.CATEGORICAL: ["A"]}
