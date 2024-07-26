from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from contextlib import contextmanager
from src.repositories.environment_repository import EnvironmentRepository
from sqlalchemy.exc import SQLAlchemyError
from src.repositories.data_contracts import source

class Database:
    """
    Manages database connections, sessions, and operations such as creating tables and executing SQL scripts.
    """

    def __init__(self):
        """
        Initializes the DatabaseManager with a database engine, session factory, and base declarative class.
        """
        self.environment_repository = EnvironmentRepository()
        self.engine = create_engine(self.environment_repository.get_database_url())
        self.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)
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

    def create_tables(self):
        """
        Creates all tables defined in the source Base metadata.

        Uses:
            self.engine: The database engine bound to the metadata.
        """
        source.Base.metadata.create_all(bind=self.engine)

    def execute_sql_script(self, sql_script_path: str):
        """
        Executes an SQL script from the given file path.

        Args:
            sql_script_path (str): The file path to the SQL script.

        Raises:
            SQLAlchemyError: If a database error occurs during the script execution, the transaction is rolled back.
        """
        with open(sql_script_path, 'r') as file:
            sql_script = file.read()

        with self.engine.connect() as connection:
            try:
                connection.execute(sql_script)
            except SQLAlchemyError as e:
                connection.rollback()
