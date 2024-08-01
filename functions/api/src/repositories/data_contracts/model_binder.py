from src.repositories.data_contracts import source
from src.utils.database import DatabaseManager


class ModelBinder:
    """
    Binds models to the database, handling table creation.

    Attributes:
        engine (Engine): The SQLAlchemy engine instance used for database operations.
    """

    def __init__(self) -> None:
        """
        Initializes the ModelBinder instance by setting up the database engine.
        """
        manager = DatabaseManager()
        self.engine = manager.engine

    def create_tables(self) -> None:
        """
        Creates all tables defined in the source Base metadata.

        Uses the engine to bind and create all tables defined in the SQLAlchemy
        Base metadata imported from the source module.
        """
        source.Base.metadata.create_all(bind=self.engine)
