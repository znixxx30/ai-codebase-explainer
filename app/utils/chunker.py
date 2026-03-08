from langchain_text_splitters import RecursiveCharacterTextSplitter
class CodeChunker:

    def __init__(self):

        self.splitter = RecursiveCharacterTextSplitter(
            chunk_size=1200,
            chunk_overlap=200,
            length_function=len
        )

    def chunk_documents(self, documents):

        texts = [doc["content"] for doc in documents]

        metadatas = [{"path": doc["path"]} for doc in documents]

        chunks = self.splitter.create_documents(
            texts,
            metadatas=metadatas
        )

        return chunks