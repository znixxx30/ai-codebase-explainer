import os
from git import Repo
from app.core.config import settings


class RepoService:

    def __init__(self):
        self.repo_storage = settings.REPO_STORAGE

        os.makedirs(self.repo_storage, exist_ok=True)

    def clone_repository(self, repo_url: str) -> str:

        repo_name = repo_url.rstrip("/").split("/")[-1]

        repo_path = os.path.join(self.repo_storage, repo_name)

        if os.path.exists(repo_path):
            return repo_path

        Repo.clone_from(repo_url, repo_path)

        return repo_path