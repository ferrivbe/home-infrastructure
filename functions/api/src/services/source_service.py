from uuid import UUID, uuid4

from src.common.constants.entity_type import EntityType
from src.models.mappers.source_mapper import SourceMapper
from src.models.source import NewSourceDto, SourceDto
from src.repositories.data_contracts.source import Source
from src.repositories.source_repository import SourceRepository
from src.services.extensions.request_extensions import RequestExtensions


class SourceService:
    """
    Service class for managing sources.
    """

    def __init__(self) -> None:
        """
        Initializes the SourceService with a SourceRepository instance.
        """

        self.repository = SourceRepository()

    def create_source(self, entity: NewSourceDto) -> SourceDto:
        """
        Creates a new source and returns its DTO representation.

        Args:
            entity (NewSourceDto): The data transfer object containing information about the new source.

        Returns:
            SourceDto: The data transfer object representing the created source.
        """

        id = uuid4()
        source = SourceMapper.to_repository(entity=entity, id=id)
        created_source = self.repository.create_source(source=source)

        return SourceMapper.to_dto(created_source)

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

        entity = self._get_source_by_id(id=id)

        return SourceMapper.to_dto(entity)

    def get_sources(self) -> list[SourceDto]:
        """
        Gets a list of all sources.

        Returns:
            list[SourceDto]: A list of data transfer objects representing the sources.
        """

        entities = self.repository.get_all_sources()

        return [SourceMapper.to_dto(entity) for entity in entities]

    def update_source(self, id: UUID, updated_source: SourceDto) -> SourceDto:
        """
        Updates an existing source and returns its updated DTO representation.

        Args:
            id (UUID): The unique identifier of the source to update.
            updated_source (SourceDto): The data transfer object containing updated information about the source.

        Returns:
            SourceDto: The data transfer object representing the updated source.

        Raises:
            NotFoundException: If the source with the given ID does not exist.
        """

        self._get_source_by_id(id=id)

        new_source = SourceMapper.to_repository(entity=updated_source, id=id)
        updated_entity = self.repository.update_source(id=id, new_source=new_source)

        RequestExtensions.raise_if_not_found(
            entity=updated_entity, id=id, type=EntityType.SOURCE
        )

        return SourceMapper.to_dto(updated_entity)

    def _get_source_by_id(self, id: UUID):
        """
        Gets the source by identifier.
        """

        entity: Source = self.repository.get_source(id=id)
        RequestExtensions.raise_if_not_found(
            entity=entity, id=id, type=EntityType.SOURCE
        )

        return entity
