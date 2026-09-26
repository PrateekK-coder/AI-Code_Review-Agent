from app.models import code
from pathlib import Path
import subprocess
import shutil
from urllib.parse import urlparse

class GitHubRepositoryLoader:

   

    def clone(self, repo_url: str) -> Path:
        # 1. Validate the GitHub URL
        
        is_valid_github = False
        if repo_url.startswith("git@github.com:"):
            is_valid_github = True
        else:
            try:
                parsed = urlparse(repo_url)
                if parsed.scheme in ("http", "https") and parsed.netloc.lower() in ("github.com", "www.github.com"):
                    is_valid_github = True
            except Exception:
                is_valid_github = False
                
        if not is_valid_github:
            raise ValueError(f"Invalid URL: '{repo_url}' is not a valid GitHub repository URL.")

        # 2. Extract repo name

        repo_name = repo_url.rstrip("/").split("/")[-1]
        if repo_name.endswith(".git"):
            repo_name = repo_name[:-4]
            
        # 3. Setup directories

        base_dir = Path('app/data/repositories')
        base_dir.mkdir(parents=True, exist_ok=True)
        target_dir: Path = base_dir / repo_name

        # 4. Run git clone
        cmd = ["git", "clone", repo_url, str(target_dir)]
        
        try:
            subprocess.run(cmd, check=True, text=True, capture_output=True)
            print(f"Successfully cloned: {repo_url}")
        except subprocess.CalledProcessError as e:
            print(f"Failed to clone repository. Error:\n{e.stderr}")
            raise
                    
        return target_dir.resolve()
        
    def cleanup(self, repo_path: Path):
        if repo_path.exists():
            shutil.rmtree(repo_path)
            print(f"Cleaned up repository: {repo_path}")