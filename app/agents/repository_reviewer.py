from app.agents.code_reviewer import CodeReviewer
from app.processors.dependency_extractor import DependencyExtractor
from app.processors.dependency_resolver import DependencyResolver

class RepositoryReviewer:

    def __init__(self, code_reviewer, vector_store,code_files):
        self.code_reviewer = code_reviewer
        self.vector_store = vector_store

        self.dependency_extractor = DependencyExtractor()
        self.dependency_resolver = DependencyResolver(code_files)    
        

    def review_repository(self, code_files, chunks):

        # Group chunks by file
        file_chunks = {}

        for chunk in chunks:

            file_path = chunk.metadata["file_path"]

            if file_path not in file_chunks:
                file_chunks[file_path] = []

            file_chunks[file_path].append(chunk)

        reviews = []

        # Review one file at a time
        total_files = len(file_chunks)

        for index, (file_path, chunks_for_file) in enumerate(
            file_chunks.items(), start=1
            ):
            print(f"Reviewing file {index}/{total_files}: {file_path}")

            # Find the CodeFile object
            code_file = next(
                code_file
                for code_file in code_files
                if code_file.file_path == file_path
            )

            # Combine all chunks belonging to this file
            file_code = "\n\n".join(
                chunk.page_content
                for chunk in chunks_for_file
            )
            dependencies = self.dependency_extractor.extract_python_imports(
            file_code
            )
            resolved_dependencies = []

            for dependency in dependencies:

                resolved_file = self.dependency_resolver.resolve_python_import(
                dependency
                )

                if resolved_file:
                    resolved_dependencies.append(resolved_file)            


            dependency_context_chunks = []

            for dependency_file in resolved_dependencies:

                result = self.vector_store.get_file_chunks(
                    dependency_file.file_path
                )

                for content in result["documents"]:
                    dependency_context_chunks.append(content)



            # Retrieve related chunks from OTHER files
            context_chunks = self.vector_store.search_file_context(
                file_code=file_code,
                current_file_path=file_path,
                k=5
            )

          
            semantic_context = "\n\n".join(
                chunk.page_content
                for chunk in context_chunks
            )

            dependency_context = "\n\n".join(
                dependency_context_chunks
            )

            context = "\n\n".join(
                [
                    dependency_context,
                    semantic_context
                ]
            )

            # Review the complete file + repository context
            review = self.code_reviewer.review(
                code_file=code_file,
                code=file_code,
                context=context
            )

            reviews.append(review)

        return reviews