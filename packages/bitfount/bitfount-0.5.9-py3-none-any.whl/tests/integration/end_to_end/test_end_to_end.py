"""Tests the system end-to-end using real web calls."""
import logging
import multiprocessing
from multiprocessing import Queue
import os
from pathlib import Path
import time
from typing import cast
from unittest.mock import Mock

from _pytest.monkeypatch import MonkeyPatch

from bitfount.runners.modeller_runner import setup_modeller_from_config
from bitfount.runners.pod_runner import setup_pod_from_config
from tests.integration import CONFIG_DIR
from tests.integration.bitfount_web_interactions import (
    WebdriverBitfountSession,
    get_bitfount_session,
    grant_proactive_access,
)
from tests.integration.utils import (
    get_caplog_records,
    load_modeller_config,
    load_pod_config,
    password_from_modeller_config,
    password_from_pod_config,
    pod_start,
    run_modeller_process,
    tie_together_configs,
)
from tests.utils.helper import backend_test, end_to_end_test

logger = logging.getLogger(__name__)

# Get timeouts/sleeps from envvars if possible
POD_STARTUP_SLEEP: int = int(os.getenv("E2E_TEST_POD_STARTUP_SLEEP", default=20))
MODELLER_STARTUP_SLEEP: int = int(
    os.getenv("E2E_TEST_MODELLER_STARTUP_SLEEP", default=5)
)
MODELLER_RUN_TIMEOUT: int = int(
    os.getenv("E2E_TEST_MODELLER_RUN_TIMEOUT", default=2.5 * 60)
)


@backend_test
@end_to_end_test
class TestProsperEndToEnd:
    """End-to-end tests using the Prosper dataset."""

    async def test_prosper_e2e_results_only(
        self,
        caplog_queue: Queue,
        mock_bitfount_session: Mock,
        monkeypatch: MonkeyPatch,
        prosper_data: Path,
        tmp_path: Path,
    ) -> None:
        """Tests a full end-to-end run using Prosper dataset."""
        monkeypatch.setenv("BITFOUNT_ENVIRONMENT", "staging")
        try:
            # Load configs and tie together
            modeller_config = load_modeller_config(CONFIG_DIR / "modeller.yaml")
            modeller_pswd = password_from_modeller_config(modeller_config)
            pod_1_config = load_pod_config(CONFIG_DIR / "pod_1.yaml", prosper_data)
            pod_1_pswd = password_from_pod_config(pod_1_config)
            pod_2_config = load_pod_config(CONFIG_DIR / "pod_2.yaml", prosper_data)
            pod_2_pswd = password_from_pod_config(pod_2_config)
            tie_together_configs(modeller_config, pod_1_config, pod_2_config)
            # Mock BitfountSession
            # Override default return_value with side_effect
            # get_bitfount_session() one. side_effect takes precedence
            # over return_value.
            # If you ever change the order that the processes start in,
            # then be sure to change the order of these...
            token_dir = tmp_path / "bitfount_tokens"
            mock_bitfount_session.side_effect = [
                # pod 1 bitfount session
                get_bitfount_session(pod_1_config.username, pod_1_pswd, token_dir),
                # pod 2 bitfount session
                get_bitfount_session(pod_2_config.username, pod_2_pswd, token_dir),
                # modeller bitfount session
                get_bitfount_session(
                    modeller_config.modeller.username, modeller_pswd, token_dir
                ),
            ]
            # Load pods
            pod_1 = setup_pod_from_config(pod_1_config)
            pod_2 = setup_pod_from_config(pod_2_config)

            # Start pods
            logger.info("Spinning up pods... ")
            logger.info("Spinning up pod 1... ")
            pod_1_process = multiprocessing.Process(
                target=pod_start, name="Pod_1_Runner", args=(pod_1,)
            )
            pod_1_process.start()

            logger.info("Spinning up pod 2... ")
            pod_2_process = multiprocessing.Process(
                target=pod_start, name="Pod_2_Runner", args=(pod_2,)
            )
            pod_2_process.start()
            time.sleep(POD_STARTUP_SLEEP)  # give the pods time to spin up

            assert pod_1_process.is_alive()
            assert pod_2_process.is_alive()

            logger.info("Pods loaded.")

            # Load modeller
            # We do this after the pods have started, as we need the pods to have
            # published their public keys to the Hub.
            modeller, pod_identifiers = setup_modeller_from_config(modeller_config)
            model_out = tmp_path / "model.out"
            modeller_process = multiprocessing.Process(
                target=run_modeller_process,
                name="Modeller_Run",
                args=(modeller, pod_identifiers, model_out),
            )

            # Sort proactive access to each pod
            logger.info(f"Granting proactive access to pod {pod_1_config.pod_id}...")
            grant_proactive_access(
                modeller_username=modeller_config.modeller.username,
                pod_id=pod_1_config.pod_id,
                role="general_modeller",
                # This is a WebdriverBitfountSession as we mocked it out
                pod_session=cast(WebdriverBitfountSession, pod_1._session),
            )
            logger.info(f"Granting proactive access to pod {pod_2_config.pod_id}...")
            grant_proactive_access(
                modeller_username=modeller_config.modeller.username,
                pod_id=pod_2_config.pod_id,
                role="general_modeller",
                # This is a WebdriverBitfountSession as we mocked it out
                pod_session=cast(WebdriverBitfountSession, pod_2._session),
            )

            # Start modeller
            logger.info("Starting Modeller...")
            modeller_process.start()
            time.sleep(MODELLER_STARTUP_SLEEP)  # give modeller time to spin up
            assert not model_out.exists()  # check doesn't exist at this point

            # Join modeller, wait for output for MODELLER_RUN_TIMEOUT seconds
            modeller_process.join(MODELLER_RUN_TIMEOUT)

            # Check modeller is done, pods still going
            logger.info("Modeller should be finished by this point.")
            assert not modeller_process.is_alive()
            assert (
                modeller_process.exitcode is not None and modeller_process.exitcode <= 0
            )

            # Check no errors raised in logs
            for record in get_caplog_records(caplog_queue):
                assert "ERROR" not in record

            # Check output file exists and has nonzero size
            assert model_out.exists()
            assert os.path.getsize(model_out) > 0

            # Ensure pods are still running
            assert pod_1_process.is_alive()
            assert pod_2_process.is_alive()

            # Stop all pods
            for process in [pod_1_process, pod_2_process]:
                process.terminate()
                process.join()

            # Ensure shutdown
            assert pod_1_process.exitcode is not None and pod_1_process.exitcode <= 0
            assert pod_2_process.exitcode is not None and pod_2_process.exitcode <= 0
        finally:
            try:
                # The unbound variable issue is handled by the NameError catching below.
                # noinspection PyUnboundLocalVariable
                private_key_file: Path = cast(
                    Path, modeller_config.modeller.private_key_file
                )
                os.remove(private_key_file)
            except FileNotFoundError:
                pass
            except NameError:
                # Means the modeller_config variable didn't even get created;
                # another exception has occurred that has booted us out of the
                # `try` block before it even got to there. We pass on NameError
                # to avoid masking whatever that underlying exception was.
                pass

            # Stop all processes
            # noinspection PyBroadException
            try:
                # noinspection PyUnboundLocalVariable
                modeller_process.terminate()
            except Exception:
                pass
            # noinspection PyBroadException
            try:
                # noinspection PyUnboundLocalVariable
                pod_1_process.terminate()
            except Exception:
                pass
            # noinspection PyBroadException
            try:
                # noinspection PyUnboundLocalVariable
                pod_2_process.terminate()
            except Exception:
                pass
