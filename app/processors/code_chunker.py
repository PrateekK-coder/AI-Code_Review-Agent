from langchain_core.documents import Document
from app.models.code import CodeFile
from langchain_text_splitters import RecursiveCharacterTextSplitter, Language


LANGUAGE_MAP = {
    "python": Language.PYTHON,
    "javascript": Language.JS,
    "typescript": Language.TS,
    "java": Language.JAVA,
    "cpp": Language.CPP,
    "c": Language.C,
    "csharp": Language.CSHARP,
    "go": Language.GO,
    "rust": Language.RUST,
    "kotlin":Language.KOTLIN
  # "sql": Language.SQL,   Not supported in Langchain 
}


class CodeChunker: 
    def convert_to_document(self, code_file: CodeFile) -> Document:
        return Document(
            page_content=code_file.content,
            metadata={
                "file_name": code_file.file_name,
                "file_path": code_file.file_path,
                "language": code_file.language,
            }
        )

    def code_splitter(self, document: Document) ->list[Document]:


        language = document.metadata.get("language")

        if language in LANGUAGE_MAP:
            splitter = RecursiveCharacterTextSplitter.from_language(
                language=LANGUAGE_MAP[language],
                chunk_size=500,
                chunk_overlap=0
            )
        else:
            splitter = RecursiveCharacterTextSplitter(
                chunk_size=500,
                chunk_overlap=0
            )   
        
        chunks = splitter.split_documents([document])
        return chunks


