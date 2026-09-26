from app.loaders.github_loader import GitHubRepositoryLoader
from app.loaders.repository_scanner import RepositoryScanner
from app.loaders import code_loader
from app.processors.code_chunker import CodeChunker
from app.vector_stores.chroma_store import ChromaStore
from app.services.Indexed_repo import IndexedRepositoryService


class RepositoryIndexService:

    def __init__(self, repository_registry):
        self.repository_registry = repository_registry

    def index_repository(
        self,
        github_url: str,
        branch: str = "main"
    ):

        # 1. Clone repository
        loader = GitHubRepositoryLoader()

        repo_path = loader.clone(
            github_url
        )

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

        # return {
        #     "files_indexed": len(code_files),
        #     "chunks_indexed": len(all_chunks),
        #     "status": "indexed"
        # }


        repository = self.repository_registry.register_repository(
        github_url=github_url,
        branch=branch,
        files_indexed=len(code_files),
        chunks_indexed=len(all_chunks),
        code_files=code_files
    )
        return repository