import json
import logging
import logging.config
import sys

from fastapi import Request


class JSONFormatter(logging.Formatter):
    """
    A custom formatter that outputs log records in JSON format.

    This formatter transforms logging records into a structured JSON format, making
    the log output easily parseable and suitable for ingestion into log management
    and analysis tools that support JSON.

    Methods:
        format(record): Formats the log record into JSON format.
        process_log_record(log_record): Processes the log record before formatting.
        _extract_value(value): Recursively processes the log record to ensure all values are serializable.
    """

    def format(self, record):
        """
        Formats the log record into JSON format.

        Overrides the base class format method to provide JSON formatting of log records.
        It processes the log record to ensure it contains only serializable values and
        then converts it into a JSON string.

        Args:
            record (logging.LogRecord): The log record.

        Returns:
            str: A JSON string representing the log record.
        """
        log_record = {
            "message": record.msg,
            "detail": record.detail,
            "timestamp": record.created,
        }
        processed_record = self.process_log_record(log_record)
        return json.dumps(processed_record, default=str)

    def process_log_record(self, log_record):
        """
        Processes the log record to ensure it contains only serializable values.

        This method iterates over the items in the log record, processing each value
        to ensure that it is suitable for JSON serialization. This includes ensuring
        that values are not None and handling nested dictionaries.

        Args:
            log_record (dict): The log record dictionary to process.

        Returns:
            dict: The processed log record with only serializable values.
        """
        processed_record = {
            key: self._extract_value(value)
            for key, value in log_record.items()
            if value is not None
        }
        return processed_record

    def _extract_value(self, value):
        """
        Recursively processes values, ensuring they are suitable for JSON serialization.

        If the value is a dictionary, this method is applied recursively to each of its
        items. Otherwise, the value is returned directly. This ensures that all values
        in the log record are serializable and that dictionaries contain only non-None values.

        Args:
            value: The value to process.

        Returns:
            The processed value, suitable for JSON serialization.
        """
        if isinstance(value, dict):
            return {
                key: self._extract_value(val)
                for key, val in value.items()
                if val is not None
            }
        else:
            return value


class Logger:
    """
    Facilitates logging with request-specific details in a FastAPI application.

    This class is designed to capture and log messages with additional context from
    FastAPI requests. It supports logging information, errors, and exceptions with
    request details and custom payload. Sensitive information can be masked, and
    overly large payloads can be trimmed.

    Attributes:
        request (Request): The FastAPI request object providing context.
        service_name (str): The name of the service or application.

    Methods:
        _format_payload(payload): Formats the payload, masking or trimming as configured.
        _get_headers(): Retrieves request headers.
        _populate_detail(payload): Constructs a detail dictionary with request and payload information.
        info(payload, message): Logs an informational message with additional context.
        exception(payload, message): Logs an exception with additional context.
        error(payload, message): Logs an error with additional context.
    """

    def __init__(
        self,
        service_name: str,
        request: Request = None,
    ):
        """
        Initializes the logger with a request and service name.

        Sets up the logger configuration, including a custom JSON formatter for the messages.
        It also configures which information should be trimmed or masked in the logs.

        Args:
            request (Request, optional): The FastAPI request object.
            service_name (str, optional): A name identifying the service. Defaults to "shake-infrastructure".
        """
        self.request = request
        self.service_name = service_name
        self._logger = logging.getLogger(service_name)

        self.trim_properties = [
            "file_content",
            "text",
            "url",
        ]
        self.mask_properties = [
            "password",
            "access_token",
            "refresh_token",
            "id_token",
        ]

        logging_config = {
            "version": 1,
            "disable_existing_loggers": True,
            "formatters": {
                "json": {
                    "()": JSONFormatter,
                },
            },
            "handlers": {
                "console": {
                    "class": "logging.StreamHandler",
                    "level": "INFO",
                    "formatter": "json",
                    "stream": sys.stderr,
                },
            },
            "loggers": {
                service_name: {
                    "handlers": ["console"],
                    "level": "INFO",
                    "propagate": False,
                },
            },
        }

        logging.config.dictConfig(logging_config)

    def _format_payload(self, payload: dict) -> dict:
        """
        Formats the payload by masking or trimming specified properties.

        This method is responsible for ensuring that the payload does not contain
        sensitive information in clear text and that long values are trimmed to a
        reasonable length. It iterates over the payload, applying the appropriate
        transformation based on the property name.

        Args:
            payload (dict): The original payload.

        Returns:
            dict: The formatted payload, with sensitive information masked and long values trimmed.
        """
        if payload is not None:
            for key in payload:
                if (
                    key in self.trim_properties
                    and isinstance(payload[key], str)
                    and len(payload[key]) > 100
                ):
                    payload[key] = payload[key][:100] + "..."
                if key in self.mask_properties:
                    payload[key] = "[masked]"
            return payload

    def _get_headers(self) -> dict:
        """
        Retrieves headers from the FastAPI request.

        This method extracts the request headers and returns them in a dictionary format.

        Returns:
            dict: The request headers.
        """
        return dict(self.request.headers)

    def _populate_detail(self, payload: dict) -> dict:
        """
        Constructs a detailed dictionary with request and payload information.

        This method populates a dictionary with various details about the request,
        including the service name, method, URL path, and headers. It also formats
        the payload using _format_payload and includes it in the details.

        Args:
            payload (dict): The original payload to include in the details.

        Returns:
            dict: A detailed dictionary with enriched context from the request and formatted payload.
        """
        detail = {
            "service_name": self.service_name,
            "target": f"{self.request.method} {self.request.url}",
            "payload": self._format_payload(payload),
            "x-forwarded-for": self.request.headers.get("x-forwarded-for"),
            "request_id": self.request.headers.get("request_id"),
        }

        return detail

    def info(self, payload: dict, message: str = "event") -> None:
        """
        Logs an informational message with detailed context.

        This method logs an informational message, including detailed request and payload
        information. It is designed to exclude logging for specific paths to avoid
        unnecessary noise in the logs.

        Args:
            payload (dict): The payload to log.
            message (str): The informational message to log.
        """
        if self.request.url.path != "/openapi.json":
            self._logger.info(
                message,
                extra={"detail": self._populate_detail(payload)},
            )

    def exception(self, payload: dict, message: str = "event") -> None:
        """
        Logs an exception with detailed context.

        This method captures exceptions, logging them along with detailed request and
        payload information. It is especially useful for debugging and tracing exceptions
        as they provide context to the error.

        Args:
            payload (dict): The payload associated with the exception.
            message (str): The exception message.
        """
        self._logger.exception(
            message,
            extra={"detail": self._populate_detail(payload)},
        )

    def error(self, payload: dict, message: str = "event") -> None:
        """
        Logs an error message with detailed context.

        Similar to the exception method, this method logs error messages, including
        detailed request and payload information. It's used for capturing errors that
        might not raise exceptions but are significant enough to be logged.

        Args:
            payload (dict): The payload associated with the error.
            message (str): The error message.
        """
        self._logger.error(
            message,
            extra={"detail": self._populate_detail(payload)},
        )
