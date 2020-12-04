#!/usr/bin/env python3
"""initialise the NiftyPET ninst package"""
__author__ = "Casper O. da Costa-Luis", "Pawel J. Markiewicz"
__date__ = "2020"

import logging
import os
import platform
import re
import sys
from textwrap import dedent

from tqdm.auto import tqdm

__all__ = ["LogHandler", "path_resources", "resources", "dev_info", "gpuinfo"]


class LogHandler(logging.StreamHandler):
    """Custom formatting and tqdm-compatibility"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        fmt = logging.Formatter(
            "%(levelname)s:%(asctime)s:%(name)s:%(funcName)s\n> %(message)s"
        )
        self.setFormatter(fmt)

    def handleError(self, record):
        super().handleError(record)
        raise IOError(record)

    def emit(self, record):
        """Write to tqdm's stream so as to not break progress-bars"""
        try:
            msg = self.format(record)
            tqdm.write(msg, file=self.stream, end=getattr(self, "terminator", "\n"))
            self.flush()
        except RecursionError:
            raise
        except Exception:
            self.handleError(record)


log = logging.getLogger(__name__)
# technically bad practice to add handlers
# https://docs.python.org/3/howto/logging.html#library-config
# log.addHandler(LogHandler())  # do it anyway for convenience

# if using conda put the resources in the folder with the environment name
if "CONDA_DEFAULT_ENV" in os.environ:
    try:
        env = re.findall(r"envs[/\\](.*)[/\\]bin[/\\]python", sys.executable)[0]
    except IndexError:
        env = os.environ["CONDA_DEFAULT_ENV"]
    log.info("conda environment found:" + env)
else:
    env = ""

# create the path for the resources files according to the OS platform
if platform.system() in ["Linux", "Darwin"]:
    path_resources = os.path.join(
        os.path.join(os.path.expanduser("~"), ".niftypet"), env
    )
elif platform.system() == "Windows":
    path_resources = os.path.join(
        os.path.join(os.getenv("LOCALAPPDATA"), ".niftypet"), env
    )
else:
    log.error("unrecognised operating system!")

sys.path.insert(1, path_resources)
try:
    import resources
except ImportError:
    raise ImportError(
        dedent(
            """\
        --------------------------------------------------------------------------
        NiftyPET resources file <resources.py> could not be imported.
        It should be in ~/.niftypet/resources.py (Linux) or
        in //Users//USERNAME//AppData//Local//niftypet//resources.py (Windows)
        but likely it does not exists.
        --------------------------------------------------------------------------"""
        )
    )

if resources.CC_ARCH != "" and platform.system() in ["Linux", "Windows"]:
    from .dinf import dev_info, gpuinfo
else:
    dev_info, gpuinfo = None, None
