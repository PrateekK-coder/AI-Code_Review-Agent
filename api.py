from fastapi import FastAPI, UploadFile, File, HTTPException
from pathlib import Path
import tempfile
from pydantic import BaseModel
from typing import Literal
from app.services.repository_review_service import RepositoryReviewService
from app.services.file_review_service import FileReviewService
from app.models.review import CodeReview
from app.loaders import code_loader
from app.services.repository_index_service import RepositoryIndexService
from app.services.Indexed_repo import IndexedRepositoryService
from app.services.semantic_review_service import SemanticReviewService

app = FastAPI(
    title="AI Code Review Agent API",
    description="Backend API for the AI-powered code review system",
    version="1.0.0"
)

repository_service = RepositoryReviewService()
file_service = FileReviewService()
repository_registry = IndexedRepositoryService()

index_service = RepositoryIndexService(
    repository_registry=repository_registry
)

semantic_service = SemanticReviewService(
    repository_registry=repository_registry
)

class RepositoryReviewRequest(BaseModel):
    github_url:str
    branch:str= "main"


class IssueResponse(BaseModel):
    category: Literal[
        "BUG",
        "SECURITY",
        "QUALITY",
        "PERFORMANCE"
    ]

    severity: Literal[
        "CRITICAL",
        "HIGH",
        "MEDIUM",
        "LOW"
    ]

    file: str
    line: int | None = None
    description: str
    recommendation: str

class RepositoryReviewResponse(BaseModel):
    files_reviewed: int
    total_issues: int
    severity_counts: dict[str, int]
    issues: list[IssueResponse]



class FileReviewResponse(BaseModel):
      summary: str

      overall_severity: Literal[
        "CRITICAL",
        "HIGH",
        "MEDIUM",
        "LOW"
    ]
      issues: list[IssueResponse]
      testing_recommendations: list[str]

class RepositoryIndexRequest(BaseModel):

    github_url: str
    branch: str = "main"

class RepositoryIndexResponse(BaseModel):

    repository_id: str
    files_indexed: int
    chunks_indexed: int
    status: str


class SemanticReviewRequest(BaseModel):
    repository_id: str
    query: str
    k: int = 5

class SemanticReviewResponse(BaseModel):
    reviews: list[CodeReview]


@app.get("/")
def root():
    return {
        "message": "AI Code Review Agent API is running"
    }

@app.post(
    "/api/v1/reviews/repository",
    response_model=RepositoryReviewResponse
)
def review_repository(request: RepositoryReviewRequest):

    result = repository_service.review_repository(
        github_url=request.github_url,
        branch=request.branch
    )

    return result

@app.post(
    "/api/v1/reviews/file",
    response_model=FileReviewResponse
)
async def review_file(file: UploadFile = File(...)):

    temp_path = None

    try:

        # 1. Create temporary file
        suffix = Path(file.filename).suffix

        with tempfile.NamedTemporaryFile(
            delete=False,
            suffix=suffix
        ) as temp_file:

            temp_path = Path(temp_file.name)

            content = await file.read()

            temp_file.write(content)

        # 2. Load file using our existing loader
        code_file = code_loader.load_code(temp_path)
         # Preserve original filename
        code_file.file_name = file.filename
        code_file.file_path = file.filename

        # 3. Send CodeFile to review service
        review = file_service.review_file(
            code_file
        )

        # 4. Return review
        return review

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )

    finally:

        # 5. Delete temporary file
        if temp_path and temp_path.exists():
            temp_path.unlink()


@app.post("/api/v1/repositories/index",response_model=RepositoryIndexResponse)
def index_repository(request: RepositoryIndexRequest):

    result = index_service.index_repository(
        github_url=request.github_url,
        branch=request.branch
    )

    return result


@app.get("/api/v1/repositories/{repository_id}")
def get_repository(repository_id: str):

    repository = repository_registry.get_repository(
        repository_id
    )

    if repository is None:
        return {
            "error": "Repository not found"
        }

    return repository




@app.post(
    "/api/v1/reviews/semantic",
    response_model=SemanticReviewResponse
)
def semantic_review(request: SemanticReviewRequest):

    reviews = semantic_service.review(
        repository_id=request.repository_id,
        query=request.query,
        k=request.k
    )

    return {
        "reviews": reviews
    }