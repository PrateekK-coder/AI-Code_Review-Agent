class SemanticReviewer:
    def __init__(self, code_reviewer, vector_store, code_files):
        self.code_reviewer = code_reviewer
        self.vector_store = vector_store
        self.code_files = code_files


    def search(self, query, k=5):

        results = self.vector_store.search(
        query=query,
        k=k
    )

        return results


    def group_chunks_by_file(self, chunks):

        file_chunks = {}

        for chunk in chunks:

            file_path = chunk.metadata["file_path"]

            if file_path not in file_chunks:
                file_chunks[file_path] = []

            file_chunks[file_path].append(chunk)

        return file_chunks


    def get_code_file(self, file_path):

        for code_file in self.code_files:

            if code_file.file_path == file_path:
                return code_file

        return None


    def retrieve_relevant_files(self, query, k=5):

        chunks = self.search(query, k)

        file_chunks = self.group_chunks_by_file(chunks)

        relevant_files = []

        for file_path in file_chunks:

            code_file = self.get_code_file(file_path)

            if code_file:
                relevant_files.append(
                    (code_file, file_chunks[file_path])
                )

        return relevant_files


    def review(self, query, k=5):

        relevant_files = self.retrieve_relevant_files(
            query,
            k
        )

        reviews = []

        for code_file, chunks in relevant_files:

            code = "\n\n".join(
                chunk.page_content
                for chunk in chunks
            )

            review = self.code_reviewer.review_semantic(
                query=query,
                code_file=code_file,
                code=code
            )

            reviews.append(review)

        return reviews