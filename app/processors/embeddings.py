
from langchain_openai import OpenAIEmbeddings
from langchain_core.documents import Document



# This is redundant code now as now we are doing the samething in the vector_stores/chroma_store.py file there we are letting the chromaDb to do the embeddings for us 
# This class is for the learning purpose like we were checking that either our OpenAI is able to create the embeddings of our chunks or not


class CodeEmbedding:

    def __init__(self):
        self.embedding = OpenAIEmbeddings(
            model="text-embedding-3-small"
        )

    def docs_to_vec(self, documents: list[Document]):

        texts = []
    
   
        for document in documents:
    
            code_text = document.page_content
  
            texts.append(code_text)

   
        return self.embedding.embed_documents(texts)

