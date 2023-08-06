"""Test config settings for the end-to-end tests."""
import logging
from logging import handlers
from multiprocessing import Manager
from multiprocessing.managers import SyncManager
from pathlib import Path
import queue
from typing import Generator

from _pytest.monkeypatch import MonkeyPatch
from _pytest.tmpdir import TempPathFactory
import dotenv
from pytest import fixture
import requests

import bitfount.config
from tests.integration import PRIVATE_DETAILS_ENV_FILE

logger = logging.getLogger(__name__)

TMP_DIR_BASENAME = "E2E-"
PROSPER_CSV_URL = (
    "https://bitfount-hosted-downloads.s3.eu-west-2.amazonaws.com/prosper.csv"
)


@fixture(autouse=True)
def env_fix(monkeypatch: MonkeyPatch) -> None:
    """Fix the environment into a known state for tests."""
    # Overrides the default fixture in tests/conftest.py
    monkeypatch.setenv("BITFOUNT_ENGINE", bitfount.config._PYTORCH_ENGINE)
    monkeypatch.setattr(
        "bitfount.config.BITFOUNT_ENGINE", bitfount.config._PYTORCH_ENGINE
    )


@fixture(scope="package", autouse=True)
def load_env() -> None:
    """Load the private environment variables file if it exists."""
    if PRIVATE_DETAILS_ENV_FILE.exists():
        dotenv.load_dotenv(dotenv_path=PRIVATE_DETAILS_ENV_FILE)


@fixture(scope="session")
def prosper_data(tmp_path_factory: TempPathFactory) -> Path:
    """Load the prosper data from S3."""
    logging.info("Downloading prosper data... ")
    tmp_dir = tmp_path_factory.mktemp(TMP_DIR_BASENAME)
    local_filename = tmp_dir / "prosper.csv"
    with requests.get(PROSPER_CSV_URL) as r:
        r.raise_for_status()
        with open(local_filename, "wb") as f:
            f.write(r.content)
    logging.info(f"Prosper data saved to {local_filename}")
    return local_filename


@fixture(scope="module")
def manager() -> Generator[SyncManager, None, None]:
    """Creates a multiprocessing manager.

    Returns: Manager for use in tests
    """
    yield Manager()


@fixture
def caplog_queue(manager: SyncManager) -> Generator[queue.Queue, None, None]:
    """Capture logs from other processes in a Queue and returns it."""
    logger_queue = manager.Queue()
    # We want to capture all logs, not just ours, so use root logger
    logger_for_caplog = logging.getLogger()
    logger_for_caplog.setLevel(logging.INFO)
    logger_for_caplog.addHandler(handlers.QueueHandler(logger_queue))
    yield logger_queue
