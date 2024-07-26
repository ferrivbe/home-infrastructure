from sqlalchemy.orm import Session
from src.repositories.data_contracts.source import Source
from src.utils.database import DatabaseManager

class SourceRepository:
    def __init__(self):
        self.db_manager = DatabaseManager()

    def get_source(self, id: int):
        with self.db_manager.get_database_session() as session:
            return session.query(Source).filter(Source.id == id).first()
