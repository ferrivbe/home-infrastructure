from typing import Union

from src.common.error.http import HTTPError
from fastapi import Request
from fastapi.exceptions import HTTPException, RequestValidationError
from fastapi.responses import JSONResponse
from src.utils.logger import Logger


async def exception_handler(request: Request, exception: HTTPError) -> JSONResponse:
    """
    Handles custom HTTP errors, logging the error details and returning a JSON response.

    Args:
        request (Request): The request that led to the exception.
        exception (HTTPError): The custom HTTP error thrown by the application.

    Returns:
        JSONResponse: The response object with error details and the corresponding HTTP status code.
    """
    response = {
        "error_code": exception.error_code,
        "message": exception.message,
        "detail": exception.detail,
        "target": f"{request.method}|{request.url.path}",
    }

    Logger(service_name="home-infrastructure", request=request).error(response)
    return JSONResponse(content=response, status_code=exception.http_status)


async def default_exception_handler(
    request: Request, exception: HTTPException
) -> JSONResponse:
    """
    Handles generic HTTP exceptions, logging and returning a standardized error response.

    Args:
        request (Request): The incoming request.
        exception (HTTPException): The FastAPI HTTP exception.

    Returns:
        JSONResponse: A response with a generic error message and the exception's status code.
    """
    response = {
        "error_code": "GenericExceptionRaised",
        "message": "Something went wrong inside a process.",
        "detail": str(exception.detail),
        "target": f"{request.method}|{request.url.path}",
    }

    Logger(service_name="home-infrastructure", request=request).error(response)
    return JSONResponse(content=response, status_code=exception.status_code)


async def python_exception_handler(
    request: Request, exception: Exception
) -> JSONResponse:
    """
    Handles unexpected Python exceptions, returning an internal server error response.

    Args:
        request (Request): The request during which the exception occurred.
        exception (Exception | ValueError): The caught exception.

    Returns:
        JSONResponse: A response indicating an internal server error.
    """
    response = {
        "error_code": "InternalServerError",
        "message": "Something went wrong!",
        "detail": str(exception),
        "target": f"{request.method}|{request.url.path}",
    }

    Logger(service_name="home-infrastructure", request=request).error(response)
    return JSONResponse(content=response, status_code=500)


async def request_validation_error_handler(
    request: Request, exception: RequestValidationError
) -> JSONResponse:
    """
    Handles validation errors for incoming requests, logging and returning a detailed error response.

    Args:
        request (Request): The request with validation errors.
        exception (RequestValidationError): The validation error object from FastAPI.

    Returns:
        JSONResponse: A response detailing the validation errors with a 400 status code.
    """
    response = {
        "error_code": "RequestValidationError",
        "message": "There are errors in the request.",
        "detail": exception.errors(),
        "target": f"{request.method}|{request.url.path}",
    }

    Logger(service_name="home-infrastructure", request=request).error(response)
    return JSONResponse(content=response, status_code=400)
