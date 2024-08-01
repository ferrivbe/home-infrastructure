import uuid

from sqlalchemy import update
from src.repositories.data_contracts.source import Source
from src.utils.database import DatabaseManager


class SourceRepository:
    """
    Repository class for handling CRUD operations for the Source model.

    Attributes:
        db_manager (DatabaseManager): An instance of DatabaseManager to handle database sessions.
    """

    def __init__(self):
        """
        Initializes the SourceRepository with a DatabaseManager instance.
        """

        self.db_manager = DatabaseManager()

    def get_all_sources(self):
        """
        Retrieves all sources from the database.

        Returns:
            List[Source]: A list of Source objects retrieved from the database.
        """

        with self.db_manager.get_database_session() as session:
            return session.query(Source).all()

    def create_source(self, source: Source):
        """
        Creates a new source in the database.

        Args:
            source (Source): The Source object to be added to the database.

        Returns:
            Source: The newly created Source object with updated fields.
        """

        with self.db_manager.get_database_session() as session:
            session.add(source)
            session.commit()
            session.refresh(source)
            return source

    def get_source(self, id: uuid.UUID):
        """
        Retrieves a source by its ID.

        Args:
            id (uuid.UUID): The UUID of the Source to be retrieved.

        Returns:
            Source: The Source object if found, otherwise None.
        """

        with self.db_manager.get_database_session() as session:
            return session.query(Source).filter(Source.id == id).first()

    def update_source(self, id: uuid.UUID, new_source: Source):
        """
        Updates an existing source in the database with new values.

        Args:
            id (uuid.UUID): The UUID of the Source to be updated.
            new_source (Source): The Source object with new values.

        Returns:
            Source: The updated Source object if found and updated.
        """

        with self.db_manager.get_database_session() as session:
            session.query(Source).filter_by(id=id).update(
                {
                    attr: value
                    for attr, value in vars(new_source).items()
                    if attr != "id"
                    and attr != "_sa_instance_state"
                    and value is not None
                }
            )
            session.commit()

            return new_source
