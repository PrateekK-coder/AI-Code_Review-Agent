from app.agents.semantic_reviewer import SemanticReviewer
from app.agents.code_reviewer import CodeReviewer
from app.vector_stores.chroma_store import ChromaStore


class SemanticReviewService:

    def __init__(self, repository_registry):

        self.repository_registry = repository_registry
        self.code_reviewer = CodeReviewer()
        self.vector_store = ChromaStore()

    def review(
        self,
        repository_id: str,
        query: str,
        k: int = 5
    ):

        # Get the repository metadata
        repository = self.repository_registry.get_repository(
            repository_id
        )

        if repository is None:
            raise ValueError(
                f"Repository '{repository_id}' is not indexed."
            )

        # Get the CodeFile objects belonging to this repository
        code_files = self.repository_registry.get_code_files(
            repository_id
        )

        if not code_files:
            raise ValueError(
                f"No code files found for repository '{repository_id}'."
            )

        # Create semantic reviewer
        semantic_reviewer = SemanticReviewer(
            code_reviewer=self.code_reviewer,
            vector_store=self.vector_store,
            code_files=code_files
        )

        # Perform semantic review
        reviews = semantic_reviewer.review(
            query=query,
            k=k
        )

        return reviews