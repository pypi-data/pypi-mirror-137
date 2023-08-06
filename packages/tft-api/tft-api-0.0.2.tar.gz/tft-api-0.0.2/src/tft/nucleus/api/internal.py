# Copyright Contributors to the Testing Farm project.
# SPDX-License-Identifier: Apache-2.0
"""
The module provides public implementation of testing farm API.
"""
from typing import Dict

from fastapi import FastAPI
from fastapi_versioning import VersionedFastAPI, version

from .about import about_get
from .errors import NucleusException, nucleus_exception_handler
from .routers import test_request, user

api = FastAPI(
    title='Testing Farm Private API',
)


@api.get('/about', summary='About Testing Farm')
@version(0, 1)  # type: ignore
def get_about() -> Dict[str, str]:
    """
    The function returns metadata about nucleus api package.
    """
    return about_get()


api.include_router(user.router)
api.include_router(test_request.internal_router)


# This line should be at the end of the file
api = VersionedFastAPI(api, version_format='{major}.{minor}', prefix_format='/v{major}.{minor}')


# Workaround of handler catching
# See: https://github.com/DeanWay/fastapi-versioning/issues/30
for sub_api in api.routes:
    assert hasattr(sub_api, 'app')
    if hasattr(sub_api.app, "add_exception_handler"):  # type: ignore
        sub_api.app.add_exception_handler(NucleusException, nucleus_exception_handler)  # type: ignore
