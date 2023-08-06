#!/usr/bin/env python3
"""Script to run a Pod that acts as a compute and data provider."""
from asyncio import get_event_loop
import logging
from os import PathLike
import sys
from typing import Union

import fire

from bitfount.runners.pod_runner import setup_pod_from_config_file
from bitfount.runners.utils import setup_loggers
from scripts.pod_ui_utils import Frame

try:
    # Skipping analyzing "wxasync": module is installed,
    # but missing library stubs or py.typed marker
    # This is only used for Mac but must be imported here to avoid mypy errors on
    # non-mac platforms.
    import wxasync  # type: ignore[import] # Reason: see above
except ImportError:
    pass

# Mypy error:Skipping analyzing "wx"/"wxasync" : module is
# installed, but missing library stubs or py.typed marker


loggers = setup_loggers([logging.getLogger("bitfount")])


def run(path_to_config_yaml: Union[str, PathLike]) -> None:
    """Runs a pod from a config file."""
    pod = setup_pod_from_config_file(path_to_config_yaml)
    pod.start()


def main() -> None:
    """Script entry point."""
    # Check to see if the code is running in a headless client.
    headless = False
    try:
        if sys.stdin.isatty():
            headless = True
    except AttributeError:  # stdin is NoneType if not headless.
        pass

    if headless:
        fire.Fire(run)

    elif sys.platform == "win32":
        import easygui as easygui

        # Windows doesn't work well with wxasync, so using easygui instead of wx.
        filename = easygui.fileopenbox(filetypes=[["*.yaml", "*.yml", "YAML files"]])
        if filename:
            try:
                run(filename)
            except Exception as e:
                print(e)
                sys.exit(1)
        else:
            print("No file provided.")

    elif sys.platform == "darwin":

        # Use wxPython if client is not headless
        app = wxasync.WxAsyncApp(redirect=True)
        try:
            Frame().Show()
            loop = get_event_loop()
            loop.run_until_complete(app.MainLoop())

        except Exception as e:
            print(e)
            print("The file provided does not match the required format.")
            sys.exit(1)

    else:
        print("Unrecognised OS.")


if __name__ == "__main__":
    main()
