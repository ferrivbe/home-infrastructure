import uuid

from sqlalchemy import Column, Integer, String
from sqlalchemy.dialects.postgresql import UUID as PGUUID
from src.utils.database import DatabaseManager

db_manager = DatabaseManager()
Base = db_manager.Base


class Source(Base):
    """
    Represents a source entity in the database.

    Attributes:
        id (UUID): The primary key, a universally unique identifier (UUID).
        name (str): The name of the source, up to 32 characters. This field is indexed.
        description (str, optional): A brief description of the source, up to 128 characters. This field is indexed.
        address (str): The address associated with the source, up to 15 characters.
        port (int): The port number for the source.
        username (str): The username for accessing the source, up to 128 characters.
        password (str): The password for accessing the source, up to 128 characters.
        protocol (str): The protocol used by the source, up to 12 characters.
    """

    __tablename__ = "source"

    id = Column(PGUUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    name = Column(String(32), nullable=False, index=True)
    description = Column(String(128), nullable=True, index=True)
    address = Column(String(15), nullable=False)
    port = Column(Integer, nullable=False)
    username = Column(String(128), nullable=False)
    password = Column(String(128), nullable=False)
    protocol = Column(String(12), nullable=False)
