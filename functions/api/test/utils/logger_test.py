import json
import logging
from unittest.mock import Mock, patch
from urllib.parse import urlparse

import pytest
from fastapi import Request
from src.utils.logger import JSONFormatter, Logger

SAMPLE_PAYLOAD = {"key": "value", "password": "secret", "text": "a" * 105}
SAMPLE_HEADERS = {"x-forwarded-for": "123.123.123.123", "request_id": "abcd-1234"}


def create_mock_request(headers=SAMPLE_HEADERS):
    request = Mock(spec=Request)
    request.headers = headers
    request.method = "GET"
    request.url = urlparse("http://testserver/test")
    return request


@pytest.fixture
def logger_fixture():
    request = create_mock_request()
    logger = Logger("test-service", request)
    return logger


def test_json_formatter_format():
    formatter = JSONFormatter()
    record = logging.LogRecord(
        name="test",
        level=logging.INFO,
        pathname="",
        lineno=0,
        msg="Test message",
        args=(),
        exc_info=None,
    )
    record.created = 1234567890.123
    record.detail = {"key": "value"}

    formatted_record = json.loads(formatter.format(record))
    assert formatted_record["message"] == "Test message"
    assert formatted_record["detail"] == {"key": "value"}
    assert formatted_record["timestamp"] == 1234567890.123


def test_json_formatter_process_log_record():
    formatter = JSONFormatter()
    log_record = {"key": "value", "none_key": None}
    processed_record = formatter.process_log_record(log_record)
    assert "none_key" not in processed_record
    assert processed_record == {"key": "value"}


def test_json_formatter_extract_value():
    formatter = JSONFormatter()
    processed_value = formatter._extract_value({"key": "value", "none_key": None})
    assert processed_value == {"key": "value"}


def test_logger_info(logger_fixture):
    with patch.object(logger_fixture._logger, "info") as mock_info:
        logger_fixture.info(SAMPLE_PAYLOAD, "Test Info")
        mock_info.assert_called_once()
        args, kwargs = mock_info.call_args
        assert "Test Info" in args
        assert "[masked]" in kwargs["extra"]["detail"]["payload"]["password"]
        assert kwargs["extra"]["detail"]["payload"]["text"].endswith("...")


def test_logger_exception(logger_fixture):
    with patch.object(logger_fixture._logger, "exception") as mock_exception:
        logger_fixture.exception(SAMPLE_PAYLOAD, "Test Exception")
        mock_exception.assert_called_once()
        args, kwargs = mock_exception.call_args
        assert "Test Exception" in args
        assert "[masked]" in kwargs["extra"]["detail"]["payload"]["password"]


def test_logger_error(logger_fixture):
    with patch.object(logger_fixture._logger, "error") as mock_error:
        logger_fixture.error(SAMPLE_PAYLOAD, "Test Error")
        mock_error.assert_called_once()
        args, kwargs = mock_error.call_args
        assert "Test Error" in args
        assert "[masked]" in kwargs["extra"]["detail"]["payload"]["password"]


def test_logger_format_payload_none_case(logger_fixture):
    formatted_payload = logger_fixture._format_payload(None)
    assert formatted_payload is None, "Expected None for None input payload"


def test_logger_format_payload_trim_and_mask(logger_fixture):
    payload = {
        "file_content": "x" * 105,  # Expect trimming
        "password": "secret",  # Expect masking
        "normal_key": "value",
    }
    expected_result = {
        "file_content": "x" * 100 + "...",
        "password": "[masked]",
        "normal_key": "value",
    }
    formatted_payload = logger_fixture._format_payload(payload)
    assert (
        formatted_payload == expected_result
    ), "Payload trimming and masking did not work as expected"


def test_logger_get_headers(logger_fixture):
    headers = logger_fixture._get_headers()
    assert headers == SAMPLE_HEADERS, "Headers do not match the expected sample headers"


def test_logger_populate_detail_with_payload(logger_fixture):
    detail = logger_fixture._populate_detail(SAMPLE_PAYLOAD)
    assert detail["service_name"] == "test-service", "Service name did not match"
    assert detail["target"].startswith("GET"), "HTTP method in target is incorrect"
    assert "[masked]" in detail["payload"]["password"], "Password was not masked"
    assert detail["payload"]["text"].endswith(
        "..."
    ), "Text was not trimmed appropriately"
    assert "x-forwarded-for" in detail, "Expected header is missing in detail"
    assert "request_id" in detail, "Expected header is missing in detail"


def test_logger_info_skipped_path(logger_fixture):
    logger_fixture.request.url = urlparse("http://testserver/openapi.json")
    with patch.object(logger_fixture._logger, "info") as mock_info:
        logger_fixture.info(SAMPLE_PAYLOAD)
        mock_info.assert_not_called(), "Logger should not log for excluded paths"


def test_logger_exception_without_payload(logger_fixture):
    with patch.object(logger_fixture._logger, "exception") as mock_exception:
        logger_fixture.exception(None, "Exception without payload")
        mock_exception.assert_called_once()
        args, kwargs = mock_exception.call_args
        assert "Exception without payload" in args, "Exception message did not match"
        assert (
            kwargs["extra"]["detail"]["payload"] is None
        ), "Expected payload to be None"


def test_logger_error_with_empty_payload(logger_fixture):
    with patch.object(logger_fixture._logger, "error") as mock_error:
        logger_fixture.error({}, "Error with empty payload")
        mock_error.assert_called_once()
        args, kwargs = mock_error.call_args
        assert "Error with empty payload" in args, "Error message did not match"
        assert (
            kwargs["extra"]["detail"]["payload"] == {}
        ), "Expected payload to be empty"
