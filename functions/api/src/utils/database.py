from contextlib import contextmanager

from sqlalchemy import create_engine
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from src.repositories.data_contracts import source
from src.repositories.environment_repository import EnvironmentRepository


class DatabaseManager:
    """
    Manages database connections, sessions, and operations such as creating tables and executing SQL scripts.
    """

    def __init__(self):
        """
        Initializes the DatabaseManager with a database engine, session factory, and base declarative class.
        """
        self.environment_repository = EnvironmentRepository()
        self.engine = create_engine(self.environment_repository.get_database_url())
        self.SessionLocal = sessionmaker(
            autocommit=False, autoflush=False, bind=self.engine
        )
        self.Base = declarative_base()

    @contextmanager
    def get_database_session(self):
        """
        Provides a transactional scope around a series of operations.

        Yields:
            Session: A SQLAlchemy session object.

        Raises:
            SQLAlchemyError: If a database error occurs, the transaction is rolled back and the error is raised.
        """
        session = self.SessionLocal()
        try:
            yield session
        except SQLAlchemyError as e:
            session.rollback()
            raise e
        finally:
            session.close()
