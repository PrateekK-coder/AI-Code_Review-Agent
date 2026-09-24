from pathlib import Path
from app.loaders.code_loader import EXTENSION_MAP




class RepositoryScanner:

    def scan(self, repository_path: Path,) -> list[Path]:

        # 1. Validate repository path

        if not repository_path.exists() or not repository_path.is_dir():
            raise NotADirectoryError(
                f"The path '{repository_path}' is not a valid directory."
            )



        # 2. Find the file which are in our extension map
        
        matched_files = []


        for file_path in repository_path.rglob("*"):
            if not file_path.is_file():
                continue

            if file_path.suffix.lower() in EXTENSION_MAP:
                matched_files.append(file_path.resolve())


        # 3. Return discovered files
        
        return matched_files

