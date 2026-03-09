from pydantic_settings import BaseSettings
from dotenv import load_dotenv

load_dotenv()


class Settings(BaseSettings):

    GEMINI_API_KEY: str | None = None

    REPO_STORAGE: str = "repos"

    VECTOR_DB_PATH: str = "vector_db"

    class Config:
        env_file = ".env"


settings = Settings()