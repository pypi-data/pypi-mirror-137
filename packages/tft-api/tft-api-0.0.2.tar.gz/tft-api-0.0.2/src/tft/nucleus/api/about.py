# Copyright Contributors to the Testing Farm project.
# SPDX-License-Identifier: Apache-2.0
"""
The module provides information about the nucleus API.
"""

from typing import Dict

from . import app_version


def about_get() -> Dict[str, str]:
    """
    Main entrypoint for the Molten application.
    """

    return {'app_version': app_version}
