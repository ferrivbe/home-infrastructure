from unittest.mock import AsyncMock, patch

import pytest
from fastapi import HTTPException, Request
from fastapi.exceptions import RequestValidationError
from src.common.error.http import HTTPError
from src.middleware.exception import (
    default_exception_handler,
    exception_handler,
    python_exception_handler,
    request_validation_error_handler,
)
from src.utils.logger import Logger


@pytest.mark.asyncio
async def test_exception_handler():
    """
    Test the custom HTTP error handler.
    """
    request_mock = AsyncMock(spec=Request)
    request_mock.method = "GET"
    request_mock.url.path = "/test"
    http_error = HTTPError(
        http_status=400,
        error_code="BadRequest",
        message="Bad request",
        detail="Invalid parameters",
    )

    with patch.object(Logger, "error") as logger_mock:
        response = await exception_handler(request_mock, http_error)

    assert response.status_code == 400
    assert (
        response.body.decode()
        == '{"error_code":"BadRequest","message":"Bad request","detail":"Invalid parameters","target":"GET|/test"}'
    )


@pytest.mark.asyncio
async def test_default_exception_handler():
    """
    Test the default HTTP exception handler.
    """
    request_mock = AsyncMock(spec=Request)
    request_mock.method = "POST"
    request_mock.url.path = "/default"
    http_exception = HTTPException(status_code=500, detail="Server error")

    with patch.object(Logger, "error") as logger_mock:
        response = await default_exception_handler(request_mock, http_exception)

    assert response.status_code == 500
    assert (
        response.body.decode()
        == '{"error_code":"GenericExceptionRaised","message":"Something went wrong inside a process.","detail":"Server error","target":"POST|/default"}'
    )


@pytest.mark.asyncio
async def test_python_exception_handler():
    """
    Test the handler for unexpected Python exceptions.
    """
    request_mock = AsyncMock(spec=Request)
    request_mock.method = "PUT"
    request_mock.url.path = "/python-error"
    exception = ValueError("An unexpected error occurred")

    response = await python_exception_handler(request_mock, exception)

    assert response.status_code == 500
    assert (
        response.body.decode()
        == '{"error_code":"InternalServerError","message":"Something went wrong!","detail":"An unexpected error occurred","target":"PUT|/python-error"}'
    )


@pytest.mark.asyncio
async def test_request_validation_error_handler():
    """
    Test the request validation error handler.
    """
    request_mock = AsyncMock(spec=Request)
    request_mock.method = "DELETE"
    request_mock.url.path = "/validation-error"
    error_details = [
        {
            "loc": ("query", "test"),
            "msg": "field required",
            "type": "value_error.missing",
        }
    ]
    validation_exception = RequestValidationError(errors=error_details)

    response = await request_validation_error_handler(
        request_mock, validation_exception
    )

    assert response.status_code == 400
    assert (
        response.body.decode()
        == '{"error_code":"RequestValidationError","message":"There are errors in the request.","detail":[{"loc":["query","test"],"msg":"field required","type":"value_error.missing"}],"target":"DELETE|/validation-error"}'
    )
