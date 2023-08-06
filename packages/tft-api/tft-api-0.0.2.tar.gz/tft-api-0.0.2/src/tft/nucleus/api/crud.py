# Copyright Contributors to the Testing Farm project.
# SPDX-License-Identifier: Apache-2.0
"""
The module provides implementation of Create, Read, Update, and Delete database operations.
"""
from datetime import datetime
from typing import List
from uuid import UUID, uuid4

from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from . import errors
from .database import Request, RequestStateType, User
from .schemes import Auth, test_request, user


def get_test_request(session: Session, request_id: UUID) -> test_request.RequestGetUpdateOut:
    """
    Retrieve request from database and transform to response schema.
    """
    request = session.query(Request).filter(Request.id == request_id).first()
    if not request:
        raise errors.NoSuchEntityError()
    request_out = test_request.RequestGetUpdateOut(
        user_id=request.user_id,
        test=request.test,
        # state=request.state,  # TODO: uncomment once database migrated
        state=request.state.name.lower(),
        run=request.run,
        queued_time=request.queued_time,
        run_time=request.run_time,
        created=request.created,
        updated=request.updated,
    )
    return request_out


def create_test_request(
    session: Session, test_request_create_in: test_request.RequestCreateIn
) -> test_request.RequestCreateOut:
    """
    Create test request in database and transform it to response schema.
    """
    auth_user = session.query(User).filter(User.api_key == test_request_create_in.api_key).first()
    if not auth_user:
        raise errors.NotAuthorizedError
    request_id = str(uuid4())
    db_test_request = Request(
        id=request_id,
        user_id=auth_user.id,
        test=jsonable_encoder(test_request_create_in.test),
        environments_requested=jsonable_encoder(test_request_create_in.environments),
        notification=jsonable_encoder(test_request_create_in.notification),
    )
    session.add(db_test_request)
    session.commit()
    session.refresh(db_test_request)
    request_out = test_request.RequestCreateOut(
        id=request_id,
        test=test_request_create_in.test,
        notification=test_request_create_in.notification,
        environments=test_request_create_in.environments,
        created=db_test_request.created,
        updated=db_test_request.updated,
        state=db_test_request.state.name.lower(),  # TODO: remove once database migrated
    )
    return request_out


def update_test_request(
    session: Session, request_id: UUID, test_request_in: test_request.RequestUpdateIn
) -> test_request.RequestGetUpdateOut:
    """
    Update test request in database and return response schema.
    """
    auth_user = session.query(User).filter(User.api_key == test_request_in.api_key).first()
    if not auth_user:
        raise errors.NotAuthorizedError

    update_test_request_db = session.query(Request).filter(Request.id == str(request_id)).first()
    if not update_test_request_db:
        raise errors.NoSuchEntityError()

    queued_time = None
    if test_request_in.state == RequestStateType.RUNNING:
        queued_time = datetime.utcnow() - update_test_request_db.created

    run_time = None
    if test_request_in.state in [RequestStateType.COMPLETE, RequestStateType.ERROR]:
        run_time = datetime.utcnow() - update_test_request_db.created

    updated_test_request_db = (
        session.query(Request)
        .filter(Request.id == str(request_id))
        .update(
            {
                'state': test_request_in.state or update_test_request_db.state,
                'notes': test_request_in.notes or update_test_request_db.notes,
                'environments_provisioned': test_request_in.environment_provisioned
                or update_test_request_db.environments_provisioned,  # noqa # pylint: disable=line-too-long
                'result': test_request_in.result or update_test_request_db.result,
                'run': test_request_in.run or update_test_request_db.run,
                'queued_time': queued_time or update_test_request_db.queued_time,
                'run_time': run_time or update_test_request_db.run_time,
            }
        )
    )

    if not updated_test_request_db:
        raise errors.NoSuchEntityError()

    session.commit()

    test_request_db = session.query(Request).filter(Request.id == str(request_id)).first()
    assert test_request_db is not None

    test_request_out = test_request.RequestGetUpdateOut(
        user_id=test_request_db.user_id,
        test=test_request_db.test,
        # state=test_request_db.state,  # TODO: uncomment once database migrated
        state=test_request_db.state.name.lower(),
        run=test_request_db.run,
        queued_time=test_request_db.queued_time,
        run_time=test_request_db.run_time,
        created=test_request_db.created,
        updated=test_request_db.updated,
    )
    return test_request_out


def create_user(session: Session, user_in: user.UserCreateUpdateIn) -> user.UserCreateGetUpdateOut:
    """
    Create a user in database and transform it to response schema.
    """
    auth_user = session.query(User).filter(User.api_key == user_in.api_key).first()
    if not auth_user:
        raise errors.NotAuthorizedError
    user_id = str(uuid4())
    user_db = User(id=user_id, name=user_in.name, api_key=user_in.user_api_key, enabled=user_in.enabled)
    session.add(user_db)
    session.commit()
    session.refresh(user_db)
    user_out = user.UserCreateGetUpdateOut(
        id=user_db.id,
        name=user_db.name,
        api_key=user_db.api_key,
        enabled=user_db.enabled,
        created=user_db.created,
        updated=user_db.updated,
    )
    return user_out


def get_user(session: Session, user_id: UUID, auth: Auth) -> user.UserCreateGetUpdateOut:
    """
    Retrieve user from database and transform to response schema.
    """
    auth_user = session.query(User).filter(User.api_key == auth.api_key).first()
    if not auth_user:
        raise errors.NotAuthorizedError

    user_db = session.query(User).filter(User.id == str(user_id)).first()
    if not user_db:
        raise errors.NoSuchEntityError()

    user_out = user.UserCreateGetUpdateOut(
        id=user_db.id,
        name=user_db.name,
        api_key=user_db.api_key,
        enabled=user_db.enabled,
        created=user_db.created,
        updated=user_db.updated,
    )
    return user_out


def get_users(session: Session, auth: Auth) -> List[user.UserCreateGetUpdateOut]:
    """
    Retrieve users from database and transform to response schemes list.
    """
    auth_user = session.query(User).filter(User.api_key == auth.api_key).first()
    if not auth_user:
        raise errors.NotAuthorizedError

    users_db = session.query(User).all()
    if not users_db:
        raise errors.NoSuchEntityError()

    users_out = []
    for user_db in users_db:
        users_out.append(
            user.UserCreateGetUpdateOut(
                id=user_db.id,
                name=user_db.name,
                api_key=user_db.api_key,
                enabled=user_db.enabled,
                created=user_db.created,
                updated=user_db.updated,
            )
        )
    return users_out


def update_user(session: Session, user_id: UUID, user_in: user.UserCreateUpdateIn) -> user.UserCreateGetUpdateOut:
    """
    Update user in database and return response schema.
    """
    auth_user = session.query(User).filter(User.api_key == user_in.api_key).first()
    if not auth_user:
        raise errors.NotAuthorizedError

    update_user_db = session.query(User).filter(User.id == str(user_id)).first()
    if not update_user_db:
        raise errors.NoSuchEntityError()

    # For enabled flag we can't just do `user_in.enabled or update_user_db.enabled` (False or True will return False)
    if user_in.enabled is not None:
        enabled = user_in.enabled
    else:
        enabled = update_user_db.enabled

    updated_user_db = (
        session.query(User)
        .filter(User.id == str(user_id))
        .update(
            {
                'name': user_in.name or update_user_db.name,
                'api_key': user_in.user_api_key or update_user_db.api_key,
                'enabled': enabled,
            }
        )
    )

    if not updated_user_db:
        raise errors.NoSuchEntityError()

    session.commit()

    user_db = session.query(User).filter(User.id == str(user_id)).first()
    assert user_db is not None

    user_out = user.UserCreateGetUpdateOut(
        id=user_db.id,
        name=user_db.name,
        api_key=user_db.api_key,
        enabled=user_db.enabled,
        created=user_db.created,
        updated=user_db.updated,
    )
    return user_out


def delete_user(session: Session, user_id: UUID, auth: Auth) -> None:
    """
    Delete the user from database.
    """
    auth_user = session.query(User).filter(User.api_key == auth.api_key).first()
    if not auth_user:
        raise errors.NotAuthorizedError

    user_db = session.query(User).filter(User.id == str(user_id)).first()
    if not user_db:
        raise errors.NoSuchEntityError()

    session.delete(user_db)  # type: ignore
    session.commit()
