from fastapi import APIRouter

from app.services.repo_service import RepoService
from app.services.parser_service import ParserService
from app.utils.chunker import CodeChunker
from app.services.embedding_service import EmbeddingService
from app.vectorstore.faiss_store import VectorStore

router = APIRouter()

repo_service = RepoService()
parser = ParserService()
chunker = CodeChunker()
embedding_service = EmbeddingService()

vector_store = None


@router.post("/index-repo")
def index_repo(repo_url: str):

    global vector_store

    repo_path = repo_service.clone_repository(repo_url)

    docs = parser.load_files(repo_path)

    chunks = chunker.chunk_documents(docs)

    vector_store = VectorStore(embedding_service)

    vector_store.create_vector_store(chunks)

    return {"status": "repository indexed"}