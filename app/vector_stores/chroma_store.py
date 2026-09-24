from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings
class ChromaStore:
     def __init__(self):
        self.embeddings = OpenAIEmbeddings(
            model="text-embedding-3-small"
        )
        self.vector_store=Chroma(
            collection_name = "code_review",# table name which is made inside the chroma db is code-review
            embedding_function=self.embeddings, # we are letting the chromadb handle the embedding by self.embeddings method which is OpenAIEmbeddings
            persist_directory="app/data/chroma_db" # Directory where our vector will be stored locally 
        )

     def add_documents(self, documents):
        self.vector_store.add_documents(documents)

     def count(self):
      return self.vector_store._collection.count()

     def search(self, query: str, k: int = 3):
      return self.vector_store.similarity_search(query,k=k)


     def search_context(self, query: str, current_chunk, k: int = 3):

         results = self.vector_store.similarity_search(query,k=k + 1)

         context_chunks = []

         for result in results:

            if (result.page_content == current_chunk.page_content and result.metadata == current_chunk.metadata):
               continue

            context_chunks.append(result)

            if len(context_chunks) == k: 
               break

         return context_chunks 

     def search_file_context(self,file_code: str,current_file_path: str,k: int = 5):

         query = f"""
Find code from other files that is relevant to reviewing this file.

Focus on:
- imported modules
- functions or classes used by this file
- shared utilities
- configuration dependencies
- database models or database operations
- APIs or services used
- related business logic

Current file:

{file_code}
"""
         results = self.vector_store.similarity_search(query,k=k + 10)

         context_chunks = []

         for result in results:

            if result.metadata.get("file_path") == current_file_path:
               continue

            context_chunks.append(result)

            if len(context_chunks) == k:
               break

         return context_chunks



     def get_file_chunks(self, file_path):

         result = self.vector_store._collection.get(
            where={"file_path": file_path}
         )

         return result

   