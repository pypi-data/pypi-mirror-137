# Copyright Contributors to the Testing Farm project.
# SPDX-License-Identifier: Apache-2.0
"""
The module provides implementation of test requests router
"""
from uuid import UUID

from fastapi import APIRouter, Depends
from fastapi_versioning import version
from sqlalchemy.orm import Session

from .. import crud
from ..database import get_db
from ..schemes import test_request

router = APIRouter()
internal_router = APIRouter()


@router.post('/requests', response_model=test_request.RequestCreateOut)
@version(0, 1)  # type: ignore
def request_a_new_test(
    request_in: test_request.RequestCreateIn, session: Session = Depends(get_db)
) -> test_request.RequestCreateOut:
    """
    Create new test request handler
    """
    return crud.create_test_request(session, request_in)


@router.get('/requests/{request_id}', response_model=test_request.RequestGetUpdateOut)
@version(0, 1)  # type: ignore
def test_request_details(request_id: str, session: Session = Depends(get_db)) -> test_request.RequestGetUpdateOut:
    """
    Get test request handler
    """
    return crud.get_test_request(session, request_id)  # type: ignore


@internal_router.put('/requests/{request_id}', response_model=test_request.RequestGetUpdateOut)
@version(0, 1)  # type: ignore
def update_test_request(
    request_id: str, request_in: test_request.RequestUpdateIn, session: Session = Depends(get_db)
) -> test_request.RequestGetUpdateOut:
    """
    Update test request handler
    """
    return crud.update_test_request(session, UUID(request_id), request_in)
