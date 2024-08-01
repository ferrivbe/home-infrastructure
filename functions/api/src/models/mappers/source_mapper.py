from uuid import UUID

from src.models.source import NewSourceDto, ProtocolTypeDto, SourceDto
from src.repositories.data_contracts.source import Source


class SourceMapper:
    """
    Maps between SourceDto and Source entities.
    """

    def to_dto(entity: Source) -> SourceDto:
        """
        Converts a Source entity to a SourceDto.

        Args:
            entity (Source): The Source entity to convert.

        Returns:
            SourceDto: The converted SourceDto.

        Example:
            source = Source(
                id="123",
                name="Example Source",
                description="Description of source",
                address="192.168.1.1",
                port=22,
                username="user",
                password="pass",
                protocol="SSH"
            )
            source_dto = SourceMapper().to_dto(source)
        """
        return SourceDto(
            id=entity.id,
            name=entity.name,
            description=entity.description,
            address=entity.address,
            port=entity.port,
            username=entity.username,
            password=entity.password,
            protocol=ProtocolTypeDto(entity.protocol),
        )

    def to_repository(entity: NewSourceDto, id: UUID) -> Source:
        """
        Converts a SourceDto to a Source entity.

        Args:
            entity (SourceDto): The SourceDto to convert.

        Returns:
            Source: The converted Source entity.

        Example:
            source_dto = SourceDto(
                id=123,
                name="Example Source DTO",
                description="Description of source DTO",
                address="192.168.1.1",
                port=22,
                username="user",
                password="pass",
                protocol=ProtocolTypeDto("SSH")
            )
            source = SourceMapper().to_repository(source_dto)
        """
        return Source(
            id=str(id),
            name=entity.name,
            description=entity.description,
            address=entity.address,
            port=entity.port,
            username=entity.username,
            password=entity.password,
            protocol=entity.protocol.value,
        )
