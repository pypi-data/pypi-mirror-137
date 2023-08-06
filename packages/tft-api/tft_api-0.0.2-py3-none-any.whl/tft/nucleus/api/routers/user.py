# Copyright Contributors to the Testing Farm project.
# SPDX-License-Identifier: Apache-2.0
"""
The module provides implementation of users router
"""
from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends
from fastapi_versioning import version
from sqlalchemy.orm import Session

from .. import crud
from ..database import get_db
from ..schemes import Auth, user

router = APIRouter()


@router.post('/users', response_model=user.UserCreateGetUpdateOut)
@version(0, 1)  # type: ignore
def create_user(user_in: user.UserCreateUpdateIn, session: Session = Depends(get_db)) -> user.UserCreateGetUpdateOut:
    """
    Create new user handler
    """
    return crud.create_user(session, user_in)


@router.put('/users/{user_id}', response_model=user.UserCreateGetUpdateOut)
@version(0, 1)  # type: ignore
def update_user(
    user_id: str, user_in: user.UserCreateUpdateIn, session: Session = Depends(get_db)
) -> user.UserCreateGetUpdateOut:
    """
    Update new user handler
    """
    return crud.update_user(session, UUID(user_id), user_in)


@router.get('/users/{user_id}', response_model=user.UserCreateGetUpdateOut)
@version(0, 1)  # type: ignore
def get_user(user_id: str, auth: Auth, session: Session = Depends(get_db)) -> user.UserCreateGetUpdateOut:
    """
    Get user handler
    """
    return crud.get_user(session, UUID(user_id), auth)


@router.get('/users', response_model=List[user.UserCreateGetUpdateOut])
@version(0, 1)  # type: ignore
def get_users(auth: Auth, session: Session = Depends(get_db)) -> List[user.UserCreateGetUpdateOut]:
    """
    Get users handler
    """
    return crud.get_users(session, auth)


@router.delete('/users/{user_id}')
@version(0, 1)  # type: ignore
def delete_user(user_id: str, auth: Auth, session: Session = Depends(get_db)) -> None:
    """
    Delete user handler
    """
    return crud.delete_user(session, UUID(user_id), auth)
