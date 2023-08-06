"""Tests for LightGBM models."""
import os
from pathlib import Path

import pytest

from bitfount.backends.lightgbm.models.models import (
    LGBMRandomForestClassifier,
    LGBMRandomForestRegressor,
)
from bitfount.data.datasource import DataSource
from bitfount.data.datastructure import DataStructure
from bitfount.data.schema import BitfountSchema
from tests.bitfount.models.test_models import SERIALIZED_MODEL_NAME, assert_vars_equal
from tests.utils.helper import (
    assert_results,
    backend_test,
    create_datasource,
    create_datastructure,
    create_schema,
    integration_test,
    unit_test,
)


@pytest.fixture
def datastructure() -> DataStructure:
    """Fixture for datastructure."""
    return create_datastructure()


@pytest.fixture
def datasource() -> DataSource:
    """Fixture for datasource."""
    return create_datasource(classification=True)


@pytest.fixture
def schema() -> BitfountSchema:
    """Fixture for datastructure with schema."""
    return create_schema(classification=True)


@backend_test
class TestLGBMRandomForest:
    """Test LGBMRandomForest model classes."""

    @integration_test
    def test_classification(
        self,
        datasource: DataSource,
        datastructure: DataStructure,
        schema: BitfountSchema,
    ) -> None:
        """Tests LGBMRandomForestClassifier training."""
        random_forest = LGBMRandomForestClassifier(
            datastructure=datastructure,
            schema=schema,
            n_estimators=10,
            early_stopping_rounds=2,
            verbose=-1,
        )
        random_forest.fit(datasource)
        assert_results(model=random_forest)

    @integration_test
    def test_regression(
        self, datasource: DataSource, datastructure: DataStructure
    ) -> None:
        """Tests LGBMRandomForestRegressor training."""
        random_forest = LGBMRandomForestRegressor(
            datastructure=datastructure, schema=BitfountSchema(), verbose=-1
        )
        random_forest.fit(datasource)
        assert_results(model=random_forest)

    @integration_test
    def test_serialization(
        self,
        datasource: DataSource,
        datastructure: DataStructure,
        schema: BitfountSchema,
        tmp_path: Path,
    ) -> None:
        """Tests serialize() and deserialize() methods."""
        random_forest = LGBMRandomForestClassifier(
            datastructure=datastructure,
            schema=schema,
            n_estimators=10,
            early_stopping_rounds=10,
            verbose=-1,
        )

        random_forest.fit(datasource)
        random_forest.serialize(str(tmp_path / SERIALIZED_MODEL_NAME))
        assert os.path.exists(tmp_path / SERIALIZED_MODEL_NAME)
        rf_model = LGBMRandomForestClassifier(
            datastructure=datastructure,
            schema=schema,
            n_estimators=10,
            early_stopping_rounds=10,
            verbose=-1,
        )
        rf_model.fit(datasource)
        rf_model.deserialize(str(tmp_path / SERIALIZED_MODEL_NAME))
        rf_model.evaluate(random_forest.test_set)

    @unit_test
    def test_evaluate_no_test_dl_error(self, datastructure: DataStructure) -> None:
        """Tests that evaluate raises error with no test_dl."""
        random_forest = LGBMRandomForestRegressor(
            datastructure=datastructure, schema=BitfountSchema(), verbose=-1
        )
        with pytest.raises(ValueError):
            random_forest.evaluate()

    @unit_test
    def test_fit_no_validation_dl(
        self,
        datasource: DataSource,
        datastructure: DataStructure,
        schema: BitfountSchema,
    ) -> None:
        """Tests that evaluate called without test data raises error."""
        random_forest = LGBMRandomForestClassifier(
            datastructure=datastructure,
            schema=schema,
            n_estimators=10,
            early_stopping_rounds=2,
            verbose=-1,
        )
        random_forest._add_datasource_to_schema(datasource)
        random_forest._set_dataloaders()
        random_forest.validation_dl = None
        train_df, val_df = random_forest._create_dataset()
        assert val_df is None


@backend_test
@unit_test
class TestMarshmallowSerialization:
    """Test Marshmallow Serialization for LightGBM models."""

    def test_rf_classifier_serialization(
        self, datastructure: DataStructure, schema: BitfountSchema
    ) -> None:
        """Tests serialization with LGBMRandomForestClassifier."""
        model = LGBMRandomForestClassifier(datastructure=datastructure, schema=schema)
        model_schema = model.get_schema()
        serialized_model = model_schema().dump(model)
        deserialized_model = model_schema().load(serialized_model)
        assert_vars_equal(vars(model), vars(deserialized_model))

    def test_rf_regressor_serialization(self, datastructure: DataStructure) -> None:
        """Tests serialization with LGBMRandomForestRegressor."""
        model = LGBMRandomForestRegressor(
            datastructure=datastructure, schema=BitfountSchema()
        )
        schema = model.get_schema()
        serialized_model = schema().dump(model)
        deserialized_model = schema().load(serialized_model)
        assert_vars_equal(vars(model), vars(deserialized_model))
