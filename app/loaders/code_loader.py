from app.models import code
from pathlib import Path



EXTENSION_MAP = {
    ".py": "python",
    ".js": "javascript",
    ".ts": "typescript",
    ".java": "java",
    ".cpp": "cpp",
    ".c": "c",
    ".cs": "csharp",
    ".go": "go",
    ".rs": "rust",
    ".sql": "sql",
    ".kt":"kotlin"
}




def load_code(path:str) -> code.CodeFile:


    file_path=Path(path)
    with open(path, "r", encoding="utf-8") as file:
        c = file.read()

    language = EXTENSION_MAP.get(file_path.suffix.lower(), "text")
    return code.CodeFile( 
        file_name=file_path.name,
        file_path=str(file_path),
        language=language,
        content=c)