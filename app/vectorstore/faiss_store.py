from langchain_community.vectorstores import FAISS
from langchain_core.documents import Document


class VectorStore:

    def __init__(self, embedding_service):

        self.embedding_service = embedding_service
        self.db = None

    def create_vector_store(self, chunks):

        documents = [
            Document(
                page_content=chunk.page_content,
                metadata=chunk.metadata
            )
            for chunk in chunks
        ]

        self.db = FAISS.from_documents(
            documents,
            self.embedding_service.embedding_model
        )

    def similarity_search(self, query, k=5):

        return self.db.similarity_search(query, k=k)