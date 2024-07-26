from src.repositories.source_repository import SourceRepository

class SourceService:
    def __init__(self) -> None:
        self.repository = SourceRepository()

    def get_source(self, id: int):
        entity = self.repository.get_source(id=id)
        print(entity)