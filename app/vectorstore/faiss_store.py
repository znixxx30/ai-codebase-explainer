import os
from langchain_community.vectorstores import FAISS
from langchain_core.documents import Document


class VectorStore:

    def __init__(self, embedding_service):

        self.embedding_service = embedding_service
        self.db = None
        self.index_path = "vector_db/index"

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

        os.makedirs("vector_db", exist_ok=True)

        self.db.save_local(self.index_path)

    def load_vector_store(self):

        self.db = FAISS.load_local(
            self.index_path,
            self.embedding_service.embedding_model,
            allow_dangerous_deserialization=True
        )

    def similarity_search(self, query, k=5):

        return self.db.similarity_search(query, k=k)