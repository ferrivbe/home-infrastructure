from http import HTTPStatus

import pytest
from src.common.error.http import (
    HTTPError,
    HTTPInternalServerError,
    HTTPUnprocessableEntityError,
)


def test_http_error_initialization():
    error = HTTPError(
        http_status=HTTPStatus.BAD_REQUEST,
        error_code="BAD_REQUEST",
        message="Bad request",
        detail="Missing parameter",
    )
    assert error.http_status == HTTPStatus.BAD_REQUEST
    assert error.error_code == "BAD_REQUEST"
    assert error.message == "Bad request"
    assert error.detail == "Missing parameter"
    assert error.status_code == HTTPStatus.BAD_REQUEST


def test_http_unprocessable_entity_error_initialization():
    error = HTTPUnprocessableEntityError(
        error_code="INVALID_INPUT",
        message="Invalid input",
        detail="Age cannot be negative",
    )
    assert error.http_status == HTTPStatus.UNPROCESSABLE_ENTITY
    assert error.error_code == "INVALID_INPUT"
    assert error.message == "Invalid input"
    assert error.detail == "Age cannot be negative"
    assert error.status_code == HTTPStatus.UNPROCESSABLE_ENTITY


def test_http_internal_server_error_initialization():
    error = HTTPInternalServerError(
        error_code="SERVER_ERROR",
        message="Server error",
        detail="Unexpected error occurred",
    )
    assert error.http_status == HTTPStatus.INTERNAL_SERVER_ERROR
    assert error.error_code == "SERVER_ERROR"
    assert error.message == "Server error"
    assert error.detail == "Unexpected error occurred"
    assert error.status_code == HTTPStatus.INTERNAL_SERVER_ERROR
