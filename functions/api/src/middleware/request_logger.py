import json
from uuid import uuid4

from fastapi import Request, Response
from fastapi.responses import JSONResponse
from starlette.types import Message
from src.utils.logger import Logger


class AsyncIteratorWrapper:
    """
    Wraps an iterable object to provide an asynchronous iterator interface.

    This wrapper allows for the object to be iterated over in an asynchronous context,
    returning elements from the underlying iterator when awaited.

    Attributes:
        _iterator: An iterator of the wrapped iterable object.
    """

    def __init__(self, obj):
        """
        Initializes the AsyncIteratorWrapper with the given iterable object.

        Args:
            obj: An iterable object to be wrapped for asynchronous iteration.
        """
        self._iterator = iter(obj)

    def __aiter__(self):
        """
        Returns the asynchronous iterator itself, allowing use of the async for statement.

        Returns:
            AsyncIteratorWrapper: The instance of itself, enabling asynchronous iteration.
        """
        return self

    async def __anext__(self):
        """
        Asynchronously returns the next item from the iterator.

        This method is awaited in an asynchronous context to retrieve the next element
        from the wrapped iterable. If the iterator is exhausted, it raises StopAsyncIteration.

        Returns:
            The next item from the iterator.

        Raises:
            StopAsyncIteration: If the iterator is exhausted, indicating no more elements to return.
        """
        try:
            return next(self._iterator)
        except StopIteration:
            raise StopAsyncIteration from None


class RequestLogger:
    """
    Provides middleware functionality for logging requests and responses in an ASGI application.

    This class logs incoming requests and outgoing responses, including their bodies and
    associated metadata, using a provided logger. It uniquely identifies requests using UUIDs.

    Attributes:
        service_name: A string representing the name of the service for logging purposes.
    """

    def __init__(self, service_name: str):
        """
        Initializes the RequestLogger with the specified service name.

        Args:
            service_name: A string representing the name of the service to be used in logging.
        """
        self.service_name = service_name

    async def _set_request_body(self, request: Request):
        """
        Sets the body of the request in its state for later retrieval.

        This method is a helper function designed to capture and set the request body
        so it can be accessed again later without consuming the stream.

        Args:
            request: The Request object from which the body will be read and set.
        """
        return await request.body()

    async def _log_request(self, request: Request, call_next):
        """
        Logs the incoming request and processes it through the next request handler.

        This method logs the incoming request's body and metadata, assigns a unique request ID,
        and then proceeds to call the next request handler in the ASGI application chain. After
        receiving the response, it logs the response as well.

        Args:
            request: The incoming Request object to be logged and processed.
            call_next: A callable that takes the request and returns a response. This represents
                       the next middleware or endpoint in the processing chain.

        Returns:
            Response: The response object after processing the request and logging.
        """
        request.state.request_id = str(uuid4())
        logger = Logger(self.service_name, request)

        body = await self._get_request_body(request)
        serialized_body = self._serialize_data(body)

        logger.info(payload=serialized_body, message="client_received_request")

        response = await call_next(request)
        response = await self._log_response(request, response, logger)

        response.headers["request_id"] = request.state.request_id
        return response

    async def _get_request_body(self, request: Request):
        """
        Retrieves the body of the request in a serialized form.

        This method captures and returns the request body, handling different content types
        appropriately. For multipart/form-data content, a placeholder is returned instead of
        attempting to read the body directly.

        Args:
            request: The Request object from which the body is to be retrieved.

        Returns:
            The request body in a serialized form suitable for logging. For multipart/form-data,
            returns a placeholder dictionary.
        """
        content_type = request.headers.get("content-type", "").split(";")[0]
        if content_type and content_type != "multipart/form-data":
            await self._set_request_body(request)
            return await request.body()
        return None

    async def _log_response(self, request: Request, response: Response, logger: Logger):
        """
        Logs the outgoing response and modifies it to include the request ID in the headers.

        This method logs the response body and metadata. If an error occurs during the logging
        process, an error response is generated and logged instead.

        Args:
            request: The Request object associated with the response.
            response: The outgoing Response object to be logged.
            logger: The Logger instance used for logging the response.

        Returns:
            Response: The modified Response object, potentially with added error information
                      and the request ID in the headers.
        """
        try:
            response_body = [
                section async for section in response.__dict__["body_iterator"]
            ]
            response.__setattr__("body_iterator", AsyncIteratorWrapper(response_body))

            serialized_response_body = (
                self._serialize_data(response_body[0].decode())
                if response_body
                else None
            )
        except Exception as exception:
            serialized_response_body = {
                "errorCode": "InternalServerError",
                "message": "Something went wrong!",
                "detail": str(exception),
                "target": f"{request.method}|{request.url._url}",
            }
            response = JSONResponse(serialized_response_body, status_code=500)

        logger.info(payload=serialized_response_body, message="client_sent_response")
        return response

    def _serialize_data(self, data) -> str:
        """
        Serializes the given data to a JSON string, if possible.

        This helper method attempts to serialize the given data into a JSON string.
        If the data cannot be serialized (e.g., due to a JSONDecodeError), None is returned.

        Args:
            data: The data to be serialized.

        Returns:
            str or None: The serialized data as a JSON string, or None if serialization fails.
        """
        try:
            return json.loads(data) if data else None
        except json.JSONDecodeError:
            return None

    async def log_request(self, request: Request, call_next):
        """
        Public method to log the request and response.

        This method serves as the entry point for logging requests and their responses,
        delegating the actual logging to the `_log_request` method.

        Args:
            request: The incoming Request object to be logged.
            call_next: A callable that takes the request and returns a response. This represents
                       the next middleware or endpoint in the processing chain.

        Returns:
            Response: The response object after logging the request and response.
        """
        return await self._log_request(request, call_next)
