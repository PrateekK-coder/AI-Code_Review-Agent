from pydantic import BaseModel
from datetime import datetime


class IndexedRepository(BaseModel):
    repository_id: str
    github_url: str
    branch: str
    files_indexed: int
    chunks_indexed: int
    status: str
    indexed_at: datetime