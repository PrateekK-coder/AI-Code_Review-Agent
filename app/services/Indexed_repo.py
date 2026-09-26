from datetime import datetime
from app.models.indexed_repository_model import IndexedRepository


class IndexedRepositoryService:

    def __init__(self):
        self.repositories = {}
        self.repository_code_files = {}

    def register_repository(
        self,
        github_url: str,
        branch: str,
        files_indexed: int,
        chunks_indexed: int,
        code_files
    ):

        repository_id = f"repo_{len(self.repositories) + 1}"

        repository = IndexedRepository(
            repository_id=repository_id,
            github_url=github_url,
            branch=branch,
            files_indexed=files_indexed,
            chunks_indexed=chunks_indexed,
            status="indexed",
            indexed_at=datetime.now()
        )
        

        self.repositories[repository_id] = repository
        self.repository_code_files[repository_id] = code_files

        return repository

    def get_repository(self, repository_id: str):

        return self.repositories.get(repository_id)

    def get_code_files(self, repository_id: str):

        return self.repository_code_files.get(
            repository_id,
            []
        )