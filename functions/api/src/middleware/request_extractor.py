import re

from src.common.error.http import HTTPNotFoundError
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.types import ASGIApp


class RequestExtractorMiddleware(BaseHTTPMiddleware):
    """
    Middleware for extracting the application ID from the request URL's hostname and validating it.

    This middleware checks if the request hostname contains a valid application ID as its subdomain
    formatted as `{id}.{api_host}`. It only allows requests with valid IDs or requests to certain
    predefined endpoints to proceed.

    Attributes:
        api_host (str): The expected API host domain which requests must match.
        pattern (re.Pattern): Compiled regular expression to extract the ID from the hostname.
        allowed_endpoints (List[str]): A list of endpoints that do not require application ID validation.

    Methods:
        __init__(self, app: ASGIApp, api_host: str)
            Initializes the middleware with the application instance and the API host.
        dispatch(self, request: Request, call_next)
            Processes each request, validates the application ID, or allows predefined endpoints.
    """

    def __init__(self, app: ASGIApp, api_host: str):
        """
        Initializes the middleware with the given ASGI application and the expected API host.

        Args:
            app (ASGIApp): The ASGI application instance that this middleware wraps.
            api_host (str): The expected API host for extracting the application ID from the hostname.

        Raises:
            ValueError: If the api_host is not a valid hostname.
        """
        super().__init__(app)
        self.api_host = api_host
        self.pattern = re.compile(rf"^(?P<id>[^.]+)\.{re.escape(api_host)}$")
        self.allowed_endpoints = [
            "/health",
            "/service",
            "/docs",
            "/openapi.json",
        ]

    async def dispatch(self, request: Request, call_next):
        """
        Process the incoming request and validate its hostname for a proper application ID.

        This method checks if the request URL path is one of the allowed endpoints. If not, it tries
        to extract and validate the application ID from the hostname using a precompiled regex pattern.
        If the ID is invalid or missing where required, it raises an HTTPException.

        Args:
            request (Request): The incoming HTTP request to process.
            call_next: The next callable to proceed with the request handling.

        Returns:
            Response: The HTTP response object after processing the request or handling exceptions.

        Raises:
            HTTPException: If the hostname does not contain a valid application ID.
        """
        if request.url.path not in self.allowed_endpoints:
            hostname = request.url.hostname
            match = self.pattern.match(hostname)

            if not match:
                raise HTTPNotFoundError(
                    error_code="ApplicationMissing",
                    message="Application id not found.",
                )

            application_id = match.group("id")

            request.state.id = application_id

        response = await call_next(request)
        return response
