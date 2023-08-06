"""Fixtures related to environment setup, envvars, etc."""
from typing import Iterator

from _pytest.monkeypatch import MonkeyPatch
from pytest import fixture

import bitfount
from tests.utils import PytestRequest
from tests.utils.helper import DATASET_ROW_COUNT


@fixture(autouse=True)
def env_fix(monkeypatch: MonkeyPatch) -> None:
    """Fix the environment into a known state for tests."""
    # Sets the environment and engine to use the BasicDataFactory. If a specific
    # engine is needed (aka PyTorch), this must be overridden in a fixture of the
    # same name in a conftest.py file closer to the test.
    monkeypatch.setenv("BITFOUNT_ENGINE", bitfount.config._BASIC_ENGINE)
    monkeypatch.setattr(
        "bitfount.config.BITFOUNT_ENGINE", bitfount.config._BASIC_ENGINE
    )


@fixture
def environment(monkeypatch: MonkeyPatch, request: PytestRequest) -> None:
    """Sets up the BITFOUNT_ENVIRONMENT environment variable."""
    environment = request.param
    if environment:
        monkeypatch.setenv("BITFOUNT_ENVIRONMENT", environment)


@fixture(autouse=True)
def cache_clear() -> Iterator[None]:
    """Clears the cache of get_environment before and after each test."""
    bitfount.config._get_environment.cache_clear()
    yield
    bitfount.config._get_environment.cache_clear()


@fixture(autouse=True, scope="session")
def koalas_pyspark() -> None:
    """Sets pyspark and koalas config for the whole test session."""
    from pyspark import SparkConf, SparkContext

    conf = SparkConf()
    # Ensures that the host is localhost if it cannot be resolved
    conf.set("spark.driver.host", "127.0.0.1")
    # Limits memory as tests shouldn't need more than this from Spark
    conf.set("spark.executor.memory", "1g")
    # Disables the UI to speed up Spark
    conf.set("spark.ui.enabled", "false")
    # Koalas automatically uses this Spark context with the configurations set.
    SparkContext(conf=conf)

    import databricks.koalas as ks

    ks.set_option("compute.default_index_type", "sequence")
    ks.set_option("compute.max_rows", DATASET_ROW_COUNT)
