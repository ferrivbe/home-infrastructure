# Import necessary modules and classes for asynchronous operation, mocking, and testing
import asyncio
import json
from unittest.mock import AsyncMock, MagicMock, patch
from uuid import uuid4

import pytest
from src.middleware.request_logger import AsyncIteratorWrapper, RequestLogger
from starlette.requests import Request
from starlette.responses import JSONResponse, Response

# Fixtures for setting up test objects and states


@pytest.fixture
def service_name():
    """Provides a fixed service name for testing."""
    return "test_service"


@pytest.fixture
def request_logger(service_name):
    """Creates a RequestLogger object with a predefined service name."""
    return RequestLogger(service_name)


@pytest.fixture
def request_fixture():
    """Creates a mock HTTP GET request for testing."""
    scope = {
        "type": "http",
        "method": "GET",
        "path": "/test",
        "headers": [],
    }
    return Request(scope)


@pytest.fixture
def response():
    """Provides a simple HTTP response object for testing."""
    return Response()


@pytest.fixture
def logger():
    """Creates a mock logger object."""
    return MagicMock()


# Test functions to verify the functionality of RequestLogger


@pytest.mark.asyncio
async def test_log_request(request_logger, request_fixture, response, logger):
    """
    Tests the _log_request method of RequestLogger for logging requests correctly.
    """
    # Simulate a request with a unique ID and a mock body
    request_fixture.state.request_id = str(uuid4())
    request_fixture.body = AsyncMock(return_value=b'{"test": "body"}')

    # Mock function to simulate calling the next request handler
    call_next = AsyncMock(return_value=response)

    # Use patching to mock internal behaviors and verify interactions
    with patch.object(
        request_logger, "_serialize_data", return_value='{"test": "body"}'
    ) as mock_serialize, patch(
        "src.utils.logger.Logger", return_value=logger
    ) as mock_logger, patch.object(
        request_logger, "_log_response", return_value=response
    ) as mock_log_response:

        result = await request_logger._log_request(request_fixture, call_next)

        mock_log_response.assert_called_once()
        assert result.headers["request_id"] == request_fixture.state.request_id
        assert result is response


@pytest.mark.asyncio
async def test_serialize_data(request_logger):
    """
    Tests serialization of data by the RequestLogger.
    """
    data = '{"key": "value"}'
    assert request_logger._serialize_data(data) == json.loads(data)
    assert request_logger._serialize_data("") is None
    assert request_logger._serialize_data("{bad json") is None


@pytest.mark.asyncio
async def test_set_request_body(request_logger, request_fixture):
    """
    Verifies that the request body is correctly set by the RequestLogger.
    """
    message = {"type": "http.request", "body": b'{"key": "value"}'}
    request_fixture._receive = AsyncMock(return_value=message)

    await request_logger._set_request_body(request_fixture)

    received_message = await request_fixture._receive()
    assert received_message == message


@pytest.mark.asyncio
async def test_log_response(request_logger, request_fixture, response, logger):
    """
    Tests logging of responses by the RequestLogger.
    """
    request_fixture.state.request_id = str(uuid4())
    response_body = b'{"response": "data"}'
    response.__dict__["body_iterator"] = AsyncIteratorWrapper([response_body])

    with patch.object(
        request_logger,
        "_serialize_data",
        return_value=json.loads(response_body.decode()),
    ) as mock_serialize:
        result = await request_logger._log_response(request_fixture, response, logger)

        mock_serialize.assert_called_once_with(response_body.decode())
        assert json.loads(response_body.decode()) == mock_serialize.return_value
        assert result == response

    # Test error handling in _log_response
    with patch.object(
        request_logger, "_serialize_data", side_effect=Exception("Test exception")
    ):
        result = await request_logger._log_response(request_fixture, response, logger)
        assert isinstance(result, JSONResponse)
        assert result.status_code == 500


@pytest.mark.asyncio
async def test_log_request_integration(request_logger, request_fixture, response):
    """
    Integrative test for logging a request using RequestLogger.
    """
    request_fixture.body = AsyncMock(return_value=b'{"test": "body"}')
    call_next = AsyncMock(return_value=response)

    with patch.object(RequestLogger, "_log_request", autospec=True) as mock_log_request:
        await request_logger.log_request(request_fixture, call_next)
        mock_log_request.assert_called_once_with(
            request_logger, request_fixture, call_next
        )


# Additional fixtures for testing with different content types


@pytest.fixture
def json_request_fixture():
    """Creates a mock JSON HTTP GET request."""
    scope = {
        "type": "http",
        "method": "GET",
        "path": "/test",
        "headers": [(b"content-type", b"application/json")],
    }
    return Request(scope)


@pytest.fixture
def multipart_form_data_request():
    """Creates a mock multipart/form-data HTTP POST request."""
    scope = {
        "type": "http",
        "method": "POST",
        "path": "/upload",
        "headers": [(b"content-type", b"multipart/form-data")],
    }
    return Request(scope)


# Tests for handling different request content types


@pytest.mark.asyncio
async def test_get_request_body_with_json_content_type(
    request_logger, json_request_fixture
):
    """
    Tests retrieval of the request body for JSON content type.
    """
    json_request_fixture._receive = AsyncMock(
        return_value={"type": "http.request", "body": b'{"key": "value"}'}
    )

    with patch.object(
        request_logger, "_set_request_body", return_value=None
    ) as mock_set_request_body:
        body = await request_logger._get_request_body(json_request_fixture)

        mock_set_request_body.assert_called_once()
        assert json.loads(body) == {"key": "value"}


@pytest.mark.asyncio
async def test_get_request_body_with_multipart_content_type(
    request_logger, multipart_form_data_request
):
    """
    Tests handling of multipart/form-data content type, expecting no request body to be returned.
    """
    assert await request_logger._get_request_body(multipart_form_data_request) is None
