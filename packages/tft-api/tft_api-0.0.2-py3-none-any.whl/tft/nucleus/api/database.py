# Copyright Contributors to the Testing Farm project.
# SPDX-License-Identifier: Apache-2.0

"""
Testing Farm API - database
"""

import enum
import os
from typing import Generator

import sqlalchemy
import sqlalchemy.ext.declarative
from dynaconf import settings
from sqlalchemy import (
    Boolean,
    Column,
    ForeignKey,
    Integer,
    Interval,
    String,
    create_engine,
)
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy_utils import ChoiceType, EncryptedType, Timestamp
from sqlalchemy_utils.types.encrypted.encrypted_type import AesEngine

# This secret key is used for sqlalchemy_utils.EncryptedType to encrypt secrets in DB
ENCRYPTION_SECRET = os.environ.get('NUCLEUS_DATABASE_SECRET_KEY', 'nucleus')

SQLALCHEMY_DATABASE_URL = os.environ.get('NUCLEUS_SQLALCHEMY_DATABASE_URL', settings.DATABASE_URL)

engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={'sslmode': 'disable'})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# We are using declarative class definitions
Base = sqlalchemy.ext.declarative.declarative_base()


def get_db() -> Generator[sessionmaker, None, None]:
    """
    Retrieve database session.
    """

    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()


class User(Base, Timestamp):  # type: ignore
    """
    Testing Farm User

    name: Name of the user (primary key)
    api_key: Secret key used for authentication to the API endpoints
    enabled: Flag indicating if the user is enabled
    """

    __tablename__ = 'users'

    id = Column(UUID, primary_key=True)

    name = Column(String, nullable=False)
    api_key = Column(EncryptedType(String, ENCRYPTION_SECRET, AesEngine), nullable=False)
    enabled = Column(Boolean, default=True, nullable=False)

    requests = relationship('Request')


class RequestStateType(enum.Enum):
    """
    Enum for state column in Request table.
    """

    NEW = enum.auto()
    QUEUED = enum.auto()
    RUNNING = enum.auto()
    COMPLETE = enum.auto()
    ERROR = enum.auto()


class Request(Base, Timestamp):  # type: ignore
    """
    Testing Farm Test Request.
    """

    __tablename__ = 'requests'

    id = Column(UUID, primary_key=True)
    user_id = Column(UUID, ForeignKey('users.id'), nullable=False)

    generation = Column(Integer, nullable=False, default=0)

    state = Column(ChoiceType(RequestStateType, impl=Integer()), default=RequestStateType.NEW.value, nullable=False)
    notes = Column(JSONB)

    environments_requested = Column(JSONB, nullable=False)
    environments_provisioned = Column(JSONB)

    test = Column(JSONB, nullable=False)

    result = Column(JSONB)

    run = Column(JSONB)

    notification = Column(JSONB)

    queued_time = Column(Interval)
    run_time = Column(Interval)
