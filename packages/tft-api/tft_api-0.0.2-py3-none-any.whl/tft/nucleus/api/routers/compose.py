# Copyright Contributors to the Testing Farm project.
# SPDX-License-Identifier: Apache-2.0
"""
The module provides implementation of test requests router
"""
from fastapi import APIRouter
from fastapi_versioning import version

from ..schemes import compose

router = APIRouter()


# TODO: it does nothing, for working docs
@router.get('/composes', response_model=compose.SupportedComposesOut)
@version(0, 1)  # type: ignore
def supported_composes() -> compose.SupportedComposesOut:
    """
    Create new test request handler
    """
    response = compose.SupportedComposesOut()
    return response
