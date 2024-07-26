from http import HTTPMethod, HTTPStatus

from src.common.constants.controller import ControllerConstants
from fastapi import APIRouter
from src.models.health import HealthDto
from src.models.http_error import HTTPErrorDto

from src.services.source_service import SourceService


class HealthController:
    """
    Manages health checks for the service.

    This controller initializes an APIRouter and configures an endpoint to handle
    POST requests to get the health status of the service. The endpoint returns
    information about the service's health.

    Attributes:
        router (APIRouter): An APIRouter instance for routing HTTP requests.
    """

    def __init__(self):
        """
        Initializes the HealthController with API routing configurations.

        This constructor initializes the APIRouter and configures an API route for
        the health check endpoint. It specifies the request method, path, response
        models, and status codes for different responses.

        The endpoint is configured to respond with a `HealthDto` model on a successful
        request and an `HTTPErrorDto` model in case of an internal server error.
        """
        self.router = APIRouter()
        self.service = SourceService()

        self.router.add_api_route(
            path="",
            endpoint=self.get_health,
            methods=[HTTPMethod.GET],
            tags=[self.__class__.__name__],
            status_code=HTTPStatus.OK,
            responses={
                HTTPStatus.OK: {ControllerConstants.MODEL: HealthDto},
                HTTPStatus.INTERNAL_SERVER_ERROR: {
                    ControllerConstants.MODEL: HTTPErrorDto
                },
            },
            response_model=HealthDto,
            response_model_exclude_none=True,
            summary="Gets the service health",
        )

    async def get_health(self):
        """
        Asynchronously gets the service's health status.

        This method handles POST requests to the health check endpoint and returns
        the service's current health status. It creates and returns a `HealthDto`
        instance indicating the health status of the service.

        Returns:
            HealthDto: An instance of `HealthDto` indicating the health status of
            the service, with the `healthy` attribute set to True.
        """

        self.service.get_source(1)

        return HealthDto(healthy=True)
