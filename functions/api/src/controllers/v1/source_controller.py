from http import HTTPMethod, HTTPStatus
from uuid import UUID

from fastapi import APIRouter, Depends
from src.common.constants.controller import ControllerConstants
from src.models.http_error import HTTPErrorDto
from src.models.source import NewSourceDto, SourceDto
from src.services.source_service import SourceService


class SourceController:
    """
    Controller class for handling source-related API endpoints.
    """

    def __init__(self):
        """
        Initializes the SourceController with a router and a service.
        """

        self.router = APIRouter()
        self.service = SourceService()

        self.router.add_api_route(
            path="",
            endpoint=self.create_source,
            methods=[HTTPMethod.POST],
            tags=[self.__class__.__name__],
            status_code=HTTPStatus.CREATED,
            responses={
                HTTPStatus.OK: {ControllerConstants.MODEL: SourceDto},
                HTTPStatus.UNPROCESSABLE_ENTITY: {
                    ControllerConstants.MODEL: HTTPErrorDto
                },
                HTTPStatus.INTERNAL_SERVER_ERROR: {
                    ControllerConstants.MODEL: HTTPErrorDto
                },
            },
            response_model=SourceDto,
            response_model_exclude_none=True,
            summary="Creates a new source.",
        )

        self.router.add_api_route(
            path="",
            endpoint=self.get_sources,
            methods=[HTTPMethod.GET],
            tags=[self.__class__.__name__],
            status_code=HTTPStatus.OK,
            responses={
                HTTPStatus.OK: {ControllerConstants.MODEL: list[SourceDto]},
                HTTPStatus.NOT_FOUND: {ControllerConstants.MODEL: HTTPErrorDto},
                HTTPStatus.INTERNAL_SERVER_ERROR: {
                    ControllerConstants.MODEL: HTTPErrorDto
                },
            },
            response_model=list[SourceDto],
            response_model_exclude_none=True,
            summary="Gets all sources.",
        )

        self.router.add_api_route(
            path="/{id}",
            endpoint=self.get_source_by_id,
            methods=[HTTPMethod.GET],
            tags=[self.__class__.__name__],
            status_code=HTTPStatus.OK,
            responses={
                HTTPStatus.OK: {ControllerConstants.MODEL: SourceDto},
                HTTPStatus.NOT_FOUND: {ControllerConstants.MODEL: HTTPErrorDto},
                HTTPStatus.INTERNAL_SERVER_ERROR: {
                    ControllerConstants.MODEL: HTTPErrorDto
                },
            },
            response_model=SourceDto,
            response_model_exclude_none=True,
            summary="Gets the source by identifier.",
        )

        self.router.add_api_route(
            path="/{id}",
            endpoint=self.update_source,
            methods=[HTTPMethod.PUT],
            tags=[self.__class__.__name__],
            status_code=HTTPStatus.OK,
            responses={
                HTTPStatus.OK: {ControllerConstants.MODEL: SourceDto},
                HTTPStatus.UNPROCESSABLE_ENTITY: {
                    ControllerConstants.MODEL: HTTPErrorDto
                },
                HTTPStatus.NOT_FOUND: {ControllerConstants.MODEL: HTTPErrorDto},
                HTTPStatus.INTERNAL_SERVER_ERROR: {
                    ControllerConstants.MODEL: HTTPErrorDto
                },
            },
            response_model=SourceDto,
            response_model_exclude_none=True,
            summary="Updates an existing source by identifier.",
        )

    def create_source(self, source: NewSourceDto) -> SourceDto:
        """
        Creates a new source using the provided data.

        Args:
            source (NewSourceDto): The data transfer object containing information about the new source.

        Returns:
            SourceDto: The data transfer object representing the created source.
        """

        return self.service.create_source(entity=source)

    def get_source_by_id(self, id: UUID) -> SourceDto:
        """
        Gets a source by its UUID.

        Args:
            id (UUID): The unique identifier of the source to retrieve.

        Returns:
            SourceDto: The data transfer object representing the source.

        Raises:
            NotFoundException: If the source with the given ID does not exist.
        """

        return self.service.get_source_by_id(id=id)

    def get_sources(self) -> list[SourceDto]:
        """
        Gets a list of all sources.

        Returns:
            list[SourceDto]: A list of data transfer objects representing the sources.
        """

        return self.service.get_sources()

    def update_source(self, id: UUID, source: NewSourceDto) -> SourceDto:
        """
        Updates an existing source using the provided data.

        Args:
            id (UUID): The unique identifier of the source to update.
            source (NewSourceDto): The data transfer object containing updated information about the source.

        Returns:
            SourceDto: The data transfer object representing the updated source.
        """

        return self.service.update_source(id=id, updated_source=source)
