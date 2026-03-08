import os


class ParserService:

    SUPPORTED_EXTENSIONS = (
        # Python / AI
        ".py", ".ipynb",

        # Web
        ".js", ".ts", ".jsx", ".tsx",
        ".html", ".css", ".scss",

        # Backend
        ".java", ".go", ".rs", ".cpp", ".c",
        ".cs", ".php", ".rb", ".kt",

        # Config
        ".json", ".yaml", ".yml",
        ".toml", ".ini", ".cfg",

        # DevOps
        ".sh", ".bash", ".zsh", ".ps1",

        # Documentation
        ".md", ".rst", ".txt"
    )

    IGNORED_DIRECTORIES = {
        ".git",
        "__pycache__",
        "node_modules",
        "dist",
        "build",
        "venv"
    }

    MAX_FILE_SIZE = 200000  # 200 KB

    def load_files(self, repo_path: str):

        documents = []

        for root, dirs, files in os.walk(repo_path):

            dirs[:] = [d for d in dirs if d not in self.IGNORED_DIRECTORIES]

            for file in files:

                if not file.endswith(self.SUPPORTED_EXTENSIONS):
                    continue

                file_path = os.path.join(root, file)

                if os.path.getsize(file_path) > self.MAX_FILE_SIZE:
                    continue

                try:

                    with open(file_path, "r", encoding="utf-8", errors="ignore") as f:

                        content = f.read()

                        documents.append(
                            {
                                "content": content,
                                "path": file_path
                            }
                        )

                except Exception:
                    continue

        return documents