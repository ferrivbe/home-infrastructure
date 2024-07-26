from sqlalchemy import Column, Integer, String
from src.utils.database import DatabaseManager

db_manager = DatabaseManager()
Base = db_manager.Base

class Source(Base):
    __tablename__ = 'source'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String, index=True)
