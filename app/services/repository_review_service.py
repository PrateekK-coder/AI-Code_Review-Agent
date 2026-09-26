from app.loaders.github_loader import GitHubRepositoryLoader
from app.loaders.repository_scanner import RepositoryScanner
from app.loaders import code_loader

from app.processors.code_chunker import CodeChunker

from app.vector_stores.chroma_store import ChromaStore

from app.agents.code_reviewer import CodeReviewer
from app.agents.repository_reviewer import RepositoryReviewer
from app.agents.review_aggregator import ReviewAgentAggregator


class RepositoryReviewService:

    def review_repository(
        self,
        github_url: str,
        branch: str = "main"
    ):

        # 1. Clone repository
        loader = GitHubRepositoryLoader()

        repo_path = loader.clone(
            github_url
        )

        try:
            # 2. Scan repository
            scanner = RepositoryScanner()

            files = scanner.scan(repo_path)

            print("Code files found:", len(files))

            # 3. Load all code files
            code_files = []

            for file in files:

                code_file = code_loader.load_code(file)

                code_files.append(code_file)

            print("CodeFiles loaded:", len(code_files))

            # 4. Chunk all code
            chunker = CodeChunker()

            all_chunks = []

            for code_file in code_files:

                document = chunker.convert_to_document(
                    code_file
                )

                chunks = chunker.code_splitter(
                    document
                )

                all_chunks.extend(chunks)

            print("Total chunks:", len(all_chunks))

            # 5. Store chunks in ChromaDB
            store = ChromaStore()

            store.add_documents(
                all_chunks
            )

            print(
                "Stored documents:",
                store.count()
            )

            # 6. Repository review
            code_reviewer = CodeReviewer()

            repository_reviewer = RepositoryReviewer(
                code_reviewer=code_reviewer,
                vector_store=store,
                code_files=code_files
            )

            reviews = repository_reviewer.review_repository(
                code_files=code_files,
                chunks=all_chunks
            )

            # 7. Aggregate results
            aggregator = ReviewAgentAggregator()

            final_result = aggregator.aggregate(
                reviews
            )

            return final_result

        finally:
            loader.cleanup(repo_path)