"""Tests for PyTorch-backed models."""
from functools import partial
import os
from pathlib import Path
from typing import Any, Dict, List, MutableMapping, cast
from unittest.mock import Mock

import numpy as np
import pandas as pd
import py
import pytest
from pytest_mock import MockerFixture
from pytorch_lightning import Trainer as LightningTrainer
from pytorch_lightning.loggers import (
    MLFlowLogger,
    NeptuneLogger,
    TensorBoardLogger,
    TestTubeLogger,
    WandbLogger,
)
from pytorch_lightning.loggers import CSVLogger
from pytorch_lightning.loggers import LightningLoggerBase as LightningLoggers
from sklearn.metrics import roc_auc_score
import torch
from torch import nn as nn
from torch.nn import Linear, ReLU
import torch_optimizer

from bitfount.backends.pytorch.models.models import (
    PyTorchImageClassifier,
    PyTorchTabularClassifier,
    TabNetClassifier,
)
from bitfount.data.datasource import DataSource
from bitfount.data.datasplitters import PercentageSplitter
from bitfount.data.datastructure import DataStructure
from bitfount.data.schema import BitfountSchema
from bitfount.data.types import _SemanticTypeValue
from bitfount.federated.modeller import Modeller
from bitfount.federated.privacy.differential import DPModellerConfig
from bitfount.metrics import (
    BINARY_CLASSIFICATION_METRICS,
    MULTICLASS_CLASSIFICATION_METRICS,
    ClassificationMetric,
    MetricCollection,
)
from bitfount.models.base_models import (
    CNNModelStructure,
    FeedForwardModelStructure,
    LoggerConfig,
    ModelContext,
    NeuralNetworkPredefinedModel,
    Optimizer,
    Scheduler,
)
from tests.bitfount import TEST_SECURITY_FILES
from tests.bitfount.models.test_models import SERIALIZED_MODEL_NAME
from tests.utils.helper import (
    AUC_THRESHOLD,
    assert_results,
    backend_test,
    create_dataset,
    create_datasource,
    create_datastructure,
    create_schema,
    get_datastructure_and_datasource,
    integration_test,
    unit_test,
)


def assert_vars_equal(vars_original: Dict[str, Any], vars_copy: Dict[str, Any]) -> None:
    """Asserts both vars() are equal."""
    for variable, value in vars_original.items():
        if not isinstance(
            value,
            (
                LightningTrainer,
                LightningLoggers,
                DataStructure,
                BitfountSchema,
            ),
        ) and variable not in ["opt_func", "scheduler_func"]:
            assert value == vars_copy[variable]
        else:
            if isinstance(value, DataStructure):
                assert value.target == vars_copy[variable].target
            elif variable == "opt_func" and value is not None:
                assert issubclass(
                    value.func, (torch.optim.Optimizer, torch_optimizer.Optimizer)
                )
                assert value.func == vars_copy[variable].func
                assert value.keywords == vars_copy[variable].keywords


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
    """Fixture for schema."""
    return create_schema(classification=True)


@backend_test
class TestPyTorchModel:
    """Test PyTorchTabularClassifier class from bitfount.models."""

    @unit_test
    def test_training_steps(
        self, datasource: DataSource, datastructure: DataStructure
    ) -> None:
        """Test that training works with steps instead of epochs."""
        model = PyTorchTabularClassifier(
            datastructure=datastructure, schema=BitfountSchema(), steps=10
        )
        assert (
            model._pl_trainer.max_epochs  # type:ignore[attr-defined] # Reason: error: "Trainer" has no attribute "max_epochs" even though it does # noqa: B950
            is None
        )
        assert (
            model._pl_trainer.max_steps  # type:ignore[attr-defined] # Reason: see below
            == 10
        )  # Reason: error: "Trainer" has no attribute "max_steps" even though it does
        model.fit(datasource)

    @unit_test
    def test_classifier_has_n_classes_after_init_modeller_context(
        self, datastructure: DataStructure, schema: BitfountSchema
    ) -> None:
        """Test that n_classes is set during initialise_model in modeller context."""
        model = PyTorchTabularClassifier(
            datastructure=datastructure, schema=schema, steps=10
        )
        assert not hasattr(model, "n_classes")
        model.initialise_model(context=ModelContext.MODELLER)
        assert model.n_classes == 2

    @unit_test
    @pytest.mark.parametrize(
        "epochs, steps, value_error",
        [
            (0, 0, True),
            (1, 10, True),
            (None, None, True),
            (None, 1, False),
            (1, None, False),
            (None, 0, False),
        ],
    )
    def test_epochs_steps_value_error_raised_correctly(
        self,
        datastructure: DataStructure,
        epochs: int,
        steps: int,
        value_error: ValueError,
    ) -> None:
        """Ensure steps/epochs logic is correct in NeuralNetworkMixIn."""
        if value_error:
            with pytest.raises(ValueError):
                PyTorchTabularClassifier(
                    datastructure=datastructure,
                    schema=BitfountSchema(),
                    steps=steps,
                    epochs=epochs,
                )
        else:
            PyTorchTabularClassifier(
                datastructure=datastructure,
                schema=BitfountSchema(),
                steps=steps,
                epochs=epochs,
            )

    @unit_test
    @pytest.mark.parametrize("steps", [5, 100])
    def test_stepwise_fit_remembers_batch_number_after_reset(
        self, datasource: DataSource, datastructure: DataStructure, steps: int
    ) -> None:
        """Tests that the model remembers the batch number in between `fit` calls.

        This allows us to call `fit` multiple times on the same model without training
        on the same batches as before.
        """

        class _PyTorchTabularClassifier(PyTorchTabularClassifier):
            batch_indices_trained_on = []

            def on_train_batch_end(self, outputs, batch, batch_idx, dataloader_idx):  # type: ignore[no-untyped-def] # Reason: just a test method # noqa: B950
                """Hook called at the end of each batch training.

                Implementing this allows us to keep track of batches that were actually
                trained on. If `outputs` is empty, then the batch was skipped.
                """
                if outputs:
                    self.batch_indices_trained_on.append(batch_idx)

        model = _PyTorchTabularClassifier(
            datastructure=datastructure,
            schema=BitfountSchema(),
            steps=steps,
            batch_size=32,
        )
        model.fit(datasource)
        # index starts from 0
        assert model._pl_trainer.batch_idx == steps - 1  # type: ignore[attr-defined] # Reason: mypy can't detect attribute # noqa: B950
        assert model._total_num_batches_trained == steps

        model.reset_trainer()
        model.fit(datasource)
        # We take the modulo of batches in an epoch to ensure the calculation works
        # even if the number of batches goes past how many there are in an epoch
        assert (
            model._pl_trainer.batch_idx  # type: ignore[attr-defined] # Reason: mypy can't detect attribute # noqa: B950
            == (((steps * 2) - 1) % len(model.train_dl))  # index starts from 0
        )
        assert model._total_num_batches_trained == steps * 2

        # The batch indices trained on should go up sequentially and smoothly indicating
        # that the batches are going in order and that no batches are skipped/repeated
        assert model.batch_indices_trained_on == [
            i % len(model.train_dl) for i in range(steps * 2)
        ]

    @integration_test
    def test_transfer_learning(self) -> None:
        """Tests transfer learning works."""
        datastructure, datasource = get_datastructure_and_datasource(
            classification=True, loss_weights=True
        )
        lr = 0.01
        neural_network = PyTorchTabularClassifier(
            datastructure=datastructure,
            schema=BitfountSchema(),
            epochs=1,
            batch_size=32,
            lr=lr,
        )
        neural_network.fit(datasource)
        # divide learning rate by 10
        neural_network._opt_func = partial(neural_network._opt_func, lr=lr * 0.1)
        neural_network.fit(datasource)  # fine tune pre-trained model
        assert_results(model=neural_network)

    @integration_test
    def test_multitask_transfer_learning(self) -> None:
        """Tests multitask training works."""
        lr = 0.01
        datastructure, datasource = get_datastructure_and_datasource(
            classification=True,
            multihead=True,
            multihead_size=2,
            loss_weights=True,
        )
        neural_network = PyTorchTabularClassifier(
            datastructure=datastructure,
            schema=BitfountSchema(),
            epochs=1,
            batch_size=32,
            optimizer_func=torch.optim.AdamW,
            optimizer_params={"lr": lr},
        )

        neural_network.fit(datasource)
        # divide learning rate by 10
        neural_network._opt_func = partial(neural_network._opt_func, lr=lr * 0.1)
        neural_network.fit(datasource)  # fine tune pre-trained model
        assert_results(model=neural_network)

    @integration_test
    def test_classification(
        self, datasource: DataSource, datastructure: DataStructure
    ) -> None:
        """Tests Tabular classification.

        Test PyTorchTabularClassifier fit() and get_results() methods for a
        classification problem using Adam optimizer.
        """
        neural_network = PyTorchTabularClassifier(
            datastructure=datastructure,
            schema=BitfountSchema(),
            epochs=1,
            batch_size=16,
        )
        neural_network.fit(datasource)
        assert_results(model=neural_network)

    @unit_test
    def test_specify_n_classes(
        self,
        datasource: DataSource,
    ) -> None:
        """Tests specifying number of classes explicitly works.

        Tests the functionality where n_classes can be specified
        when initialising the classifier model. Required for running
        prediction, where the dataset doesn't contain a target.
        """
        inference_datasource = DataSource(datasource.data, ignore_cols=["TARGET"])
        inference_datastructure = DataStructure()
        inference_network = PyTorchTabularClassifier(
            datastructure=inference_datastructure,
            schema=BitfountSchema(inference_datasource),
            epochs=1,
            n_classes=5,
        )
        assert inference_network.n_classes == 5

    @unit_test
    def test_init_datastructure_no_target(
        self,
        datasource: DataSource,
    ) -> None:
        """Tests DataStructure with no target.

        Test that a DataStructure can be initialised without specifying
        a target, as this is an optional argument now, and needs to be
        for unsupervised datasets.
        """
        inference_datastructure = DataStructure()
        assert inference_datastructure is not None
        assert inference_datastructure.target is None

    @unit_test
    def test_set_number_of_classes(
        self, datasource: DataSource, datastructure: DataStructure
    ) -> None:
        """Tests that n_classes override works."""
        inference_datasource = DataSource(datasource.data, ignore_cols=["TARGET"])
        inference_datastructure = DataStructure()
        inference_datastructure.target = None
        inference_network = PyTorchTabularClassifier(
            datastructure=inference_datastructure,
            schema=BitfountSchema(inference_datasource),
            epochs=1,
            n_classes=2,
        )
        inference_network.set_number_of_classes()

    @unit_test
    def test_no_classes_raises_error(
        self,
        datasource: DataSource,
        datastructure: DataStructure,
        tmp_path: py.path.local,
    ) -> None:
        """Ensures error raised if unknown number of classes.

        Tests that error is raised when both no target is specified in data,
        and no n_classes is explicitly defined.
        """
        inference_datasource = DataSource(datasource.data, ignore_cols=["TARGET"])
        inference_datastructure = DataStructure()
        inference_network = PyTorchTabularClassifier(
            datastructure=inference_datastructure,
            schema=BitfountSchema(inference_datasource),
            epochs=1,
        )
        with pytest.raises(ValueError):
            inference_network.initialise_model()

    @unit_test
    def test_prediction(
        self, datasource: DataSource, datastructure: DataStructure
    ) -> None:
        """Test that prediction works with trained model."""
        model = PyTorchTabularClassifier(
            datastructure=datastructure, schema=BitfountSchema(), steps=10
        )
        model.fit(datasource)
        model.predict(datasource)

    @unit_test
    def test_prediction_empty_testset(
        self, datasource: DataSource, datastructure: DataStructure
    ) -> None:
        """Test that prediction fails if no test data is provided."""
        model = PyTorchTabularClassifier(
            datastructure=datastructure, schema=BitfountSchema(), steps=10
        )
        model.fit(datasource)
        empty_datasource = DataSource(datasource.data, PercentageSplitter(0, 0))
        with pytest.raises(ValueError):
            model.predict(empty_datasource)

    @integration_test
    def test_prediction_after_train(
        self,
        datasource: DataSource,
        datastructure: DataStructure,
        tmp_path: py.path.local,
    ) -> None:
        """Tests Tabular classification.

        Test PyTorchTabularClassifier fit() and predict() methods for a
        classification problem.
        """
        datastructure = DataStructure(target="TARGET")

        training_network = PyTorchTabularClassifier(
            datastructure=datastructure,
            schema=BitfountSchema(datasource, force_stype={"categorical": ["TARGET"]}),
            epochs=1,
            batch_size=16,
        )
        training_network.fit(datasource)

        training_network.serialize(tmp_path / SERIALIZED_MODEL_NAME)
        assert os.path.exists(tmp_path / SERIALIZED_MODEL_NAME)

        inference_datasource = DataSource(datasource.data, ignore_cols=["TARGET"])
        inference_datastructure = DataStructure()
        inference_network = PyTorchTabularClassifier(
            datastructure=inference_datastructure,
            schema=BitfountSchema(inference_datasource),
            epochs=1,
            n_classes=2,
        )
        inference_network.deserialize(tmp_path / SERIALIZED_MODEL_NAME)
        assert inference_network._initialised
        preds = inference_network.predict(inference_datasource)
        assert preds is not None
        assert len(preds) == len(inference_datasource.test_set)
        assert inference_network.n_classes == preds[0].shape[0]

    @unit_test
    def test_classification_with_continuous_data_only(
        self, datasource: DataSource, datastructure: DataStructure
    ) -> None:
        """Tests calling fit() with continuous only features."""
        datastructure = DataStructure(
            target="TARGET", selected_cols=["A", "B", "C", "D", "TARGET"]
        )
        neural_network = PyTorchTabularClassifier(
            datastructure=datastructure,
            schema=BitfountSchema(),
            steps=1,
            optimizer=Optimizer("Adam"),
            batch_size=32,
        )
        neural_network.fit(datasource)

    @integration_test
    def test_fit_eval_with_continuous_data_only(
        self, datasource: DataSource, datastructure: DataStructure
    ) -> None:
        """Tests calling fit& eval with continuous only features."""
        datastructure = DataStructure(
            target="TARGET", selected_cols=["A", "B", "C", "D", "TARGET"]
        )
        neural_network = PyTorchTabularClassifier(
            datastructure=datastructure,
            schema=BitfountSchema(),
            steps=1,
            optimizer=Optimizer("Adam"),
            batch_size=32,
        )
        neural_network.fit(datasource)
        assert_results(neural_network)

    @unit_test
    def test_classification_with_categorical_data_only(
        self, datasource: DataSource, datastructure: DataStructure
    ) -> None:
        """Tests calling fit() with categorical only features."""
        force_stype = {"categorical": ["E", "F", "G", "H"]}
        datastructure = DataStructure(
            target="TARGET",
            selected_cols=["E", "F", "G", "H", "M", "N", "O", "P", "TARGET"],
        )
        datastructure._force_stype = cast(
            MutableMapping[_SemanticTypeValue, List[str]], force_stype
        )
        neural_network = PyTorchTabularClassifier(
            datastructure=datastructure,
            schema=BitfountSchema(),
            steps=1,
            optimizer=Optimizer("Adam"),
            batch_size=32,
        )
        neural_network._add_datasource_to_schema(
            datasource,
        )
        neural_network.fit(datasource)

    @integration_test
    def test_classification_no_optimizer_params(
        self, datasource: DataSource, datastructure: DataStructure
    ) -> None:
        """Confirms that optimizer works without params provided."""
        model = PyTorchTabularClassifier(
            datastructure=datastructure,
            schema=BitfountSchema(),
            epochs=1,
            batch_size=16,
            optimizer=Optimizer("Adam"),
        )
        model.fit(datasource)

        model_optimizer: Optimizer = model.optimizer
        assert model_optimizer.name == "Adam"
        assert model_optimizer.params == {}

    @integration_test
    def test_classification_custom_scheduler(
        self, datasource: DataSource, datastructure: DataStructure
    ) -> None:
        """Confirms that training works with a custom scheduler."""
        epochs = 2
        batch_size = 16
        total_steps = int(len(datasource.train_idxs) * epochs / batch_size)
        model = PyTorchTabularClassifier(
            datastructure=datastructure,
            schema=BitfountSchema(),
            epochs=epochs,
            batch_size=batch_size,
            optimizer=Optimizer("Adam"),
            scheduler=Scheduler(
                "OneCycleLR", {"max_lr": 0.01, "total_steps": total_steps}
            ),
        )

        model.fit(datasource)

        model_scheduler = cast(Scheduler, model.scheduler)
        assert model_scheduler.name == "OneCycleLR"
        assert model_scheduler.params == {"max_lr": 0.01, "total_steps": total_steps}
        assert_results(model=model)

    @integration_test
    def test_classification_swa(
        self, datasource: DataSource, datastructure: DataStructure
    ) -> None:
        """Test classification with stochastic weight averaging."""
        model = PyTorchTabularClassifier(
            datastructure=datastructure,
            schema=BitfountSchema(),
            epochs=1,
            batch_size=16,
            optimizer=Optimizer("Adam"),
            swa=True,
        )

        model.fit(datasource)
        assert_results(model=model)

    @integration_test
    def test_classification_lamb_optimizer(
        self, datasource: DataSource, datastructure: DataStructure
    ) -> None:
        """Tests classification with a different optimizer."""
        neural_network = PyTorchTabularClassifier(
            datastructure=datastructure,
            schema=BitfountSchema(),
            epochs=1,
            batch_size=16,
            optimizer=Optimizer("Lamb", {"lr": 0.01}),
        )

        neural_network.fit(datasource)
        assert_results(model=neural_network)

    @unit_test
    def test_optimizer_not_supported(
        self, datasource: DataSource, datastructure: DataStructure
    ) -> None:
        """Tests classification with a different optimizer."""
        with pytest.raises(ValueError):
            model = PyTorchTabularClassifier(
                datastructure=datastructure,
                schema=BitfountSchema(),
                epochs=1,
                batch_size=16,
                optimizer=Optimizer("FooBar", {"lr": 0.01}),
            )

            model.fit(datasource)

    @unit_test
    def test_tabnet_passed_to_tabular_classifier_raises_error(
        self, datastructure: DataStructure
    ) -> None:
        """Ensures error is raised if tabnet model passed to tabular classifier."""
        ms = NeuralNetworkPredefinedModel("TabNet")
        with pytest.raises(ValueError):
            PyTorchTabularClassifier(
                model_structure=ms, datastructure=datastructure, epochs=2
            )

    @integration_test
    def test_multilabel_classification(self) -> None:
        """Tests multilabel classification works."""
        datastructure = create_datastructure(multilabel=True)
        datasource = create_datasource(classification=True, multilabel=True)
        neural_network = PyTorchTabularClassifier(
            datastructure=datastructure,
            schema=BitfountSchema(),
            epochs=1,
            batch_size=16,
            multilabel=True,
        )
        neural_network.fit(datasource)
        assert_results(model=neural_network)

    @unit_test
    def test_multilabel_has_correct_loss_funct(self) -> None:
        """Test that the correct loss function is loaded ."""
        datastructure = create_datastructure(multilabel=True)

        neural_network = PyTorchTabularClassifier(
            datastructure=datastructure,
            schema=BitfountSchema(),
            epochs=1,
            batch_size=16,
            multilabel=True,
        )
        assert issubclass(neural_network.loss_func, nn.BCEWithLogitsLoss)  # type: ignore[arg-type] # reason: mypy gives incompatible type error "Optional[Callable[..., Any]]"; expected "type" # noqa: B950

    @integration_test
    def test_multilabel_multitask_classification(self) -> None:
        """Tests multilabel multitask classification works."""
        datastructure, datasource = get_datastructure_and_datasource(
            classification=True,
            multilabel=True,
            multihead=True,
            multihead_size=2,
            loss_weights=True,
        )
        neural_network = PyTorchTabularClassifier(
            datastructure=datastructure,
            schema=BitfountSchema(),
            epochs=1,
            batch_size=16,
            multilabel=True,
        )
        neural_network.fit(datasource)
        assert_results(model=neural_network)

    @unit_test
    def test_serialization_deserialization_before_fitting(
        self,
        datasource: DataSource,
        datastructure: DataStructure,
        tmp_path: py.path.local,
    ) -> None:
        """Tests serialize() and deserialize() method before fitting."""
        neural_network = PyTorchTabularClassifier(
            datastructure=datastructure,
            schema=BitfountSchema(datasource, force_stype={"categorical": ["TARGET"]}),
            epochs=1,
            batch_size=16,
        )
        neural_network.serialize(tmp_path / SERIALIZED_MODEL_NAME)
        assert os.path.exists(tmp_path / SERIALIZED_MODEL_NAME)

        model = PyTorchTabularClassifier(
            datastructure=datastructure,
            schema=BitfountSchema(datasource, force_stype={"categorical": ["TARGET"]}),
            epochs=2,
        )
        model.deserialize(tmp_path / SERIALIZED_MODEL_NAME)
        assert model._initialised

    @unit_test
    def test_serialization_deserialization_after_fitting(
        self,
        datasource: DataSource,
        datastructure: DataStructure,
        tmp_path: py.path.local,
    ) -> None:
        """Tests serialize() and deserialize() methods after fitting."""
        neural_network = PyTorchTabularClassifier(
            datastructure=datastructure,
            schema=BitfountSchema(),
            epochs=1,
            batch_size=16,
        )

        neural_network.fit(datasource)
        neural_network.serialize(tmp_path / SERIALIZED_MODEL_NAME)
        assert os.path.exists(tmp_path / SERIALIZED_MODEL_NAME)
        neural_network = PyTorchTabularClassifier(
            datastructure=datastructure, schema=BitfountSchema(), epochs=2
        )
        neural_network.fit(datasource)
        neural_network.deserialize(tmp_path / SERIALIZED_MODEL_NAME)
        neural_network.evaluate(neural_network.test_dl)

    @unit_test
    def test_tabular_invalid_model_structure(
        self, datastructure: DataStructure
    ) -> None:
        """Tests error raised on invalid tabular model structure."""
        with pytest.raises(ValueError):
            PyTorchTabularClassifier(
                model_structure=NeuralNetworkPredefinedModel("resnet18"),
                datastructure=datastructure,
                epochs=1,
                batch_size=16,
            )

    @unit_test
    def test_image_invalid_model_structure(self, datastructure: DataStructure) -> None:
        """Tests error raised on invalid image model structure."""
        with pytest.raises(ValueError):
            PyTorchImageClassifier(
                model_structure=FeedForwardModelStructure(),
                datastructure=datastructure,
                epochs=1,
                batch_size=16,
            )

    @unit_test
    def test_tabular_classifier_split_dataloader_output(self) -> None:
        """Tests tabular classifier split dataloader output."""
        data = torch.stack((torch.ones(8), torch.ones(8), torch.ones(8)), dim=1)
        datasource = DataSource(pd.DataFrame(data, columns=["A", "B", "TARGET"]))
        datastructure = DataStructure(target=["TARGET"])
        datastructure._force_stype = {
            "categorical": ["TARGET", "A"],
            "continuous": ["B"],
        }
        model = PyTorchTabularClassifier(
            datastructure=datastructure,
            schema=BitfountSchema(),
            epochs=2,
        )
        # Need to call the below to initialize the dataloaders
        model.initialise_model(datasource)
        test_data = (
            torch.stack((torch.ones(8), torch.ones(8)), dim=1),
            torch.stack((torch.ones(8), torch.ones(8)), dim=1),
        )
        split_data = model._split_dataloader_output(test_data)
        assert len(split_data) == 3
        assert split_data[0][0].float().mean() == 1.0
        assert split_data[0][1].float().mean() == 1.0
        assert split_data[1].mean() == 1.0
        assert split_data[2] is None

    @unit_test
    def test_image_classifier_split_dataloader_output_categories(
        self, datasource: DataSource, datastructure: DataStructure
    ) -> None:
        """Tests image classifier dataloader splitting with categories."""
        model = PyTorchImageClassifier(
            datastructure=datastructure,
            schema=BitfountSchema(),
            model_structure=NeuralNetworkPredefinedModel("resnet18"),
            epochs=2,
        )

        # Need to call the below to initialize the dataloaders
        model.initialise_model(datasource)

        data = (
            torch.ones(8),
            torch.stack((torch.ones(8), torch.zeros(8), torch.ones(8)), dim=1),
        )
        split_data = model._split_dataloader_output(data)
        assert len(split_data) == 3
        assert cast(torch.Tensor, split_data[0]).mean() == 1.0
        assert split_data[1].mean() == 1.0
        assert cast(torch.Tensor, split_data[2]).sum() == 8

    @unit_test
    def test_image_classifier_create_model_cnn_model_structure(self) -> None:
        """Tests image classifier creation with CNN structure."""
        data = create_dataset(image=True)
        ds = DataSource(data)
        datastructure = DataStructure(
            target="TARGET", selected_cols=["image", "TARGET"], image_cols=["image"]
        )
        model_structure = CNNModelStructure(pooling_function="avg")
        model = PyTorchImageClassifier(
            datastructure=datastructure,
            schema=BitfountSchema(),
            model_structure=model_structure,
            epochs=2,
        )
        # Need to call the below to initialize the dataloaders
        model.initialise_model(ds)
        torch_model = model._create_model()
        assert isinstance(torch_model, torch.nn.Module)
        assert isinstance(
            cast(nn.ModuleList, torch_model.pooling_functions)[0], torch.nn.AvgPool2d
        )

    @unit_test
    def test_image_classifier_create_model_predefined_structure(self) -> None:
        """Tests image classifier creation with predefined structure."""
        data = create_dataset(image=True)
        ds = DataSource(data, image_col=["image"])
        datastructure = DataStructure(
            target="TARGET", selected_cols=["image", "TARGET"]
        )
        model = PyTorchImageClassifier(
            datastructure=datastructure,
            schema=BitfountSchema(),
            model_structure=NeuralNetworkPredefinedModel("resnet18"),
            epochs=2,
        )

        model.initialise_model(ds)
        torch_model = model._create_model()
        assert isinstance(torch_model, torch.nn.Module)
        assert cast(nn.Linear, torch_model.fc).out_features == 2

    @unit_test
    def test_image_classifier_multilabel_loss(self) -> None:
        """Tests image classifier with multilabel loss function."""
        datastructure = DataStructure(
            target="TARGET", selected_cols=["image", "TARGET"]
        )
        model = PyTorchImageClassifier(
            datastructure=datastructure,
            schema=BitfountSchema(),
            model_structure=NeuralNetworkPredefinedModel("resnet18"),
            epochs=2,
            multilabel=True,
        )
        assert model.loss_func == torch.nn.BCEWithLogitsLoss

    @unit_test
    def test_image_classifier_loss_func_not_recognised(self) -> None:
        """Tests error raised if unknown loss_func supplied."""
        datastructure = DataStructure(
            target="TARGET", selected_cols=["image", "TARGET"]
        )
        with pytest.raises(ValueError):
            PyTorchImageClassifier(
                datastructure=datastructure,
                schema=BitfountSchema(),
                model_structure=NeuralNetworkPredefinedModel("resnet18"),
                custom_loss_func="test",
                epochs=2,
            )

    @integration_test
    def test_image_classifier_run_training(self) -> None:
        """Tests training of image classifier."""
        data = create_dataset(image=True)
        data = data[:500]
        ds = DataSource(data)
        datastructure = DataStructure(
            target="TARGET", selected_cols=["image", "TARGET"], image_cols=["image"]
        )
        model_structure = CNNModelStructure(
            layers=[16, 32], ff_layers=[500], ff_dropout_probs=[0.1]
        )
        model = PyTorchImageClassifier(
            datastructure=datastructure,
            schema=BitfountSchema(),
            epochs=3,
            model_structure=model_structure,
            batch_size=64,
            optimizer=Optimizer("RAdam", {"lr": 0.01}),
        )
        model.fit(ds)
        assert_results(model=model)

    @integration_test
    def test_image_classifier_run_training_with_custom_transformations(self) -> None:
        """Tests training of image classifier."""
        data = create_dataset(image=True)
        data = data[:500]
        ds = DataSource(data)
        datastructure = DataStructure(
            target="TARGET",
            selected_cols=["image", "TARGET"],
            image_cols=["image"],
            batch_transforms=[
                {
                    "image": {
                        "step": "train",
                        "output": True,
                        "arg": "image",
                        "transformations": [
                            {"Resize": {"height": 224, "width": 224}},
                            "Normalize",
                            "HorizontalFlip",
                            "ToTensorV2",
                        ],
                    }
                },
                {
                    "image": {
                        "step": "validation",
                        "output": True,
                        "arg": "image",
                        "transformations": [
                            {"Resize": {"height": 224, "width": 224}},
                            "Normalize",
                            "ToTensorV2",
                        ],
                    }
                },
            ],
        )
        model_structure = CNNModelStructure(
            layers=[16, 32], ff_layers=[500], ff_dropout_probs=[0.1]
        )
        model = PyTorchImageClassifier(
            datastructure=datastructure,
            schema=BitfountSchema(),
            epochs=3,
            model_structure=model_structure,
            batch_size=64,
            optimizer=Optimizer("RAdam", {"lr": 0.01}),
        )
        model.fit(ds)
        assert_results(model=model)

    @unit_test
    def test_image_classifier_fit_multiple_images(self) -> None:
        """Tests that the image classifier works with multiple images per row."""
        data = create_dataset(classification=True, multiimage=True, img_size=2)
        datasource = DataSource(data[:64])
        datastructure = DataStructure(
            target="TARGET",
            selected_cols=["image1", "image2", "TARGET"],
            image_cols=["image1", "image2"],
        )
        model = PyTorchImageClassifier(
            datastructure=datastructure,
            schema=BitfountSchema(),
            epochs=1,
        )
        model.fit(datasource)

    @unit_test
    def test_classification_with_custom_metrics(
        self, datasource: DataSource, datastructure: DataStructure
    ) -> None:
        """Tests calling fit() with different metrics."""
        neural_network = PyTorchTabularClassifier(
            datastructure=datastructure,
            schema=BitfountSchema(),
            steps=1,
            optimizer=Optimizer("Adam"),
            batch_size=32,
        )
        metrics: Dict[str, str]
        metric_results = neural_network.fit(
            datasource,
            metrics={
                "AUC": ClassificationMetric(
                    partial(roc_auc_score, multi_class="ovr", average="macro"), True
                )
            },
        )
        assert "AUC" in cast(Dict[str, str], metric_results).keys()
        assert "validation_loss" in cast(Dict[str, str], metric_results).keys()
        assert len(cast(Dict[str, str], metric_results)) == 2

    @unit_test
    def test_tensorboard_logger_default(self, datastructure: DataStructure) -> None:
        """Tests that the default lightning logger is TensorBoard."""
        model = PyTorchTabularClassifier(
            datastructure=datastructure, schema=BitfountSchema(), steps=10
        )

        assert isinstance(model._pl_logger, TensorBoardLogger)

    @unit_test
    def test_csv_logger(
        self, datastructure: DataStructure, tmpdir: py.path.local
    ) -> None:
        """Tests that CSVLogger works."""
        model = PyTorchTabularClassifier(
            datastructure=datastructure,
            schema=BitfountSchema(),
            steps=10,
            logger_config=LoggerConfig(
                name="CSVLogger", save_dir=cast(Path, tmpdir.strpath)
            ),
        )
        assert isinstance(model._pl_logger, CSVLogger)

    @unit_test
    def test_mlflow_logger(
        self, datastructure: DataStructure, tmpdir: py.path.local
    ) -> None:
        """Tests that MLFlowLogger works."""
        model = PyTorchTabularClassifier(
            datastructure=datastructure,
            schema=BitfountSchema(),
            steps=10,
            logger_config=LoggerConfig(
                name="MLFlow", save_dir=cast(Path, tmpdir.strpath)
            ),
        )
        assert isinstance(model._pl_logger, MLFlowLogger)

    @unit_test
    def test_neptune_logger(
        self, datastructure: DataStructure, tmpdir: py.path.local
    ) -> None:
        """Tests that NeptuneLogger works."""
        model = PyTorchTabularClassifier(
            datastructure=datastructure,
            schema=BitfountSchema(),
            steps=10,
            logger_config=LoggerConfig(name="Neptune"),
        )
        assert isinstance(model._pl_logger, NeptuneLogger)

    @unit_test
    def test_testtube_logger(
        self, datastructure: DataStructure, tmpdir: py.path.local
    ) -> None:
        """Tests that TestTubeLogger works."""
        model = PyTorchTabularClassifier(
            datastructure=datastructure,
            schema=BitfountSchema(),
            steps=10,
            logger_config=LoggerConfig(
                name="TestTube", save_dir=cast(Path, tmpdir.strpath)
            ),
        )
        assert isinstance(model._pl_logger, TestTubeLogger)

    @unit_test
    def test_wandb_logger(
        self, datastructure: DataStructure, tmpdir: py.path.local
    ) -> None:
        """Tests that WandbLogger works."""
        model = PyTorchTabularClassifier(
            datastructure=datastructure,
            schema=BitfountSchema(),
            steps=10,
            logger_config=LoggerConfig(
                name="WeightsAndBiases",
                save_dir=cast(Path, tmpdir.strpath),
                params={"offline": True},
            ),
        )
        assert isinstance(model._pl_logger, WandbLogger)

    @unit_test
    def test__fit_federated(
        self,
        datastructure: DataStructure,
        mock_bitfount_session: Mock,
        mocker: MockerFixture,
    ) -> None:
        """Tests private _fit_federated method.

        Checks that DistributedModelMixIn._fit_federated is helper method creates
        correct instances and runs the modeller correctly.
        """
        # Create model to test
        model = PyTorchTabularClassifier(
            datastructure=datastructure,
            schema=BitfountSchema(),
            epochs=1,
            batch_size=16,
        )

        # Patch out the modeller's run method as we only care how it is called
        # from _fit_federated.

        mock_modeller_run_method = mocker.patch.object(Modeller, "run")

        # Run method
        pod_identifiers = ["bitfount/prosper", "bitfount/prosper2"]
        model._fit_federated(
            pod_identifiers=pod_identifiers,
            private_key_or_file=TEST_SECURITY_FILES / "test_private.testkey",
        )

        # Check run method was called correctly
        # TODO: [BIT-983] Should this check that the Modeller was instantiated
        #       correctly? Related to whether we should mock out the helper calls.
        mock_modeller_run_method.assert_called_once_with(pod_identifiers)

    @unit_test
    def test_fit_method_with_federated_arguments(
        self, datastructure: DataStructure, mocker: MockerFixture
    ) -> None:
        """Test fit method with federated arguments detected correctly."""
        mock_fit_federated_method = mocker.patch(
            "bitfount.federated.mixins._DistributedModelMixIn._fit_federated",
        )
        model = PyTorchTabularClassifier(
            datastructure=datastructure,
            schema=BitfountSchema(),
            epochs=1,
            batch_size=16,
        )
        pod_identifiers = ["bitfount/prosper", "bitfount/prosper2"]
        private_key_or_file = TEST_SECURITY_FILES / "test_private.testkey"
        model.fit(
            pod_identifiers=pod_identifiers,
            private_key_or_file=private_key_or_file,
        )
        mock_fit_federated_method.assert_called_once_with(
            pod_identifiers=pod_identifiers, private_key_or_file=private_key_or_file
        )


@backend_test
@unit_test
class TestMarshmallowSerialization:
    """Test Marshmallow Serialization for PyTorch models."""

    def test_pytorch_classifier_serialization(
        self, datastructure: DataStructure
    ) -> None:
        """Tests tabular classifier serialization."""
        model = PyTorchTabularClassifier(
            datastructure=datastructure, schema=BitfountSchema(), epochs=2
        )
        schema = model.get_schema()

        serialized_model = schema().dump(model)
        deserialized_model = schema().load(serialized_model)
        assert_vars_equal(vars(model), vars(deserialized_model))

    def test_image_classifier_serialization(self, datastructure: DataStructure) -> None:
        """Test PyTorchImageClassifier serialization."""
        model = PyTorchImageClassifier(
            model_structure=NeuralNetworkPredefinedModel("resnet18"),
            datastructure=datastructure,
            schema=BitfountSchema(),
            epochs=1,
            batch_size=16,
        )

        schema = model.get_schema()
        serialized_model = schema().dump(model)
        deserialized_model = schema().load(serialized_model)
        assert_vars_equal(vars(model), vars(deserialized_model))

    def test_tabnet_serialization(self, datastructure: DataStructure) -> None:
        """Test TabNet serialization."""
        ms = NeuralNetworkPredefinedModel("TabNet")
        model = TabNetClassifier(
            model_structure=ms,
            datastructure=datastructure,
            schema=BitfountSchema(),
            balance_class_weights=True,
            epochs=2,
        )
        schema = model.get_schema()
        serialized_model = schema().dump(model)
        deserialized_model = schema().load(serialized_model)
        assert_vars_equal(vars(model), vars(deserialized_model))


@backend_test
class TestTabNetClassifier:
    """Tests for TabNetClassifier."""

    @integration_test
    def test_training_default_optimizer(
        self, datasource: DataSource, datastructure: DataStructure
    ) -> None:
        """Test training with default optimizer."""
        ms = NeuralNetworkPredefinedModel("TabNet")
        model = TabNetClassifier(
            model_structure=ms,
            datastructure=datastructure,
            schema=BitfountSchema(),
            epochs=6,
            patience=4,
            batch_size=64,
            virtual_batch_size=16,
            seed=43,
        )
        model.fit(datasource)
        preds, targs = model.evaluate()
        metrics = MetricCollection.create_from_model(model)
        results = metrics.compute(targs, preds)
        assert isinstance(results, dict)
        assert len(metrics.metrics) == len(BINARY_CLASSIFICATION_METRICS)
        assert results["AUC"] > AUC_THRESHOLD

    @unit_test
    def test_virtual_batch_size_higher_than_batch_size_raises_value_error(
        self, datastructure: DataStructure
    ) -> None:
        """Test virtual batch size higher than batch size raises value error."""
        ms = NeuralNetworkPredefinedModel("TabNet")

        with pytest.raises(ValueError):
            TabNetClassifier(
                model_structure=ms,
                datastructure=datastructure,
                schema=BitfountSchema(),
                epochs=5,
                batch_size=32,
                virtual_batch_size=64,
            )

    @unit_test
    def test_virtual_batch_same_as_batch_size_is_accepted(
        self, datastructure: DataStructure
    ) -> None:
        """Test virtual batch size same as batch size accepted."""
        ms = NeuralNetworkPredefinedModel("TabNet")

        TabNetClassifier(
            model_structure=ms,
            datastructure=datastructure,
            schema=BitfountSchema(),
            epochs=5,
            batch_size=32,
            virtual_batch_size=32,
        )

    # TODO: [BIT-507] This test is intermittently failing on GHA
    @integration_test
    @pytest.mark.skip()
    def test_training_adabelief_optimizer(
        self, datasource: DataSource, datastructure: DataStructure
    ) -> None:
        """Test training defaults."""
        ms = NeuralNetworkPredefinedModel("TabNet")
        model = TabNetClassifier(
            model_structure=ms,
            datastructure=datastructure,
            schema=BitfountSchema(),
            epochs=3,
            batch_size=64,
            virtual_batch_size=16,
            optimizer=Optimizer("AdaBelief", {"lr": 0.01}),
            seed=43,
        )
        model.fit(datasource, metrics={"auc": roc_auc_score})
        preds, targs = model.evaluate()
        metrics = MetricCollection.create_from_model(model)
        results = metrics.compute(targs, preds)
        assert isinstance(results, dict)
        assert len(metrics.metrics) == len(BINARY_CLASSIFICATION_METRICS)
        assert results["AUC"] > AUC_THRESHOLD

    @unit_test
    def test_serialization_before_fitting(
        self,
        datasource: DataSource,
        datastructure: DataStructure,
        tmp_path: py.path.local,
    ) -> None:
        """Test untrained model cannot be serialized.

        TODO: [BIT-1152] change this test once serialization/deserialization of unfitted
        model if fixed.
        """
        ms = NeuralNetworkPredefinedModel("TabNet")
        model = TabNetClassifier(
            model_structure=ms,
            datastructure=datastructure,
            schema=BitfountSchema(datasource, force_stype={"categorical": ["TARGET"]}),
            epochs=1,
        )
        model.serialize(tmp_path / SERIALIZED_MODEL_NAME)
        # TODO: [BIT-1152] change this assertion
        assert not os.path.exists(tmp_path / SERIALIZED_MODEL_NAME)

    @unit_test
    def test_deserialization_before_fitting(
        self,
        datasource: DataSource,
        datastructure: DataStructure,
        tmp_path: py.path.local,
    ) -> None:
        """Test untrained model cannot be deserialized.

        TODO: [BIT-1152] change this test once serialization/deserialization of unfitted
        model if fixed.
        """
        ms = NeuralNetworkPredefinedModel("TabNet")

        model = TabNetClassifier(
            model_structure=ms,
            datastructure=datastructure,
            schema=BitfountSchema(),
            epochs=1,
        )
        model.fit(datasource)
        model.serialize(tmp_path / SERIALIZED_MODEL_NAME)
        assert os.path.exists(tmp_path / SERIALIZED_MODEL_NAME)

        model2 = TabNetClassifier(
            model_structure=ms,
            datastructure=datastructure,
            schema=BitfountSchema(datasource, force_stype={"categorical": ["TARGET"]}),
            epochs=1,
        )
        model2.deserialize(tmp_path / SERIALIZED_MODEL_NAME)
        # TODO: [BIT-1152] change this assertion
        assert not model2._initialised

    @unit_test
    def test_serialization_deserialization_after_fitting(
        self,
        datasource: DataSource,
        datastructure: DataStructure,
        tmp_path: py.path.local,
    ) -> None:
        """Test trained model works after being serialized and deserialized."""
        ms = NeuralNetworkPredefinedModel("TabNet")
        model = TabNetClassifier(
            model_structure=ms,
            datastructure=datastructure,
            schema=BitfountSchema(),
            epochs=1,
        )
        model.fit(datasource)
        model.serialize(tmp_path / SERIALIZED_MODEL_NAME)
        assert os.path.exists(tmp_path / SERIALIZED_MODEL_NAME)
        model = TabNetClassifier(
            model_structure=ms,
            datastructure=datastructure,
            schema=BitfountSchema(),
            epochs=2,
        )
        model.fit(datasource)
        model.deserialize(tmp_path / SERIALIZED_MODEL_NAME)
        model.evaluate()

    @unit_test
    def test_model_structure_not_provided(self, datastructure: DataStructure) -> None:
        """Test model structure not provided raises TypeError."""
        with pytest.raises(TypeError):
            TabNetClassifier(datastructure=datastructure, epochs=2)

    @unit_test
    def test_steps_not_accepted(self, datastructure: DataStructure) -> None:
        """Test steps not accepted for iterations."""
        ms = NeuralNetworkPredefinedModel("TabNet")
        with pytest.raises(ValueError):
            TabNetClassifier(
                datastructure=datastructure,
                schema=BitfountSchema(),
                model_structure=ms,
                steps=2,
            )

    @unit_test
    def test_incorrect_model_structure_provided(
        self, datastructure: DataStructure
    ) -> None:
        """Test incorrect model structure provided raises ValueError."""
        ms = NeuralNetworkPredefinedModel("NotTabNetModel")
        with pytest.raises(ValueError):
            TabNetClassifier(
                model_structure=ms,
                datastructure=datastructure,
                schema=BitfountSchema(),
                epochs=2,
            )

    @integration_test
    def test_multiclass_classification(self) -> None:
        """Test Multiclass classification."""
        dataset = create_dataset()
        dataset.TARGET = np.where(
            (dataset.TARGET == 0) & (dataset.C > 800), 2, dataset.TARGET
        )
        datasource = DataSource(dataset)
        datastructure = DataStructure(target="TARGET")
        ms = NeuralNetworkPredefinedModel("TabNet")
        model = TabNetClassifier(
            model_structure=ms,
            datastructure=datastructure,
            schema=BitfountSchema(),
            epochs=2,
            batch_size=16,
            virtual_batch_size=4,
            optimizer=Optimizer("RAdam"),
        )
        model.fit(datasource)
        preds, targs = model.evaluate()
        metrics = MetricCollection.create_from_model(model)
        results = metrics.compute(targs, preds)
        assert isinstance(results, dict)
        assert len(metrics.metrics) == len(MULTICLASS_CLASSIFICATION_METRICS)


# TODO: [BIT-508] Remove skip marker
@pytest.mark.skip(reason="Awaiting bugfix for opacus/lightning interaction.")
@backend_test
@unit_test
class TestDifferentialPrivacy:
    """Tests related to differential privacy in PyTorch models."""

    class DPTestModel(PyTorchTabularClassifier):
        """A custom classifier to make DP testing easier."""

        def _create_model(self) -> torch.nn.Module:  # type: ignore[override] # reason: incompatible return types # noqa: B950
            class Model(torch.nn.Module):
                """A simplistic model for DP tests.

                Ensures DP compatible layers.
                """

                def __init__(self, input_size: int, output_size: int):
                    super().__init__()
                    self.linear = Linear(input_size, 10)
                    self.relu = ReLU()
                    self.output = Linear(10, output_size)

                def forward(self, x: Any) -> Any:
                    _x_cat, x_cont = x
                    fwd = self.linear(x_cont)
                    fwd = self.relu(fwd)
                    fwd = self.output(fwd)
                    return fwd

            num_continuous = len(self._databunch.continuous_features)
            output_size = 10
            return Model(num_continuous, output_size)

    def test_differential_privacy_output(
        self, datasource: DataSource, datastructure: DataStructure
    ) -> None:
        """Tests custom tabular classifier differential privacy."""
        neural_network = TestDifferentialPrivacy.DPTestModel(
            datastructure=datastructure,
            schema=BitfountSchema(),
            epochs=1,
            batch_size=32,
            dp_config=DPModellerConfig(max_epsilon=10.0),
        )
        results = cast(Dict[str, str], neural_network.fit(datasource))

        assert "epsilon" in results
        assert "alpha" in results

    def test_differential_privacy_exceeded(
        self,
        datasource: DataSource,
        datastructure: DataStructure,
        mocker: MockerFixture,
    ) -> None:
        """Tests that further training steps are not run when DP exceeded."""
        neural_network = TestDifferentialPrivacy.DPTestModel(
            datastructure=datastructure,
            schema=BitfountSchema(),
            epochs=1,
            batch_size=32,
            dp_config=DPModellerConfig(max_epsilon=-1.0),
        )

        # Ensure train_step() isn't called when max_epsilon is exceeded
        ts = mocker.patch.object(neural_network, "training_step")
        neural_network.fit(datasource)
        ts.assert_not_called()

    def test_differential_privacy_config_serialization(
        self, datastructure: DataStructure
    ) -> None:
        """Tests the DP-specific serialization aspects."""
        dp_config = DPModellerConfig(max_epsilon=10.0)
        neural_network = PyTorchTabularClassifier(
            datastructure=datastructure,
            schema=BitfountSchema(),
            epochs=1,
            batch_size=32,
            dp_config=dp_config,
        )

        # Serialization
        dumped = PyTorchTabularClassifier._Schema().dump(neural_network)
        assert "dp_config" in dumped

        # Deserialization
        loaded = PyTorchTabularClassifier._Schema().load(dumped)
        assert loaded._dp_config == neural_network._dp_config
