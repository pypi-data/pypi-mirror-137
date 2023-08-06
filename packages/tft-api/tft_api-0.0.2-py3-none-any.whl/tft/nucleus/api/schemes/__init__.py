# Copyright Contributors to the Testing Farm project.
# SPDX-License-Identifier: Apache-2.0
"""
The module provides commonly used schemes across different endpoints
"""
from pydantic import BaseModel, Field  # pylint: disable=no-name-in-module


class Auth(BaseModel):
    """
    The schema used for authentication only purposes
    """

    api_key: str = Field(..., description=('An unique identifier used to authenticate a client.'))
