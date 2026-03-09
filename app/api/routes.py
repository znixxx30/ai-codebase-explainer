from fastapi import APIRouter

from app.services.repo_service import RepoService
from app.services.parser_service import ParserService
from app.utils.chunker import CodeChunker
from app.services.embedding_service import EmbeddingService
from app.vectorstore.faiss_store import VectorStore
from app.services.query_service import QueryService

router = APIRouter()

repo_service = RepoService()
parser = ParserService()
chunker = CodeChunker()
embedding_service = EmbeddingService()

vector_store = None

query_service = None


@router.post("/index-repo")
def index_repo(repo_url: str):

    global vector_store
    global query_service

    repo_path = repo_service.clone_repository(repo_url)

    docs = parser.load_files(repo_path)

    docs = docs[:40]   # development limit

    chunks = chunker.chunk_documents(docs)

    vector_store = VectorStore(embedding_service)

    vector_store.create_vector_store(chunks)

    query_service = QueryService(vector_store)

    return {"status": "repository indexed"}

@router.post("/ask")
def ask_question(question: str):

    if query_service is None:
        return {"error": "Repository not indexed yet"}

    answer = query_service.ask_question(question)

    return {"answer": answer}