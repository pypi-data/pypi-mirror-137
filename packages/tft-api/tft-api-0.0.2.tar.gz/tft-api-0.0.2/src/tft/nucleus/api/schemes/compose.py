# Copyright Contributors to the Testing Farm project.
# SPDX-License-Identifier: Apache-2.0
"""
The module provides schemes of test requests
"""
from typing import List

from pydantic import BaseModel, Field  # pylint: disable=no-name-in-module


class Compose(BaseModel):
    """
    Testing compose
    """

    name: str = Field(..., description=('Name of the compose.'))


class SupportedComposesOut(BaseModel):
    """
    Get supported composes response
    """

    composes: List[Compose] = Field(..., description=('Composes supported by Testing Farm.'))
