# Copyright Contributors to the Testing Farm project.
# SPDX-License-Identifier: Apache-2.0
"""
The module provides exception classes for testing farm API.
"""
from typing import Any

from fastapi import Request
from fastapi.responses import JSONResponse


class NucleusException(Exception):
    """
    Base Exception class for nucleus api, use this as a parent class.
    Do not use it raw, use GenericError for generic purposes.
    """

    def __init__(self, status_code: int, content: Any, headers: Any = None):
        super().__init__(status_code)
        self.status_code = status_code
        self.content = content
        self.headers = headers


def nucleus_exception_handler(
    request: Request, exc: NucleusException  # pylint: disable=unused-argument
) -> JSONResponse:
    """
    Exception handler is a function which defines what will be returned to user as a response.
    """
    return JSONResponse(status_code=exc.status_code, content=exc.content, headers=exc.headers)


class GenericError(NucleusException):
    """
    Generic purpose error. Returns 500 status code. The default message can be changed.
    https://developer.mozilla.org/en-US/docs/Web/HTTP/Status/500
    """

    def __init__(self, headers: Any = None, message: str = 'Unknown error') -> None:
        super().__init__(status_code=500, content={'message': message}, headers=headers)


class BadRequestError(NucleusException):
    """
    Bad request error. May be used for indicating invalid syntax in request.
    Returns 400 status code. The default message can be changed.
    https://developer.mozilla.org/en-US/docs/Web/HTTP/Status/400
    """

    def __init__(self, headers: Any = None, message: str = 'Bad request') -> None:
        super().__init__(status_code=400, content={'message': message}, headers=headers)


class NoSuchEntityError(NucleusException):
    """
    Not found error. Returns 404 status code. The default message can be changed.
    https://developer.mozilla.org/en-US/docs/Web/HTTP/Status/404
    """

    def __init__(self, headers: Any = None, message: str = 'No such entity') -> None:
        super().__init__(status_code=404, content={'code': 404, 'message': message}, headers=headers)


class NonUniqueValidationError(NucleusException):
    """
    Non unique validation error. May be used to indicate posted object already exists.
    Returns 409 status code. The default message can be changed.
    https://developer.mozilla.org/en-US/docs/Web/HTTP/Status/409
    """

    def __init__(self, headers: Any = None, message: str = 'Object already exists') -> None:
        super().__init__(status_code=409, content={"message": message}, headers=headers)


class NotAuthorizedError(NucleusException):
    """
    Not authorized error. May be used to indicate bad authorizing credentials was send.
    Returns 401 status code. The default message can be changed.
    https://developer.mozilla.org/en-US/docs/Web/HTTP/Status/401
    """

    def __init__(self, headers: Any = None, message: str = 'Not authorized to perform this action') -> None:
        super().__init__(status_code=401, content={"message": message}, headers=headers)


class ForbiddenError(NucleusException):
    """
    Forbidden error. May be used to indicate the client does not have access right to the content.
    Returns 403 status code. The default message can be changed.
    https://developer.mozilla.org/en-US/docs/Web/HTTP/Status/403
    """

    def __init__(self, headers: Any = None, message: str = 'Not authorized to perform this action') -> None:
        super().__init__(status_code=403, content={"message": message}, headers=headers)


class UnprocessableEntityError(NucleusException):
    """
    Forbidden error. May be used to indicate that the server understands the content type of the
    request entity, and the syntax of the request entity is correct,
    but it was unable to process the contained instructions.
    Returns 422 status code. The default message can be changed.
    https://developer.mozilla.org/en-US/docs/Web/HTTP/Status/422
    """

    def __init__(self, headers: Any = None, message: str = 'The entity can not be processed') -> None:
        super().__init__(status_code=422, content={"message": message}, headers=headers)
